# Production-Ready Software Development Life Cycle (SDLC) for AI Agents

All AI Agents (Antigravity, Claude, Codex, Cursor, etc.) operating in this repository MUST strictly follow this 5-step SDLC process to ensure production-level code quality.

## Step 1: Spec & Context Retrieval (Đọc Hiểu Yêu Cầu)
- **Hành động:** Khi nhận task, Agent KHÔNG ĐƯỢC code ngay.
- **Nhiệm vụ:**
  1. Đọc `/docs/architecture/01-system-overview.md` để hiểu hệ thống.
  2. Đọc file spec của feature (VD: `spec.md`).
  3. Quét qua codebase hiện tại để nhận diện các patterns đã có.
- **Bắt buộc:** Áp dụng **Dual-Judge Protocol** để vạch ra kế hoạch (Plan) trước khi đụng vào code.

## Step 2: Implementation & Atomic Commits (Thực Thi Code)
- **Hành động:** Viết code theo từng phần nhỏ (Atomic changes).
- **Quy chuẩn Backend (FastAPI):**
  - Schema phải nằm trong `/schemas`.
  - Logic nghiệp vụ phải nằm trong `/services`.
  - Controller (API) chỉ làm nhiệm vụ parse request và gọi service.
- **Quy chuẩn Frontend (Vue3):**
  - Tách UI (Components) khỏi Logic (Composables/Stores).
- **Bắt buộc:** Sau mỗi thay đổi logic lớn, Agent phải tự động kiểm tra xem có phá vỡ Clean Architecture không.

## Step 3: Self-Correction & Linters (Tự Đánh Giá Bằng Máy)
- **Hành động:** Không dựa hoàn toàn vào cảm tính, phải dùng công cụ kiểm tra.
- **Backend:** Chạy `ruff` (linter) và `mypy` (type checker). Nếu có lỗi, Agent phải tự động sửa (Self-heal) trước khi báo cáo hoàn thành.
- **Frontend:** Chạy `eslint` và `vue-tsc` để check kiểu dữ liệu.

## Step 4: Testing & Golden Set Validation (Kiểm Thử)
- **Hành động:** Viết test cho logic vừa tạo.
- Đối với các tính năng có gọi AI (LLM), phải chạy dữ liệu qua tập `/eval/` (Golden Set) để đo lường độ chính xác.
- Đảm bảo mã lỗi (Error Handling) được test cẩn thận (ví dụ: DB rớt, API LLM timeout).

## Step 5: Memory Sync & Documentation (Đồng Bộ Trí Nhớ)
- **Hành động:** Trí nhớ của Agent bị xóa sau mỗi phiên, do đó phải lưu trữ kiến thức lại vào repo.
- Nếu có quyết định kiến trúc mới hoặc pattern mới, Agent BẮT BUỘC phải ghi log lại vào thư mục `/docs/memory/` (VD: `docs/memory/decision-001-auth-flow.md`).
- Cập nhật lại README nếu cần thiết.
