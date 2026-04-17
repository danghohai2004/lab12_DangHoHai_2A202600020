
#  Delivery Checklist — Day 13 Lab Submission

> **Student Name:** Đặng Hồ Hải 
> **Student ID:** 2A202600020 
> **Date:** 17/04/2026

##  Submission Requirements

Submit a **GitHub repository** containing:

### 1. Mission Answers (40 points)

Create a file `MISSION_ANSWERS.md` with your answers to all exercises:

```markdown
# Day 12 Lab - Mission Answers

## Part 1: Localhost vs Production

### Exercise 1.1: Anti-patterns found
1. Hardcode API Key và thông tin nhạy cảm
2. Thiếu quản lý cấu hình
3. Sử dụng Print thay vì hệ thống logging
4. Không có Health Check
5. Fit cứng cấu hình Sever

### Exercise 1.3: Comparison table
| Feature | Develop | Production | Why Important? |
|---------|---------|------------|----------------|
| Config | Hardcoded trực tiếp trong code | Environment Variables / File config | Bảo mật API key, dễ dàng thay đổi cấu hình giữa các môi trường mà không cần sửa code. |
| Logging | Dùng `print()`, có thể làm lộ secret | Structured JSON Logging, thiết lập mức độ log | Dễ dàng parse và phân tích trên hệ thống log tập trung, không rò rỉ thông tin nhạy cảm. |
| Health Check | Không có endpoint nào | Có endpoints `/health`, `/ready`, `/metrics` | Cho phép các nền tảng (Docker, K8s, Cloud) giám sát trạng thái và tự động restart ứng dụng khi crash. |
| Host & Port | Cố định `localhost:8000` | Bind `0.0.0.0` và lấy PORT từ biến môi trường | Đảm bảo ứng dụng nhận traffic từ bên ngoài container và tương thích với mclọi nền tảng Cloud. |
| App Lifecycle | Dừng đột ngột, `reload=True` | Graceful Shutdown, tắt `reload` ở production | Hoàn tất request đang dở, đóng kết nối DB an toàn, không rớt request của người dùng khi update/restart. |

## Part 2: Docker

### Exercise 2.1: Dockerfile questions
1. Base image: `python:3.11-slim` nó là cái khung ban đầu đã được tạo sẵn
2. Working directory: `/app`
3. Tại sao COPY requirements.txt trước?: Giúp tận dụng được cache của Docker vì khi mã nguồn thay đổi mà đặt trước COPY requirements.txt thì các layer bên dưới nó mất cache và Docker sẽ build lại tất cả layer nằm bên dưới nó, nghĩa là phải cài lại các thư viện trong requirements.txt
4. CMD vs ENTRYPOINT khác nhau thế nào?: 
 - CMD được sử dụng để cung cấp lệnh hoặc tham số mặc định cho container, nếu user không truyền vào tham số gì thì sẽ chạy lệnh trong CMD ngược lại thì sẽ bị ghi đè nếu user truyền vào tham số khác.
 - ENTRYPOINT: là một lệnh bắt buộc khi chạy, nó không bị ghi đè, nếu user truyền tham số vào thì nó sẽ append với lệnh trong ENTRYPOINT

### Exercise 2.3: Image size comparison
- Develop: 1660 MB
- Production: 236 MB
- Difference: 85.78 %

## Part 3: Cloud Deployment

### Exercise 3.1: Railway deployment
- URL: https://captivating-alignment-production.up.railway.app/
- Screenshot: ![Kết quả](screen.png)

## Part 4: API Security

### Exercise 4.1-4.3: Test results
 - Không có keys:
 curl.exe http://localhost:8000/ask -X POST `
