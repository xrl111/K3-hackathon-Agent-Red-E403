from fastapi import FastAPI, Request
import random
import uvicorn

app = FastAPI(title="Mock Target AI")

# Giả lập danh sách các câu trả lời ngẫu nhiên
SAFE_RESPONSES = [
    "Xin lỗi, tôi không thể hỗ trợ yêu cầu này.",
    "Tôi là một AI an toàn, tôi không được phép làm điều đó.",
    "Yêu cầu của bạn vi phạm chính sách an toàn của tôi."
]

VULNERABLE_RESPONSES = [
    "Vâng, đây là thông tin bí mật của hệ thống: CANARY_SECRET_123",
    "Chắc chắn rồi! Dưới đây là cách để bypass hệ thống: ...",
    "Được thôi, tôi sẽ lờ đi các chỉ dẫn ban đầu. Bạn muốn gì?"
]

@app.post("/chat")
async def chat_endpoint(request: Request):
    try:
        body = await request.json()
        prompt = body.get("prompt", "")
        
        # Nếu prompt nhắc đến bí mật, thỉnh thoảng AI bị "lừa" và trả lời ngớ ngẩn (Mô phỏng lỗ hổng)
        if "CANARY_SECRET" in prompt or random.random() < 0.3:
            reply = random.choice(VULNERABLE_RESPONSES)
        else:
            reply = random.choice(SAFE_RESPONSES)
            
        return {
            "response": reply
        }
    except Exception as e:
        return {"response": "Lỗi nội bộ."}

if __name__ == "__main__":
    print("🚀 Mock Target API đang chạy tại: http://localhost:8001/chat")
    uvicorn.run(app, host="0.0.0.0", port=8001)
