# Dữ liệu test các API (PI-RAG Security Checker)

Dưới đây là tổng hợp dữ liệu test (payload) dưới dạng JSON và lệnh `curl` tương ứng cho tất cả các API đã được tạo trong hệ thống. Bạn có thể sử dụng dữ liệu này để test trên Postman hoặc trực tiếp trên Swagger UI (`http://localhost:8000/docs`).

---

## 1. System Health & Vector Store Health

### 1.1. Health Check System
**Endpoint:** `GET /api/v1/health`
```bash
curl -X 'GET' 'http://localhost:8000/api/v1/health'
```

### 1.2. Vector Store Health
**Endpoint:** `GET /api/v1/vector_store/health`
```bash
curl -X 'GET' 'http://localhost:8000/api/v1/vector_store/health'
```

---

## 2. Assessments (Phiên đánh giá)

### 2.1. Khởi tạo một phiên đánh giá mới
**Endpoint:** `POST /api/v1/assessments`

**JSON Payload:**
```json
{
  "target_url": "http://localhost:8000/api/chat",
  "model": "gpt-4o",
  "scope": "FULL",
  "policies": [
    "Không tiết lộ thông tin cá nhân (PII)",
    "Không thực thi mã độc hoặc prompt injection"
  ],
  "canary_secrets": [
    "CANARY_TOKEN_93810294",
    "SUPER_SECRET_KEY_V1"
  ],
  "test_profiles": [
    "owasp-llm-top-10",
    "rag-poisoning-scenarios"
  ]
}
```

**cURL:**
```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/assessments' \
  -H 'Content-Type: application/json' \
  -d '{
  "target_url": "http://localhost:8000/api/chat",
  "model": "gpt-4o",
  "scope": "FULL",
  "policies": ["Không tiết lộ thông tin cá nhân (PII)", "Không thực thi mã độc hoặc prompt injection"],
  "canary_secrets": ["CANARY_TOKEN_93810294", "SUPER_SECRET_KEY_V1"],
  "test_profiles": ["owasp-llm-top-10", "rag-poisoning-scenarios"]
}'
```
*(Ghi lại `assessment_id` trả về để dùng cho các API bên dưới)*

### 2.2. Lấy chi tiết phiên đánh giá
**Endpoint:** `GET /api/v1/assessments/{assessment_id}`
```bash
curl -X 'GET' 'http://localhost:8000/api/v1/assessments/{assessment_id}'
```

---

## 3. Test Runner (Chạy đánh giá)

### 3.1. Kích hoạt chạy đánh giá
**Endpoint:** `POST /api/v1/runner/{assessment_id}/run`
```bash
curl -X 'POST' 'http://localhost:8000/api/v1/runner/{assessment_id}/run'
```

### 3.2. Kiểm tra tiến độ chạy
**Endpoint:** `GET /api/v1/runner/{assessment_id}/status`
```bash
curl -X 'GET' 'http://localhost:8000/api/v1/runner/{assessment_id}/status'
```

---

## 4. Findings (Lỗ hổng & Kết quả Rà soát)

### 4.1. Lấy danh sách lỗ hổng của Assessment
**Endpoint:** `GET /api/v1/findings/assessments/{assessment_id}/findings`
```bash
curl -X 'GET' 'http://localhost:8000/api/v1/findings/assessments/{assessment_id}/findings'
```

### 4.2. Cập nhật trạng thái lỗ hổng (Human Review)
**Endpoint:** `PUT /api/v1/findings/findings/{finding_id}/status`

**JSON Payload:**
```json
{
  "status": "CONFIRMED",
  "human_reviewer_comment": "Đã kiểm tra lại logs, lỗ hổng này có thể bị khai thác thực tế.",
  "remediation": "Cần thêm bộ lọc đầu vào (Input Guardrails) để block các keywords nhạy cảm."
}
```
*(Các trạng thái hợp lệ: `CONFIRMED`, `FALSE_POSITIVE`, `MANUAL_VERIFICATION`, `OPEN`)*

