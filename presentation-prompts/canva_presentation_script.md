# Presentation Script: AI Interior Decorator (8 Slides for Canva AI)

---

# Slide 1: Giới thiệu dự án — AI Interior Decorator

## Prompt cho AI sinh slide

> Hãy tạo một slide giới thiệu cho bài thuyết trình về dự án **"AI Interior Decorator — Decor nội thất bằng trí tuệ nhân tạo"**.

### Nội dung cần có trên slide:

1. **Tiêu đề chính**: "AI Interior Decorator — Biến đổi không gian sống chỉ trong vài giây"
2. **Tagline / Slogan**: "Upload ảnh phòng → Chọn phong cách → AI sẽ trang trí giúp bạn"
3. **Mô tả ngắn gọn về dự án** (2–3 dòng):
   - Đây là ứng dụng web cho phép người dùng upload ảnh chụp căn phòng thực tế
   - AI sẽ phân tích cấu trúc phòng (tường, sàn, cửa sổ...) và tạo ra hình ảnh phòng mới với nội thất theo phong cách người dùng chọn
   - Các phong cách hỗ trợ: Minimalist, Scandinavian, Indochine, Modern, hoặc Custom
4. **Hình minh họa**: Ảnh Before/After — bên trái là ảnh phòng gốc, bên phải là ảnh phòng đã được AI trang trí

### Giải thích cho người mới (Newbie):
- **AI (Trí tuệ nhân tạo)** là gì? → Đơn giản là máy tính được "dạy" để hiểu hình ảnh và tạo ra hình ảnh mới, giống như một kiến trúc sư ảo
- **Tại sao dự án này hữu ích?** → Giúp mọi người hình dung căn phòng sau khi decor mà không cần thuê designer, tiết kiệm thời gian và chi phí

### Gợi ý thiết kế:
- Nền gradient nhẹ (từ xanh dương sang tím pastel)
- Font chữ hiện đại (Outfit hoặc Inter)
- Icon ngôi sao ✨ hoặc magic wand 🪄 bên cạnh tiêu đề
- Layout: 60% text bên trái, 40% hình minh họa bên phải

---

# Slide 2: Vấn đề & Giải pháp

## Prompt cho AI sinh slide

> Hãy tạo slide trình bày **vấn đề thực tế** mà dự án "AI Interior Decorator" giải quyết, và **giải pháp** mà AI mang lại.

### Nội dung cần có trên slide:

#### 🔴 VẤN ĐỀ (Pain Points):
1. **Chi phí cao**: Thuê interior designer chuyên nghiệp có giá từ 5–50 triệu VNĐ/phòng
2. **Mất thời gian**: Quy trình tư vấn → thiết kế → duyệt → sửa mất hàng tuần đến hàng tháng
3. **Khó hình dung**: Khách hàng không thể tưởng tượng phòng của họ trông như thế nào sau khi decor
4. **Thử nghiệm hạn chế**: Muốn thử 5 phong cách khác nhau? → Phải trả tiền thiết kế 5 lần

#### 🟢 GIẢI PHÁP (Solution):
1. **Miễn phí / chi phí thấp**: Chỉ cần chạy app và upload ảnh
2. **Nhanh chóng**: Kết quả trong 1–3 phút (thay vì hàng tuần)
3. **Trực quan**: Nhìn thấy kết quả ngay lập tức dưới dạng ảnh realistic
4. **Thử không giới hạn**: Chọn Minimalist → không thích? → thử Scandi → thử Indochine → miễn phí!

### Giải thích cho người mới (Newbie):
- Dự án này giống như bạn có một **"designer ảo"** miễn phí 24/7
- Bạn chỉ cần chụp ảnh phòng bằng điện thoại, upload lên, và AI sẽ vẽ lại phòng cho bạn
- AI không thay thế 100% designer — nhưng giúp bạn **hình dung trước** để ra quyết định dễ hơn

### Gợi ý thiết kế:
- Chia slide thành 2 cột: Trái = Vấn đề (nền đỏ nhạt), Phải = Giải pháp (nền xanh nhạt)
- Sử dụng icon cho mỗi bullet point
- Có mũi tên chuyển đổi từ "Vấn đề" → "Giải pháp"

