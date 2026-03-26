# Slide 5: Quy trình hoạt động — How It Works (Pipeline)

## Prompt cho AI sinh slide

> Hãy tạo slide mô tả **quy trình hoạt động từng bước** (pipeline) của dự án AI Interior Decorator, từ khi người dùng upload ảnh đến khi nhận kết quả.

### Nội dung cần có trên slide:

#### Pipeline hoạt động (6 bước):

```
STEP 1          STEP 2           STEP 3           STEP 4            STEP 5           STEP 6
📸 Upload      🎨 Chọn Style    📤 Gửi API      ✏️ Canny Edge     🧠 AI Generate   🖼️ Kết quả
───────── ──► ──────────── ──► ─────────── ──► ──────────── ──► ──────────── ──► ────────────
Người dùng    Minimalist/      Frontend gọi     Ảnh gốc được      SD 1.5 nhận      Ảnh phòng
chụp & upload Scandi/Indo/     Backend API      chuyển thành       edge map +       mới được
ảnh phòng     Modern/Custom    POST /generate   "bản phác thảo"   text prompt      trả về user
                                                (edge map)         → sinh ảnh
```

#### Chi tiết kỹ thuật từng bước:

| Bước | Người dùng thấy | Hệ thống làm phía sau |
|---|---|---|
| **1. Upload** | Kéo thả hoặc chọn file ảnh | `POST /upload` → Lưu ảnh vào thư mục `uploads/` |
| **2. Chọn Style** | Bấm vào card phong cách | Frontend cập nhật state `selectedStyle` |
| **3. Gửi Request** | Bấm nút "Generate Design" | `POST /generate` → Tạo `task_id`, chạy background task |
| **4. Canny Edge** | Thấy loading... | OpenCV Canny: phát hiện cạnh (threshold 100/200) → tạo edge map |
| **5. AI Generate** | Thanh tiến trình 0% → 100% | Stable Diffusion chạy 35–50 bước inference, mỗi bước callback cập nhật progress |
| **6. Kết quả** | Ảnh phòng mới hiện ra | Ảnh lưu vào `results/`, trả URL qua `GET /results/{filename}` |

#### Polling cập nhật tiến trình:
- Frontend gọi `GET /status/{task_id}` mỗi **1 giây**
- Backend trả về: `progress`, `total_steps`, `remaining_time`, `status`
- Khi `status === "completed"` → hiển thị ảnh kết quả

### Giải thích cho người mới (Newbie):
- Quá trình này giống như đặt hàng online:
  1. 📸 Bạn **gửi ảnh** (giống upload ảnh hàng bị lỗi để khiếu nại)
  2. 🎨 Bạn **chọn kiểu** muốn (giống chọn màu/size)
  3. 📤 Bạn **bấm đặt** (giống bấm "Mua hàng")
  4. ⏳ Hệ thống **xử lý** (giống shipper đang giao)
  5. 📊 Bạn **theo dõi** (giống xem tracking đơn hàng)
  6. 🖼️ Bạn **nhận kết quả** (giống nhận hàng!)

### Gợi ý thiết kế:
- Sơ đồ quy trình ngang (horizontal flow) với 6 node liên kết bằng mũi tên
- Mỗi step có icon tròn và label bên dưới
- Dùng animation: mỗi step xuất hiện lần lượt
- Bảng chi tiết nhỏ hơn bên dưới sơ đồ
- Tông màu xanh → tím gradient
