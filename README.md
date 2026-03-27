# 🎨 Interior Decorator AI (Kiến Trúc Sư AI)

Chào mừng bạn đến với ứng dụng **Interior Decorator AI**! Đây là một nền tảng sáng tạo cho phép bạn biến những bản phác thảo (sketch) hoặc ảnh phòng trống thành những bản thiết kế nội thất hoàn mỹ chỉ trong vài giây bằng sức mạnh của AI.

## 🌟 Chức năng nổi bật
- **Phân tích thông minh:** AI tự động phân biệt Sàn (floor), Tường (wall) và Trần (ceiling).
- **ControlNet Precision:** Sử dụng Canny, Lineart hoặc Scribble để giữ nguyên cấu trúc không gian của bạn.
- **Thỏa sức sáng tạo:** Hỗ trợ nhiều phong cách: Indochine, Minimalist, Scandinavian, Modern, Zen... hoặc nhập prompt tùy chỉnh.
- **Inpainting (Thêm đồ nội thất):** AI tự động tìm vị trí trống phù hợp để đặt Sofa, Bàn, Đèn, Cây xanh...
- **Real-time Progress:** Xem tiến trình AI làm việc qua giao diện mượt mà (Server-Sent Events).
- **Comparison Slider:** Dễ dàng so sánh kết quả ảnh Trước (Before) và Sau (After).

---

## 🏗️ Kiến trúc dự án
Ứng dụng được chia làm 2 phần chính:
1. **Frontend (`/app`):** Được xây dựng bằng Next.js 15, React, Tailwind CSS v4 và HeroUI.
2. **Backend (`/api`):** Sử dụng FastAPI (Python), PyTorch và mô hình AI từ Hugging Face Diffusers.

---

## 🚀 Hướng dẫn khởi chạy

### 1. Chuẩn bị (Prerequisites)
- [Node.js](https://nodejs.org/) (Khuyên dùng v18+) & [pnpm](https://pnpm.io/)
- [Python 3.10+](https://www.python.org/) & [uv](https://docs.astral.sh/uv/) (Trình quản lý gói siêu tốc cho Python)

---

### 2. Chạy Backend (API)
Mở terminal tại thư mục gốc của dự án:

```bash
cd api
```

#### Cài đặt môi trường:
Nếu bạn đã cài `uv` (khuyên dùng):
```bash
uv sync
```

Hoặc dùng `pip` truyền thống:
```bash
pip install -r pyproject.toml # Hoặc cài thủ công các dependency trong file
```

#### Thiết lập API Key:
Tạo file `.env` trong thư mục `api` (nếu chưa có):
```env
HF_API_KEY=hf_your_token_here
```
*(Lấy token miễn phí tại [huggingface.co](https://huggingface.co/settings/tokens))*

#### Khởi chạy:
```bash
uv run python main.py
```
> API sẽ chạy tại `http://localhost:8000`.

---

### 3. Chạy Frontend (App)
Mở một terminal mới (vẫn ở thư mục gốc dự án):

```bash
cd app
```

#### Cài đặt:
```bash
pnpm install
```

#### Thiết lập môi trường:
Đảm bảo file `.env` có cấu hình:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

#### Khởi chạy:
```bash
pnpm dev
```
> Truy cập ứng dụng tại: `http://localhost:3000`

---

## 🛠️ Công nghệ sử dụng
- **AI Models:**
  - `runwayml/stable-diffusion-v1-5` (Gốc)
  - `lllyasviel/control_v11p_sd15_lineart` (ControlNet)
  - `nvidia/segformer-b2-finetuned-ade-512-512` (Phân mảnh ngữ nghĩa)
- **Frontend Stack:** Next.js (App Router), Framer Motion, HeroUI Components, Tailwind CSS v4.
- **Backend Stack:** FastAPI, SSE (Streaming), Pillow, OpenCV.

## 📝 Lưu ý quan trọng
- Lần chạy đầu tiên, API sẽ tải các mô hình AI từ Hugging Face (nặng khoảng vài GB). Vui lòng kiên nhẫn.
- Đối với máy Mac (M1/M2/M3), ứng dụng đã cấu hình tự động sử dụng nhân **MPS** (Metal Performance Shaders) để tối ưu tốc độ.

---
Chúc bạn có những trải nghiệm thiết kế thú vị! ✨