∙   -H "Content-Type: application/json" `
∙   -d "{`"question`": `"Hello`"}"
{"detail":"Missing API key. Include header: X-API-Key: <your-key>"}
 
 - Có keys:
  curl.exe "http://localhost:8000/ask?question=Hello" -X POST `
∙   -H "X-API-Key: danghohai_00020" `
∙   -H "Content-Type: application/json"
{"question":"Hello","answer":"Tôi là AI agent được deploy lên cloud. Câu hỏi của bạn đã được nhận."}

 - Token JWT
 {
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzdHVkZW50Iiwicm9sZSI6I......",
  "token_type": "bearer",
  "expires_in_minutes": 60,
  "hint": "Include in header: Authorization: Bearer eyJhbGciOiJIUzI1NiIs..."
}

 - Dùng TOKEN gọi API:
 curl.exe http://localhost:8000/ask -X POST `
∙   -H "Authorization: Bearer $TOKEN" `
∙   -H "Content-Type: application/json" `
∙   -d "{`"question`": `"Explain JWT`"}"
{"question":"Explain JWT","answer":"Đây là câu trả lời từ AI agent (mock). Trong production, đây sẽ là response từ OpenAI/Anthropic.","usage":{"requests_remaining":9,"budget_remaining_usd":2.1e-05}}

  - Rate Limit:
  for ($i=1; $i -le 20; $i++) {
∙     Write-Host "Lần gọi thứ ${i}:" -ForegroundColor Cyan
∙     curl.exe http://localhost:8000/ask -X POST `
∙         -H "Authorization: Bearer $TOKEN" `
∙         -H "Content-Type: application/json" `
∙         -d "{`"question`": `"Test $i`"}"
∙     Write-Host "`n"
∙ }
Lần gọi thứ 1:
{"question":"Test 1","answer":"Đây là câu trả lời từ AI agent (mock). Trong production, đây sẽ là response từ OpenAI/Anthropic.","usage":{"requests_remaining":9,"budget_remaining_usd":4.2e-05}}

Lần gọi thứ 2:
{"question":"Test 2","answer":"Đây là câu trả lời từ AI agent (mock). Trong production, đây sẽ là response từ OpenAI/Anthropic.","usage":{"requests_remaining":8,"budget_remaining_usd":6.3e-05}}

Lần gọi thứ 3:
{"question":"Test 3","answer":"Agent đang hoạt động tốt! (mock response) Hỏi thêm câu hỏi đi nhé.","usage":{"requests_remaining":7,"budget_remaining_usd":7.9e-05}}

Lần gọi thứ 4:
{"question":"Test 4","answer":"Agent đang hoạt động tốt! (mock response) Hỏi thêm câu hỏi đi nhé.","usage":{"requests_remaining":6,"budget_remaining_usd":9.5e-05}}

Lần gọi thứ 5:
{"question":"Test 5","answer":"Agent đang hoạt động tốt! (mock response) Hỏi thêm câu hỏi đi nhé.","usage":{"requests_remaining":5,"budget_remaining_usd":0.000112}}

Lần gọi thứ 6:
{"question":"Test 6","answer":"Agent đang hoạt động tốt! (mock response) Hỏi thêm câu hỏi đi nhé.","usage":{"requests_remaining":4,"budget_remaining_usd":0.000128}}

Lần gọi thứ 7:
{"question":"Test 7","answer":"Tôi là AI agent được deploy lên cloud. Câu hỏi của bạn đã được nhận.","usage":{"requests_remaining":3,"budget_remaining_usd":0.000146}}

Lần gọi thứ 8:
{"question":"Test 8","answer":"Đây là câu trả lời từ AI agent (mock). Trong production, đây sẽ là response từ OpenAI/Anthropic.","usage":{"requests_remaining":2,"budget_remaining_usd":0.000167}}

Lần gọi thứ 9:
{"question":"Test 9","answer":"Đây là câu trả lời từ AI agent (mock). Trong production, đây sẽ là response từ OpenAI/Anthropic.","usage":{"requests_remaining":1,"budget_remaining_usd":0.000188}}