---

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

---

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

---

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

---

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

---

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

---

# Slide 8: Kết luận & Hướng phát triển tương lai

## Prompt cho AI sinh slide

> Hãy tạo slide kết luận cho bài thuyết trình dự án AI Interior Decorator, tổng kết những gì đã đạt được và đề xuất hướng phát triển tương lai.

### Nội dung cần có trên slide:

#### ✅ Tổng kết dự án (What We Built):
- 🏗️ **Full-stack AI Application**: Frontend (Next.js) + Backend (FastAPI) + AI Engine (Stable Diffusion + ControlNet)
- 🎨 **5 phong cách nội thất**: Minimalist, Scandinavian, Indochine, Modern, Custom
- ⚡ **Real-time progress tracking**: Người dùng thấy tiến trình AI đang "vẽ" từng bước
- 🐳 **Docker-ready**: Một lệnh `docker compose up` là chạy được toàn bộ

#### 📚 Bài học rút ra (Key Learnings):

| # | Bài học | Chi tiết |
|---|---|---|
| 1 | **Prompt Engineering rất quan trọng** | Prompt chi tiết = Kết quả tốt. Prompt mơ hồ = Kết quả xấu |
| 2 | **ControlNet là chìa khóa** | Giúp AI không tự do sáng tác mà phải tuân theo cấu trúc phòng thật |
| 3 | **Cross-platform khó hơn tưởng** | Phải xử lý riêng cho CUDA (NVIDIA) vs MPS (Apple) vs CPU |
| 4 | **UX quan trọng không kém AI** | Progress bar, estimated time, glassmorphism → Người dùng không bỏ cuộc khi chờ đợi |

#### 🚀 Hướng phát triển tương lai (Future Roadmap):

**Ngắn hạn (1–3 tháng):**
- 📱 **Responsive mobile design**: Tối ưu cho điện thoại
- 🎨 **Thêm phong cách**: Japanese Zen, Industrial, Bohemian, Luxury Classic
- 🖼️ **Gallery kết quả**: Lưu lại lịch sử các lần generate
- 🔄 **Inpainting**: Chỉ thay đổi một phần phòng (ví dụ: chỉ đổi ghế sofa)

**Trung hạn (3–6 tháng):**
- 🧠 **Upgrade lên SDXL**: Stable Diffusion XL cho chất lượng ảnh cao hơn (1024×1024)
- 🛋️ **Tự chọn nội thất cụ thể**: Upload ảnh ghế mà bạn muốn → AI đặt vào phòng
- 💬 **Chat với AI**: "Thêm một cây xanh góc phải" → AI cập nhật ảnh
- 📐 **3D Room view**: Xoay phòng 360° để xem từ nhiều góc

**Dài hạn (6–12 tháng):**
- 🛒 **Marketplace liên kết**: Gợi ý mua nội thất thật từ ảnh AI tạo ra
- 📊 **AI đánh giá phong thủy**: Phân tích bố trí theo phong thủy
- 🏢 **B2B cho kiến trúc sư / công ty decor**: API trả phí cho doanh nghiệp

#### 🙏 Cảm ơn & Q&A:
- "Cảm ơn các bạn đã lắng nghe!"
- Mời đặt câu hỏi
- Link GitHub / Demo (nếu có)
- Thông tin liên hệ nhóm

### Giải thích cho người mới (Newbie):
- Dự án này chứng minh rằng với **AI mã nguồn mở** (không tốn tiền license), bạn có thể xây dựng ứng dụng thực tế có giá trị
- Công nghệ AI đang phát triển rất nhanh — những gì hôm nay mất 3 phút, tương lai có thể chỉ mất 3 giây
- Đây là điểm khởi đầu — từ prototype này có thể phát triển thành sản phẩm thương mại

### Gợi ý thiết kế:
- Chia slide thành 3 phần: Tổng kết (trên) → Bài học (giữa) → Roadmap (dưới)
- Timeline ngang cho Roadmap (Short → Mid → Long term)
- Kết thúc bằng màn hình "Thank You" với gradient đẹp
- Confetti animation khi chuyển đến slide cuối
- QR code link demo (nếu có)
