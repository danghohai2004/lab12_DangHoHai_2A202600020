
#  Delivery Checklist — Day 13 Lab Submission

> **Student Name:** Đặng Hồ Hải 
> **Student ID:** 2A202600020 
> **Date:** 17/04/2026

---

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
1. Base image: `python:3.11-slim` (cho cả builder và runtime)
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
- Screenshot: [Link to screenshot in repo]

## Part 4: API Security

### Exercise 4.1-4.3: Test results
[Paste your test outputs]

### Exercise 4.4: Cost guard implementation
[Explain your approach]

## Part 5: Scaling & Reliability

### Exercise 5.1-5.5: Implementation notes
[Your explanations and test results]
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
-  All code runs without errors
-  Multi-stage Dockerfile (image < 500 MB)
-  API key authentication
-  Rate limiting (10 req/min)
-  Cost guard ($10/month)
-  Health + readiness checks
-  Graceful shutdown
-  Stateless design (Redis)
-  No hardcoded secrets
cl
---

### 3. Service Domain Link

Create a file `DEPLOYMENT.md` with your deployed service information:

```markdown
# Deployment Information

## Public URL
https://your-agent.railway.app

## Platform
Railway / Render / Cloud Run

## Test Commands

### Health Check
```bash
curl https://your-agent.railway.app/health
# Expected: {"status": "ok"}
```

### API Test (with authentication)
```bash
curl -X POST https://your-agent.railway.app/ask \
  -H "X-API-Key: YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test", "question": "Hello"}'
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

# 2. Authentication required
curl https://your-app.railway.app/ask
# Should return 401

# 3. With API key works
curl -H "X-API-Key: YOUR_KEY" https://your-app.railway.app/ask \
  -X POST -d '{"user_id":"test","question":"Hello"}'
# Should return 200

# 4. Rate limiting
for i in {1..15}; do 
  curl -H "X-API-Key: YOUR_KEY" https://your-app.railway.app/ask \
    -X POST -d '{"user_id":"test","question":"test"}'; 
done
# Should eventually return 429
```

---

##  Submission

**Submit your GitHub repository URL:**

```
https://github.com/your-username/day12-agent-deployment
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
