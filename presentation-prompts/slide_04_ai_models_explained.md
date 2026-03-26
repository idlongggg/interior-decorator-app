# Slide 4: AI Models — Giải thích mô hình AI sử dụng

## Prompt cho AI sinh slide

> Hãy tạo slide giải thích **các mô hình AI (AI Models)** được sử dụng trong dự án, bao gồm tại sao chọn chúng. Trình bày dễ hiểu cho người chưa biết gì về AI.

### Nội dung cần có trên slide:

#### 🧠 Model 1: Stable Diffusion v1.5 (by RunwayML)
- **Nó là gì?** Một mô hình AI có khả năng **tạo ra hình ảnh từ mô tả bằng chữ** (text-to-image)
- **Ví dụ đơn giản**: Bạn gõ "Phòng khách phong cách Bắc Âu, nhiều ánh sáng tự nhiên, nội thất gỗ sáng" → AI sẽ vẽ ra một bức ảnh y như thật
- **Tại sao chọn Stable Diffusion 1.5?**
  - ✅ **Mã nguồn mở (Open Source)**: Miễn phí, cộng đồng lớn
  - ✅ **Nhẹ so với SD XL**: Chạy được trên máy tính thông thường (~4GB VRAM)
  - ✅ **Chất lượng tốt**: Hình ảnh realistic, chi tiết nội thất rõ ràng
  - ✅ **Tương thích ControlNet**: Kết hợp hoàn hảo để giữ cấu trúc phòng

#### 🎯 Model 2: ControlNet (Canny Edge Detection)
- **Nó là gì?** Một "plugin" giúp Stable Diffusion **giữ nguyên cấu trúc** của ảnh gốc khi tạo ảnh mới
- **Ví dụ đơn giản**: Nếu không có ControlNet, AI sẽ vẽ một phòng hoàn toàn mới. Nhưng với ControlNet, AI sẽ giữ nguyên vị trí tường, cửa sổ, cửa ra vào của phòng bạn — chỉ thay đổi nội thất
- **Canny Edge là gì?** Là kỹ thuật **phát hiện các đường viền** (cạnh) trong ảnh — giống như khi bạn vẽ phác thảo chỉ bằng nét bút chì
- **Tại sao chọn ControlNet Canny?**
  - ✅ **Giữ layout phòng thật**: Phòng output giống phòng thật về kích thước, góc nhìn
  - ✅ **Kiểm soát được**: AI không tự do sáng tác, mà phải tuân theo cấu trúc gốc
  - ✅ **Cho ra kết quả hợp lý**: Nội thất được đặt đúng vị trí (không bị floating hay đè lên tường)

#### 📐 Scheduler: DPMSolver Multistep
- **Nó là gì?** Thuật toán quyết định **cách AI "vẽ" từng bước** (từ nhiễu → ảnh rõ)
- **Tại sao chọn?** Nhanh hơn và ổn định hơn các scheduler mặc định, hoạt động tốt trên Apple Silicon (Mac)

### Giải thích cho người mới (Newbie):
Hãy tưởng tượng quá trình này giống như:
1. 📸 Bạn đưa ảnh phòng cho AI
2. ✏️ AI dùng ControlNet để "phác thảo" lại cấu trúc phòng (cạnh tường, cửa sổ...)
3. 🎨 Stable Diffusion nhận phác thảo đó + mô tả phong cách → "tô màu" lại thành ảnh mới
4. 🖼️ Kết quả: Căn phòng của bạn nhưng với nội thất hoàn toàn mới!

### Gợi ý thiết kế:
- Chia 2 phần lớn: Stable Diffusion (bên trái) và ControlNet (bên phải)
- Sơ đồ quy trình ở dưới: Input Image → Canny Edge → SD 1.5 + Prompt → Result
- Dùng 4 bước icon minh họa cho phần "Newbie"
- Nền tối gradient (navy → đen) để hình ảnh AI nổi bật
