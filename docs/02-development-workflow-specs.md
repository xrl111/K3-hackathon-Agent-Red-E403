# Quy Trình Phát Triển & Đặc Tả Công Việc (Development Workflow & Specs)
**Dự án:** PI-RAG Security Checker

Tài liệu này quy định luồng làm việc, quy tắc quản lý mã nguồn, cách sử dụng các AI Agent (Antigravity, Claude, Codex) và chi tiết phân rã công việc cho Frontend/Backend Developer. Đọc kỹ tài liệu này trước khi bắt đầu nhận task.

---

## 1. Quy tắc đặt tên Branch (GitHub Workflow)

Dự án áp dụng mô hình Git Flow rút gọn. Tất cả các tính năng mới đều phải được tách từ nhánh `develop` và tạo Pull Request (PR) để review trước khi merge.

### 1.1 Cấu trúc nhánh (Branches)
*   `main`: Nhánh chứa mã nguồn ổn định, sẵn sàng release.
*   `develop`: Nhánh tích hợp cho môi trường staging/testing.
*   `feature/*`: Nhánh phát triển tính năng mới.
*   `bugfix/*`: Nhánh sửa lỗi trong quá trình phát triển (trên develop).
*   `hotfix/*`: Nhánh sửa lỗi khẩn cấp (từ main).

### 1.2 Quy tắc đặt tên nhánh Feature
Vì dự án chia rõ FE và BE, tên nhánh bắt buộc phải có tiền tố role để dễ quản lý:
*   **Frontend:** `feature/fe-<epic>-<tên-task-ngắn-gọn>`
    *   *Ví dụ:* `feature/fe-intake-form`, `feature/fe-trace-viewer`
*   **Backend:** `feature/be-<epic>-<tên-task-ngắn-gọn>`
    *   *Ví dụ:* `feature/be-assessment-api`, `feature/be-rag-sandbox`
*   **DevOps/Docs:** `chore/ops-<tên-task>` hoặc `docs/<tên-task>`

### 1.3 Quy tắc Commit Message (Conventional Commits)
Sử dụng cấu trúc: `<type>(<scope>): <subject>`
*   `feat(fe-intake)`: Thêm form cấu hình target endpoint.
*   `fix(be-runner)`: Sửa lỗi timeout khi gọi LLM.
*   `docs(specs)`: Cập nhật tài liệu phân luồng công việc.

---

## 2. Quy trình làm việc với AI Agents (Antigravity, Claude, Codex)

Để tăng tốc độ phát triển, dev được khuyến khích sử dụng các AI coding assistant. Dưới đây là luồng kết hợp chuẩn:

### Bước 1: Phân tích & Lên kế hoạch (Sử dụng Antigravity)
*   **Trách nhiệm:** Tech Lead, PM, hoặc Dev trước khi code.
*   **Cách dùng:** Yêu cầu Antigravity đọc tài liệu (BRD/Specs), rà soát cấu trúc thư mục hiện tại (`/docs`, `/src`), và khởi tạo file thiết kế API Contract (OpenAPI/Swagger). Antigravity có khả năng đọc workspace rộng và giúp chốt luồng kiến trúc.

### Bước 2: Thiết kế UI & Code Frontend (Sử dụng Claude)
*   **Trách nhiệm:** Frontend Developer.
*   **Cách dùng:** Claude đặc biệt mạnh về UI/UX và logic luồng Front-end.
    *   Truyền API Contract (đã chốt ở Bước 1) vào cho Claude.
    *   Yêu cầu Claude generate các Component (React/Vue/Angular), Form Validation (Zod/Yup), và Dashboard layout.
    *   *Prompt mẫu:* "Dựa trên API Contract này, hãy viết React component cho Assessment Intake form có validation bắt buộc các trường Target URL và Policy."

### Bước 3: Logic, Database & Backend Core (Sử dụng Codex / Copilot)
*   **Trách nhiệm:** Backend & AI Engineer.
*   **Cách dùng:** Codex/Copilot rất mạnh trong việc hoàn thiện logic thuật toán, I/O, và test-cases.
    *   Viết schema SQL/ORM, background workers (Celery), và logic thao tác Vector DB (FAISS/Chroma).
    *   Viết Evaluator (Các regex, deterministic assertion để chấm điểm).
    *   *Prompt mẫu:* "Viết hàm Python nhận JSON raw trace, kiểm tra xem string 'CANARY_SECRET' có bị rò rỉ trong output hay không, xử lý an toàn với regex."

