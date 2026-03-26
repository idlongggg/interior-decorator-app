# Slide 3: Kiến trúc hệ thống (System Architecture)

## Prompt cho AI sinh slide

> Hãy tạo slide mô tả **kiến trúc tổng quan** của hệ thống AI Interior Decorator, trình bày đơn giản để người mới bắt đầu cũng hiểu được.

### Nội dung cần có trên slide:

#### Sơ đồ kiến trúc (Architecture Diagram):

```
┌──────────────────┐       HTTP API        ┌──────────────────────────┐
│   FRONTEND (App) │  ◄──────────────────► │     BACKEND (API)        │
│                  │    REST / JSON         │                          │
│  Next.js 16      │                       │  FastAPI (Python)        │
│  React 19        │                       │  Stable Diffusion 1.5   │
│  MUI v7          │                       │  ControlNet (Canny)     │
│  TypeScript      │                       │  PyTorch                │
│                  │                       │                          │
│  Port: 3000      │                       │  Port: 8000             │
└──────────────────┘                       └──────────────────────────┘
         │                                            │
         └────────── Docker Compose ──────────────────┘
```

#### Giải thích từng thành phần:

| Thành phần | Công nghệ | Vai trò |
|---|---|---|
| **Frontend** | Next.js 16 + React 19 + MUI v7 | Giao diện người dùng: upload ảnh, chọn style, hiển thị kết quả |
| **Backend** | FastAPI (Python) | Xử lý logic: nhận ảnh, chạy AI model, trả kết quả |
| **AI Engine** | Stable Diffusion 1.5 + ControlNet | Bộ não AI: phân tích ảnh & sinh ảnh mới |
| **Container** | Docker Compose | Đóng gói toàn bộ app để chạy trên mọi máy |

### Giải thích cho người mới (Newbie):
- **Frontend** = Cái mà bạn nhìn thấy trên trình duyệt (giao diện đẹp, nút bấm, hình ảnh)
- **Backend** = Bộ phận xử lý phía sau, nơi AI thực sự làm việc (bạn không nhìn thấy)
- **API** = Cách Frontend và Backend "nói chuyện" với nhau (giống như gửi tin nhắn qua bưu điện)
- **Docker** = Giống như một "hộp" đóng gói mọi thứ lại, ai cũng có thể mở hộp ra và chạy được mà không cần cài thêm gì

### Gợi ý thiết kế:
- Sơ đồ trung tâm, to rõ ràng
- Dùng icon cho mỗi thành phần (🖥️ Frontend, ⚙️ Backend, 🧠 AI Engine, 📦 Docker)
- Tông màu: xanh dương chủ đạo, nền trắng/sáng
- Mũi tên hai chiều giữa Frontend ↔ Backend