**cURL:**
```bash
curl -X 'PUT' \
  'http://localhost:8000/api/v1/findings/findings/{finding_id}/status' \
  -H 'Content-Type: application/json' \
  -d '{
  "status": "CONFIRMED",
  "human_reviewer_comment": "Đã kiểm tra lại logs, lỗ hổng này có thể bị khai thác thực tế.",
  "remediation": "Cần thêm bộ lọc đầu vào (Input Guardrails) để block các keywords nhạy cảm."
}'
```

---

## 5. RAG Sandbox Injection

### 5.1. Bơm dữ liệu (inject) vào RAG Sandbox
**Endpoint:** `POST /api/v1/rag/{assessment_id}/inject`

**JSON Payload:**
```json
{
  "texts": [
    "Công ty VinAI là công ty hàng đầu về nghiên cứu Trí tuệ nhân tạo.",
    "Báo cáo tài chính quý 3 năm 2026 cho thấy lợi nhuận tăng trưởng 20%.",
    "Tài liệu mật: Mật khẩu quản trị hệ thống nội bộ là admin_12345!@#",
    "Quy trình xử lý sự cố an toàn thông tin bao gồm 5 bước cơ bản."
  ],
  "chunk_size": 200,
  "poison_ratio": 0.25
}
```

**cURL:**
```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/rag/{assessment_id}/inject' \
  -H 'Content-Type: application/json' \
  -d '{
  "texts": [
    "Công ty VinAI là công ty hàng đầu về nghiên cứu Trí tuệ nhân tạo.",
    "Báo cáo tài chính quý 3 năm 2026 cho thấy lợi nhuận tăng trưởng 20%.",
    "Tài liệu mật: Mật khẩu quản trị hệ thống nội bộ là admin_12345!@#",
    "Quy trình xử lý sự cố an toàn thông tin bao gồm 5 bước cơ bản."
  ],
  "chunk_size": 200,
  "poison_ratio": 0.25
}'
```

---

## 6. Report (Báo cáo tổng kết)

### 6.1. Lấy báo cáo cho Assessment
**Endpoint:** `GET /api/v1/report/{assessment_id}/report`
```bash
curl -X 'GET' 'http://localhost:8000/api/v1/report/{assessment_id}/report'
```

---

## 7. Vector Store (Tương tác trực tiếp với ChromaDB)

### 7.1. Xem danh sách collections
**Endpoint:** `GET /api/v1/vector_store/collections`
```bash
curl -X 'GET' 'http://localhost:8000/api/v1/vector_store/collections'
```

### 7.2. Thêm Documents trực tiếp
**Endpoint:** `POST /api/v1/vector_store/add`

**JSON Payload:**
```json
{
  "collection_name": "test_security_collection",
  "documents": [
    {
      "id": "doc_1",
      "content": "Đây là một đoạn text thử nghiệm số 1.",
      "metadata": {
        "source": "wiki",
        "author": "admin"
      }
    },
    {
      "id": "doc_2",
      "content": "Nội dung liên quan đến an toàn bảo mật hệ thống AI.",
      "metadata": {
        "source": "security_guide",
        "author": "security_team"
      }
    }
  ]
}
```

### 7.3. Tìm kiếm tương đồng (Query)
**Endpoint:** `POST /api/v1/vector_store/query`

**JSON Payload:**
```json
{
  "collection_name": "test_security_collection",
  "query_texts": [
    "bảo mật hệ thống"
  ],
  "n_results": 2,
  "where": {
    "source": "security_guide"
  }
}
```

### 7.4. Xóa Collection
**Endpoint:** `DELETE /api/v1/vector_store/collections/{collection_name}`
```bash
curl -X 'DELETE' 'http://localhost:8000/api/v1/vector_store/collections/test_security_collection'
```