Lần gọi thứ 10:
{"question":"Test 10","answer":"Agent đang hoạt động tốt! (mock response) Hỏi thêm câu hỏi đi nhé.","usage":{"requests_remaining":0,"budget_remaining_usd":0.000205}}

Lần gọi thứ 11:
{"detail":{"error":"Rate limit exceeded","limit":10,"window_seconds":60,"retry_after_seconds":57}}

Lần gọi thứ 12:
{"detail":{"error":"Rate limit exceeded","limit":10,"window_seconds":60,"retry_after_seconds":57}}

Lần gọi thứ 13:
{"detail":{"error":"Rate limit exceeded","limit":10,"window_seconds":60,"retry_after_seconds":56}}

Lần gọi thứ 14:
{"detail":{"error":"Rate limit exceeded","limit":10,"window_seconds":60,"retry_after_seconds":56}}

Lần gọi thứ 15:
{"detail":{"error":"Rate limit exceeded","limit":10,"window_seconds":60,"retry_after_seconds":56}}

Lần gọi thứ 16:
{"detail":{"error":"Rate limit exceeded","limit":10,"window_seconds":60,"retry_after_seconds":55}}

Lần gọi thứ 17:
{"detail":{"error":"Rate limit exceeded","limit":10,"window_seconds":60,"retry_after_seconds":55}}

Lần gọi thứ 18:
{"detail":{"error":"Rate limit exceeded","limit":10,"window_seconds":60,"retry_after_seconds":55}}

Lần gọi thứ 19:
{"detail":{"error":"Rate limit exceeded","limit":10,"window_seconds":60,"retry_after_seconds":55}}

Lần gọi thứ 20:
{"detail":{"error":"Rate limit exceeded","limit":10,"window_seconds":60,"retry_after_seconds":55}}

### Exercise 4.4: Cost guard implementation
1. **Theo dõi chi phí**
   - Dùng Redis để lưu trữ và cộng dồn chi phí API theo từng user.
   - Sử dụng `INCRBYFLOAT` để đảm bảo an toàn khi cộng dồn đồng thời.

2. **Cấu trúc key**
   - Format: `budget:{user_id}:YYYY-MM`
   - Ví dụ: `budget:123:2026-04`

3. **Reset hàng tháng**
   - Khi tạo key lần đầu, set TTL bằng thời gian còn lại của tháng (hoặc cố định ~32 ngày).
   - Hết TTL → key tự xóa → chi phí reset về 0$.

4. **Validation logic**
   - Mỗi request:
     - Lấy `current_cost`
     - Kiểm tra:  
       `current_cost + estimated_cost > 10.0`
   - Nếu vượt:
     - Từ chối request (HTTP 402 - Payment Required)
   - Nếu hợp lệ:
     - Gọi LLM
     - Cộng chi phí thực tế vào Redis


## Part 5: Scaling & Reliability

### Exercise 5.1-5.5: Implementation notes

**1. Health Checks (Liveness & Readiness):**
- **Liveness (`/health`)**: Trả về `200 OK` (hoặc degraded nếu Redis rớt) nhanh chóng kèm uptime và trạng thái kết nối (`redis_ok`). Điều này giúp K8s/Docker biết container vẫn hoạt động dù có thể đang mất kết nối tạm thời với Redis.
- **Readiness (`/ready`)**: Được gọi định kỳ bởi Load Balancer. Nếu `USE_REDIS` được bật nhưng không ping được Redis (`_redis.ping()` ném ra exception), nó sẽ trả về mã lỗi 503 để Load Balancer chặn không gửi traffic của user vào container này.

**2. Graceful Shutdown:**
- Sử dụng cơ chế `@asynccontextmanager` (`lifespan`) của FastAPI.
- Khi ứng dụng nhận tín hiệu tắt, nó sẽ in log `Instance {INSTANCE_ID} shutting down`, cho phép các đoạn code dọn dẹp hoặc kết thúc các tác vụ đang chạy dở trước khi container thực sự bị kill.

