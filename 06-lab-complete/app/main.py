"""
Production AI Agent — Đã đồng bộ với file Config của Hải
"""

import json
import logging
import time
from contextlib import asynccontextmanager
from datetime import datetime, timezone

import google.generativeai as genai
import redis.asyncio as redis

# Import settings từ file config của bạn
from app.config import settings
from fastapi import Depends, FastAPI, HTTPException, Request, Response, Security
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security.api_key import APIKeyHeader
from pydantic import BaseModel, Field

# ─────────────────────────────────────────────────────────
# Logging
# ─────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format='{"ts":"%(asctime)s","lvl":"%(levelname)s","msg":"%(message)s"}',
)
logger = logging.getLogger(__name__)

START_TIME = time.time()
_is_ready = False

# ─────────────────────────────────────────────────────────
# Auth & Security
# ─────────────────────────────────────────────────────────
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def verify_api_key(api_key: str = Security(api_key_header)) -> str:
    # Fix: dùng settings.agent_api_key (viết thường)
    if not api_key or api_key != settings.agent_api_key:
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API key. Include header: X-API-Key: <key>",
        )
    return api_key


# ─────────────────────────────────────────────────────────
# Lifespan
# ─────────────────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    global _is_ready
    # Khởi tạo Redis
    app.state.redis = redis.from_url(settings.redis_url, decode_responses=True)

    # Cấu hình Gemini
    genai.configure(api_key=settings.openai_api_key)
    app.state.gemini = genai.GenerativeModel(settings.llm_model)

    logger.info(
        json.dumps(
            {"event": "startup", "app": settings.app_name, "env": settings.environment}
        )
    )

    _is_ready = True
    yield
    _is_ready = False
    await app.state.redis.close()


# ─────────────────────────────────────────────────────────
# App Setup
# ─────────────────────────────────────────────────────────
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan,
    docs_url="/docs" if settings.environment != "production" else None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type", "X-API-Key"],
)


@app.middleware("http")
async def security_middleware(request: Request, call_next):
    start = time.time()
    try:
        response: Response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"

        # Fix lỗi pop attribute
        if "server" in response.headers:
            del response.headers["server"]

        duration = round((time.time() - start) * 1000, 1)
        logger.info(
            json.dumps(
                {
                    "event": "request",
                    "method": request.method,
                    "path": request.url.path,
                    "status": response.status_code,
                    "ms": duration,
                }
            )
        )
        return response
    except Exception as e:
        logger.error(f"Middleware Error: {e}")
        raise


# ─────────────────────────────────────────────────────────
# Rate Limit & Cost Guard (Redis)
# ─────────────────────────────────────────────────────────
async def check_limits(api_key: str, redis_client: redis.Redis):
    # Rate Limit
    now_min = int(time.time() // 60)
    rl_key = f"rl:{api_key[:8]}:{now_min}"
    count = await redis_client.incr(rl_key)
    if count == 1:
        await redis_client.expire(rl_key, 60)

    if count > settings.rate_limit_per_minute:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    # Cost Guard
    month_key = f"cost:{datetime.now().strftime('%Y-%m')}"
    current_cost = await redis_client.get(month_key) or 0
    if float(current_cost) >= settings.daily_budget_usd:
        raise HTTPException(status_code=402, detail="Budget exhausted")


# ─────────────────────────────────────────────────────────
# Endpoints
# ─────────────────────────────────────────────────────────
class AskRequest(BaseModel):
    user_id: str = "default"
    question: str = Field(..., min_length=1, max_length=2000)


@app.post("/ask", tags=["Agent"])
async def ask_agent(body: AskRequest, api_key: str = Depends(verify_api_key)):
    await check_limits(api_key, app.state.redis)

    try:
        response = await app.state.gemini.generate_content_async(body.question)

        # Ghi nhận cost ảo ($0.01/req)
        month_key = f"cost:{datetime.now().strftime('%Y-%m')}"
        await app.state.redis.incrbyfloat(month_key, 0.01)

        return {
            "question": body.question,
            "answer": response.text,
            "model": settings.llm_model,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI Error: {str(e)}")


@app.get("/health")
def health():
    return {"status": "ok", "uptime": round(time.time() - START_TIME, 1)}


@app.get("/ready")
def ready():
    if not _is_ready:
        raise HTTPException(503, "Not ready")
    return {"status": "ready"}


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
