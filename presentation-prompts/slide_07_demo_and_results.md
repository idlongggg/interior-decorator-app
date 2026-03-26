# Slide 7: Demo & Kết quả (Results)

## Prompt cho AI sinh slide

> Hãy tạo slide trình bày **demo giao diện** và **kết quả thực tế** của dự án AI Interior Decorator, thể hiện trải nghiệm người dùng và chất lượng output.

### Nội dung cần có trên slide:

#### 🖥️ Giao diện ứng dụng (UI Demo):

**Mô tả giao diện chính:**
- **Header**: Tiêu đề "AI Interior Decorator" + tagline "Transform your room in seconds using AI"
- **Panel trái**: Khu vực upload ảnh (kéo thả hoặc chọn file, hỗ trợ Camera & Gallery)
- **Panel phải**: 5 card phong cách (Minimalist / Scandinavian / Indochine / Modern / Custom)
- **Nút chính**: "Generate Design" — nút xanh dương, to, nổi bật
- **Khu vực kết quả**: 2 ảnh cạnh nhau (Original Room | AI Generated Result)
- **Thanh tiến trình**: Hiệu ứng glassmorphism, hiển thị "Step X of Y", "Estimated: Xs remaining"

#### 📊 Kết quả thực tế (Before → After):

Trình bày 4 ví dụ kết quả:

| # | Phong cách | Mô tả kết quả |
|---|---|---|
| 1 | **Minimalist** | Tường trắng, đồ nội thất tối giản, bàn gỗ đơn giản, TV treo tường không dây |
| 2 | **Scandinavian** | Gỗ sáng, rèm lanh xám, cây xanh, chăn len chunky, tone ấm áp |
| 3 | **Indochine** | Gỗ tối chạm khắc, mây tre, rèm hoa văn, tone đất ấm, đèn đồng |
| 4 | **Modern** | Bàn kính/bê tông, ghế mid-century, rèm roller xám đậm, đèn geometric |

#### ⏱️ Hiệu suất (Performance):

| Metric | Giá trị |
|---|---|
| Thời gian xử lý (GPU NVIDIA) | ~30–60 giây |
| Thời gian xử lý (Apple MPS) | ~2–4 phút |
| Thời gian xử lý (CPU only) | ~10–20 phút |
| Kích thước ảnh output | Tối đa 768px (cạnh dài) |
| Định dạng output | PNG |

#### 🎯 Đánh giá chất lượng:
- ✅ **Giữ cấu trúc phòng**: Tường, cửa sổ, sàn nhà đúng vị trí
- ✅ **Nội thất hợp lý**: Bàn ghế không bay lơ lửng, kích thước phù hợp
- ✅ **Phong cách rõ ràng**: Mỗi style có đặc trưng riêng, dễ phân biệt
- ⚠️ **Hạn chế**: Đôi khi chi tiết nhỏ bị biến dạng, text trong ảnh bị sai

### Giải thích cho người mới (Newbie):
- Giao diện đơn giản, chỉ cần **3 bước**: Upload → Chọn Style → Bấm Generate
- Trong lúc chờ, bạn sẽ thấy thanh tiến trình và **thời gian dự kiến còn lại**
- Kết quả hiện ngay bên cạnh ảnh gốc để **so sánh trước/sau**
- Ảnh kết quả có thể tải về để gửi cho thợ xây/decor tham khảo

### Gợi ý thiết kế:
- Chèn ảnh screenshot UI thực tế (hoặc mockup)
- Grid 2×2 cho 4 kết quả Before/After
- Badge cho mỗi phong cách (màu khác nhau)
- Biểu đồ bar chart nhỏ cho performance metrics
- Nền sáng, layout thoáng đãng
