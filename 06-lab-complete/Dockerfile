# ============================================================
# Production Dockerfile — Đã sửa lỗi crash cho Hải
# ============================================================

# Stage 1: Builder
FROM python:3.11-slim AS builder

WORKDIR /build

RUN apt-get update && apt-get install -y gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
# Cài đặt vào /root/.local
RUN pip install --no-cache-dir --user -r requirements.txt


# Stage 2: Runtime
FROM python:3.11-slim AS runtime

# Tạo user agent và thiết lập thư mục home là /home/agent
RUN groupadd -r agent && useradd -r -g agent -m -d /home/agent agent

WORKDIR /app

# 1. Copy packages từ builder vào đúng thư mục .local của user agent
COPY --from=builder /root/.local /home/agent/.local

# 2. Copy source code
COPY app/ ./app/
COPY utils/ ./utils/

# 3. Quan trọng: Cấp quyền cho user agent trên cả thư mục app và thư mục thư viện
RUN chown -R agent:agent /app /home/agent/.local

USER agent

# 4. CẤU HÌNH BIẾN MÔI TRƯỜNG ĐỂ FIX LỖI CRASH
ENV PYTHONUSERBASE=/home/agent/.local
ENV PATH=/home/agent/.local/bin:$PATH
# PYTHONPATH cần bao gồm cả folder app để tìm thấy module 'app'
ENV PYTHONPATH=/app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Đảm bảo đường dẫn module đúng với cấu trúc app/main.py
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
