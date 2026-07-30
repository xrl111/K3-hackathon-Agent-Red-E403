# K3 Hackathon - System Architecture Overview

## 1. Mục tiêu (Goals)
Dự án được xây dựng với mục tiêu nhanh, dễ bảo trì, dễ mở rộng, và đặc biệt thân thiện cho việc phối hợp giữa con người (Nhiều Contributor) và Trợ lý AI. 

## 2. Công nghệ (Tech Stack)
- **Backend:** FastAPI, Pydantic V2, SQLAlchemy, Uvicorn.
- **Frontend:** Vue.js 3 (Composition API), Vite, TailwindCSS, Pinia.
- **AI Integration:** Direct API calls to LLM providers (OpenAI, Anthropic, Gemini, etc.) using unified interfaces.

## 3. Kiến trúc tổng thể (High-level Architecture)
Chúng ta áp dụng mô hình **Pragmatic Clean Architecture** (Kiến trúc Sạch Thực dụng). Do thời gian Hackathon ngắn (1.5 ngày), kiến trúc sẽ được làm phẳng một chút nhưng vẫn giữ nguyên tính chất phân tách trách nhiệm (Separation of Concerns).

```
[ Frontend (Vue3) ] <---(REST JSON/HTTP)---> [ Backend (FastAPI) ]
                                                   |
                                            [ AI Services / DB ]
```

### Backend Flow (FastAPI)
`Request -> API Router -> Schema Validation -> Service Logic -> Infrastructure (DB/AI API) -> Service Logic -> Schema Validation -> API Router -> Response`

### Frontend Flow (Vue 3)
`User Action -> Vue Component -> Pinia Action / Composable -> API Service (Axios) -> Backend -> Component State Update -> UI Rerender`

## 4. Quy trình làm việc (Workflow & Spec)
Bất kỳ ai (hoặc AI nào) khi join vào repo đều phải tuân thủ:
1. **Spec-first:** Đọc kỹ `/docs/architecture/` và `03-template-ai-spec.md`. Mọi thay đổi lớn đều bắt đầu từ việc cập nhật tài liệu spec.
2. **Dual-Judge Protocol:** Áp dụng tư duy đánh giá 2 chiều (Tổng thể kiến trúc vs. Chi tiết thực thi) trước khi code các logic phức tạp.
3. **Atomic Changes:** Tách nhỏ Pull Requests. Không sửa các phần code không liên quan đến Task hiện tại.
4. **Golden Set Testing:** Trước khi merge code liên quan đến AI, phải test với dữ liệu ở thư mục `/eval/` để đảm bảo không bị suy thoái chất lượng (Regression).