---

## 3. Đặc tả công việc chi tiết (Work Specs)

Dưới đây là 5 Epics chính của MVP. BE và FE checkout các branch tương ứng và bắt tay vào việc dựa trên API Contract.

### EPIC 1: Assessment Intake & Cấu hình Dự án
**Mục tiêu:** Giao diện cho Project Owner khai báo Target endpoint, policy, và các cấu hình an toàn.
*   **FE Branch:** `feature/fe-assessment-intake`
    *   Xây dựng Web Form (Multi-step): Khai báo Endpoint -> Policy & Secrets -> Test Profile.
    *   Validate dữ liệu form chặt chẽ (định dạng URL, JSON schema cho cấu hình).
*   **BE Branch:** `feature/be-assessment-intake`
    *   Thiết kế CSDL (Bảng `Assessments`, `TargetConfigs`).
    *   Xây dựng API `POST /api/assessments` nhận và validate payload từ FE.
    *   Xây dựng API `GET /api/assessments/:id` để render chi tiết.

### EPIC 2: PI Attack Orchestrator (Điều phối chạy Test)
**Mục tiêu:** Hệ thống chạy tấn công Prompt Injection ngầm và đẩy log lên FE.
*   **FE Branch:** `feature/fe-attack-runner`
    *   Dashboard hiển thị thanh tiến trình (Progress Bar) chạy test.
    *   Trace Viewer: UI dạng box chat/log hiển thị chi tiết từng câu Prompt gửi đi và Response nhận về.
*   **BE Branch:** `feature/be-attack-runner`
    *   Xây dựng Adapter kết nối tới hệ thống AI mục tiêu (Target Adapter).
    *   Viết Background Worker (Orchestrator) quản lý trạng thái, max-turns, và kill-switch.
    *   API `POST /api/assessments/:id/run` (trigger test) và luồng trả về trạng thái (Polling/WebSocket).

### EPIC 3: RAG Poisoning Sandbox
**Mục tiêu:** Môi trường clone Vector DB để bơm tài liệu nhiễm độc (Poison).
*   **FE Branch:** `feature/fe-rag-sandbox`
    *   UI cấu hình/upload Document hoặc trỏ tới Test Namespace.
    *   Bổ sung Trace Viewer hiển thị danh sách Top-K chunks (Chunk ID, văn bản, Score) và highlight đoạn văn bản chứa Poison.
*   **BE Branch:** `feature/be-rag-sandbox`
    *   Tích hợp Local Vector DB (FAISS/Chroma).
    *   Script tự động cắt chunk và Inject các "Poisoned Documents".
    *   API ghi nhận log retrieval pipeline mỗi khi query.

### EPIC 4: Evaluation & Findings Triage (Chấm điểm & Xác minh)
**Mục tiêu:** Chấm điểm pass/fail và giao diện cho con người duyệt kết quả (Human Review).
*   **FE Branch:** `feature/fe-evaluation-triage`
    *   Bảng danh sách Findings phân loại theo Severity (Critical, High...).
    *   Màn hình chi tiết Finding hỗ trợ nút "Override Severity" và "Mark as False Positive".
    *   Form gán Remediation (giao việc fix lỗi cho user khác).
*   **BE Branch:** `feature/be-evaluation-triage`
    *   Code hệ thống Deterministic Evaluator (Regex check Canary leak, Dummy action trigger).
    *   Tích hợp LLM Judge (gọi API GPT-4/Claude) để chấm điểm Rubric các case ngữ nghĩa.
    *   API CRUD cho Findings và cập nhật Status (`PUT /api/findings/:id/status`).

### EPIC 5: Reporting & CI/CD Runner
**Mục tiêu:** Dashboard điểm số, xuất báo cáo và CLI tích hợp pipeline.
*   **FE Branch:** `feature/fe-reporting-dashboard`
    *   Vẽ biểu đồ (Pie/Bar chart) hiển thị Readiness Score, ASR (Attack Success Rate).
    *   Nút xuất báo cáo PDF/HTML tổng hợp.
*   **BE Branch:** `feature/be-reporting-cicd`
    *   Viết Service tính toán tổng hợp các chỉ số Risk Score, ASR, PRR.
    *   Đóng gói CLI Tool (bằng Python hoặc Node.js) nhận Assessment ID, trigger test và trả về `exit code 1` nếu rớt kiểm duyệt bảo mật.