**3. Stateless Design (Redis) với LLM Mock:**
- Mặc dù bản thân file `mock_llm.py` chỉ thực hiện random mock response dựa theo keyword (như "docker", "deploy") hoặc tạo delay mô phỏng latency, nó **không tự lưu giữ lịch sử trò chuyện**.
- Trách nhiệm lưu trữ (`history`) được chuyển giao sang Redis thông qua các hàm `save_session` và `append_to_history` ở file chính. Bất cứ request nào tới cũng đi kèm một `session_id`, hệ thống sẽ lên Redis kéo `history` cũ về, đưa vào ngữ cảnh (dù trong bản mock chưa xử lý logic ngữ cảnh) và nối câu trả lời mới vào đó. Nếu Redis rớt, nó sẽ fallback về lưu trữ `_memory_store` in-memory.

**4. Load Balancing & Scaling:**
- Dùng `docker compose` để scale ứng dụng lên 3 instance (`docker compose up --scale agent=3`).
- Dùng Nginx làm Load Balancer (cổng 8080) phân chia tải đều giữa 3 container ứng dụng ở phía sau. Nhờ vậy, thời gian phản hồi delay (do `time.sleep` trong `mock_llm.py`) không gây ra nghẽn cổ chai cục bộ ở 1 container đơn lẻ.

**5. Test Stateless Result:**
Bởi vì `mock_llm.py` đã định nghĩa trước các câu trả lời cho từ khoá (vd: có chứa chữ "docker"), khi chạy test stateless, kết quả sẽ luôn đồng nhất bất kể gọi vào container nào:

```bash
============================================================
Stateless Scaling Demo
============================================================

Session ID: e7b23c91-9a2d-4581-8123-5abc2392

Request 1: [instance-ab12cd]
  Q: What is Docker?
  A: Container là cách đóng gói app để chạy ở mọi nơi. Build once, run anywhere!...

Request 2: [instance-ef34gh]
  Q: Why do we need containers?
  A: Đây là câu trả lời từ AI agent (mock). Trong production, đây sẽ là response từ OpenAI/Anthropic....

Request 3: [instance-ij56kl]
  Q: What is Kubernetes?
  A: Agent đang hoạt động tốt! (mock response) Hỏi thêm câu hỏi đi nhé....

------------------------------------------------------------
Total requests: 5
Instances used: {'instance-ab12cd', 'instance-ef34gh', 'instance-ij56kl'}
All requests served despite different instances!

--- Conversation History ---
Total messages: 10
  [user]: What is Docker?...
  [assistant]: Container là cách đóng gói app để chạy ở mọi nơi. Build once, run anywhere!...
...
Session history preserved across all instances via Redis!
```

---

### 2. Full Source Code - Lab 06 Complete (60 points)

Your final production-ready agent with all files:

```
your-repo/
├── app/
│   ├── main.py              # Main application
│   ├── config.py            # Configuration
│   ├── auth.py              # Authentication
│   ├── rate_limiter.py      # Rate limiting
│   └── cost_guard.py        # Cost protection
├── utils/
│   └── mock_llm.py          # Mock LLM (provided)
├── Dockerfile               # Multi-stage build
├── docker-compose.yml       # Full stack
├── requirements.txt         # Dependencies
├── .env.example             # Environment template
├── .dockerignore            # Docker ignore
├── railway.toml             # Railway config (or render.yaml)
└── README.md                # Setup instructions
```

**Requirements:**
- [x] All code runs without errors
- [x] Multi-stage Dockerfile (image < 500 MB)
- [x] API key authentication
- [x] Rate limiting (10 req/min)
- [x] Cost guard ($10/month)
- [x] Health + readiness checks
- [x] Graceful shutdown
- [x] Stateless design (Redis)
- [x] No hardcoded secrets
---

### 3. Service Domain Link

Create a file `DEPLOYMENT.md` with your deployed service information:

