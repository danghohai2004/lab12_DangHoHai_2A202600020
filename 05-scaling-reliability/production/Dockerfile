FROM python:3.11-slim

WORKDIR /app

# Cài đặt các thư viện cần thiết cho bài 05
RUN pip install --no-cache-dir fastapi uvicorn[standard] pydantic redis

# Copy source code của bài 05 (Stateless Agent)
COPY 05-scaling-reliability/production/app.py /app/app.py

# Copy utils (Mock LLM) từ thư mục gốc của project
RUN mkdir -p /app/utils
COPY utils/mock_llm.py /app/utils/mock_llm.py

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=15s --timeout=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Khởi chạy server
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
