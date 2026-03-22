# AI Interior Decorator (Trang trí Nội thất bằng AI)

Ứng dụng này sử dụng FastAPI cho backend và Streamlit cho frontend.
Nó tận dụng Stable Diffusion với ControlNet để thiết kế lại các căn phòng.

## Cài đặt

### Yêu cầu bắt buộc

1. **Clone repository (Tải dự án bằng Git):**
```bash
git clone <repository_url>
cd interior-decorator-app
```

2. **Cài đặt `uv` bằng curl:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Cài đặt các thư viện phụ thuộc

Dự án này sử dụng [uv](https://github.com/astral-sh/uv) để quản lý dependency.

```bash
# Cài đặt thư viện
uv sync
```

## Chạy Ứng dụng

Bạn có thể sử dụng các lệnh sau để khởi động từng thành phần:

### 1. Khởi động API (Backend)
```bash
uv run api
```
API sẽ chạy tại địa chỉ `http://localhost:8000`.

### 2. Khởi động UI (Frontend)
```bash
uv run app
```
Giao diện người dùng (UI) sẽ tự động mở trên trình duyệt của bạn.

## Cấu trúc Dự án

- `api/`: Mã nguồn backend bằng FastAPI.
- `app/`: Mã nguồn frontend bằng Streamlit.
- `uploads/`: Lưu trữ tạm thời các hình ảnh được tải lên.
- `results/`: Lưu trữ các bản thiết kế được tạo ra.
