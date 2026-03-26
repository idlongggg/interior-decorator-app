# Slide 6: Prompt Engineering — Nghệ thuật ra lệnh cho AI

## Prompt cho AI sinh slide

> Hãy tạo slide giải thích **Prompt Engineering** — cách dự án viết "lệnh" (prompt) cho AI để tạo ra hình ảnh chính xác theo từng phong cách nội thất.

### Nội dung cần có trên slide:

#### 🎯 Prompt Engineering là gì?
- Là kỹ thuật **viết mô tả chi tiết** để AI hiểu chính xác bạn muốn gì
- Giống như bạn đang **mô tả căn phòng mơ ước** cho một họa sĩ bị bịt mắt — càng chi tiết, kết quả càng đẹp

#### 📝 Ví dụ Prompt thực tế trong dự án:

**Phong cách Minimalist:**
> "A high-resolution photo of a modern room transformed with a minimalist interior design. The room maintains its original spatial structure and camera angle. The background walls are painted a clean, bright white. Furnishings are extremely sparse and functional. In the center, there is a very simple, low-profile dining table..."

**Phong cách Indochine:**
> "A high-resolution photo of the identical room with a rich, decorative Indochine interior design. The space features dark, carved wood and rattan furniture. A large, dark mahogany dining table..."

#### 🔑 Các yếu tố quan trọng trong prompt:

| Yếu tố | Mục đích | Ví dụ |
|---|---|---|
| **Chất lượng ảnh** | AI ưu tiên tạo ảnh sắc nét | "A high-resolution photo..." |
| **Giữ cấu trúc** | Phòng mới giống phòng gốc | "maintains its original spatial structure and camera angle" |
| **Vật liệu cụ thể** | AI biết dùng chất liệu gì | "dark mahogany", "light-colored pine", "rattan webbing" |
| **Nội thất chi tiết** | Mô tả từng đồ vật | "low-profile dining table", "four chairs with curved wooden backs" |
| **Ánh sáng** | Tạo bầu không khí đúng | "Natural daylight", "warm and diffused" |
| **Photography style** | Kết quả chuyên nghiệp | "Professional architectural photography" |

#### ❌ Negative Prompt (Những gì AI KHÔNG được vẽ):
```
"low quality, blurry, distorted, ugly, messy, person, text, watermark, deformed, bad anatomy"
```
→ Đảm bảo AI không tạo ra ảnh mờ, xấu, có chữ hoặc có người

#### ⚙️ Các tham số kỹ thuật theo phong cách:

| Phong cách | Guidance Scale | Inference Steps | Ý nghĩa |
|---|---|---|---|
| Minimalist | 7.5 | 35 | Guidance thấp hơn → AI tự do hơn → phù hợp style đơn giản |
| Scandinavian | 8.5 | 40 | Cân bằng giữa sáng tạo và kiểm soát |
| Indochine | 9.0 | 50 | Guidance cao → AI bám sát prompt → nhiều chi tiết phức tạp |
| Modern | 8.5 | 45 | Cân bằng, chi tiết vừa phải |

### Giải thích cho người mới (Newbie):
- **Guidance Scale** = "Mức độ nghe lời" — số càng cao, AI càng làm đúng theo mô tả, nhưng có thể kém tự nhiên
- **Inference Steps** = "Số lượt tô màu" — càng nhiều bước, ảnh càng chi tiết nhưng chạy càng lâu
- **Negative Prompt** = "Danh sách cấm" — những thứ bạn KHÔNG muốn xuất hiện trong ảnh

### Gợi ý thiết kế:
- Hiển thị 1 prompt mẫu với highlight màu cho từng yếu tố (chất liệu=vàng, ánh sáng=cam, vật liệu=xanh)
- Bảng so sánh tham số các phong cách
- Sử dụng code block cho negative prompt
- Icon 🎯 cho precision, 🎨 cho creativity