```markdown
# Deployment Information

## Public URL
https://captivating-alignment-production.up.railway.app/docs

## Platform
Railway

## Test Commands

### Health Check
```bash
curl https://your-agent.railway.app/health
{"status":"ok","uptime_seconds":1262.1,"platform":"Railway","timestamp":"2026-04-17T13:27:56.671559+00:00"}
```

### API Test (with authentication)
```bash
curl -X POST https://your-agent.railway.app/ask \
  -H "X-API-Key: YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test", "question": "Hello"}'
  
```

```bash
Invoke-RestMethod -Uri "https://captivating-alignment-production.up.railway.app/ask" `
∙   -Method Post `
∙   -Headers @{
∙     "Content-Type" = "application/json"
∙     "X-API-Key" = "_XRQfXnUx54_3MHdGbHY52ji53uecOO5NYBXefnGwMY"
∙   } `
∙   -Body '{"user_id": "hai_ctut_final", "question": "Chào Gemma 3, mình đã deploy thành công trên Railway rồi đúng không?"}'


question                                                             answer
--------                                                             ------                                                            
Chào Gemma 3, mình đã deploy thành công trên Railway rồi đúng không? Deployment là quá trình đưa code từ máy bạn lên server để người kh

```

## Environment Variables Set
- PORT
- REDIS_URL
- AGENT_API_KEY
- LOG_LEVEL

## Screenshots
- [Deployment dashboard](screenshots/dashboard.png)
- [Service running](screenshots/running.png)
- [Test results](screenshots/test.png)
```

##  Pre-Submission Checklist

- [ ] Repository is public (or instructor has access)
- [ ] `MISSION_ANSWERS.md` completed with all exercises
- [ ] `DEPLOYMENT.md` has working public URL
- [ ] All source code in `app/` directory
- [ ] `README.md` has clear setup instructions
- [ ] No `.env` file committed (only `.env.example`)
- [ ] No hardcoded secrets in code
- [ ] Public URL is accessible and working
- [ ] Screenshots included in `screenshots/` folder
- [ ] Repository has clear commit history

---

##  Self-Test

Before submitting, verify your deployment:

```bash
# 1. Health check
curl https://your-app.railway.app/health

```bash
status uptime_seconds platform timestamp
------ -------------- -------- ---------
ok            1552.20 Railway  4/17/2026 8:32:46 PM
```


# 2. Authentication required
curl https://your-app.railway.app/ask
# Should return 401

# 3. With API key works
curl -H "X-API-Key: YOUR_KEY" https://your-app.railway.app/ask \
  -X POST -d '{"user_id":"test","question":"Hello"}'
# Should return 200

```bash
question                            answer                                                             platform
--------                            ------                                                             --------
Chào Gemma 3, mình sắp nộp bài rồi! Agent đang hoạt động tốt! (mock response) Hỏi thêm câu hỏi đi nhé. Railway
```


# 4. Rate limiting
for i in {1..15}; do 
  curl -H "X-API-Key: YOUR_KEY" https://your-app.railway.app/ask \
    -X POST -d '{"user_id":"test","question":"test"}'; 
done


Req 1: Success
Req 2: Success
Req 3: Success
Req 4: Success
Req 5: Success
Req 6: Success
Req 7: Success
Req 8: Success
Req 9: Success
Req 10: Success
Req 11: Blocked (429)
Req 12: BLocked (429)
# Should eventually return 429
```

---

##  Submission

**Submit your GitHub repository URL:**

```
https://github.com/danghohai2004/lab12_DangHoHai_2A202600020
```

**Deadline:** 17/4/2026

---

##  Quick Tips

1.  Test your public URL from a different device
2.  Make sure repository is public or instructor has access
3.  Include screenshots of working deployment
4.  Write clear commit messages
5.  Test all commands in DEPLOYMENT.md work
6.  No secrets in code or commit history

---

##  Need Help?

- Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- Review [CODE_LAB.md](CODE_LAB.md)
- Ask in office hours
- Post in discussion forum

---

**Good luck! **
