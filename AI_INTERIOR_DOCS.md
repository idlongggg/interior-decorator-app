# 🏠 AI Interior Decorator: Tài Liệu Tổng Quan & FAQ

Chào mừng bạn đến với dự án **AI Interior Decorator**! Đây là tài liệu tóm tắt về kỹ thuật và bộ câu hỏi giải thích về AI dành cho người mới bắt đầu.

---

## 🚀 1. Review Dự Án (Technical Summary)

Dự án này là một ứng dụng thiết kế nội thất thông minh, kết hợp sức mạnh của **Generative AI** với khả năng kiểm soát kiến trúc chính xác.

### Kiến trúc Kỹ thuật:
- **Frontend**: Next.js 15, Tailwind CSS, HeroUI (UX hiện đại, mượt mà).
- **Backend**: FastAPI (Python), hỗ trợ xử lý đa luồng và tương thích phần cứng (NVIDIA CUDA & Apple MPS).
- **AI Engine**: 
    - **Stable Diffusion 1.5**: "Cỗ máy" tạo ảnh chính.
    - **ControlNet (Canny/Lineart)**: Giữ vững cấu trúc phòng gốc (không làm thay đổi vị trí cửa, tường).
    - **Segformer (ADE20K)**: AI phân tích bề mặt (Sàn, Tường, Trần) để đặt đồ vật hợp lý.
    - **Inpainting Pipeline**: Vẽ đè các nội thất mới mà không ảnh hưởng đến phần còn lại của căn phòng.

### Điểm nổi bật:
1.  **Real-time Progress**: Người dùng theo dõi được từng bước AI đang làm gì thông qua SSE (Server-Sent Events).
2.  **Before/After Comparison**: Công cụ slider giúp so sánh kết quả tức thì.
3.  **Style Logic**: Tự động chuyển đổi từ sở thích người dùng sang các câu lệnh (prompts) kỹ thuật phức tạp.

---

## 🧠 2. AI Glossary (Từ điển AI bình dân)

Để giải thích cho "tay mơ", hãy sử dụng các ẩn dụ sau:

-   **Model (Mô hình)**: Hãy tưởng tượng đây là một "nghệ sĩ" đã học qua hàng triệu bức ảnh nội thất.
-   **Prompt (Lời nhắc)**: Là "kịch bản" bạn gửi cho người nghệ sĩ đó vẽ theo.
-   **ControlNet (Lưới kiểm soát)**: Là "bản vẽ phác thảo" (sketch) của căn phòng cũ, bắt buộc AI phải vẽ đè lên đó chứ không được vẽ linh tinh.
-   **Inpainting (Vẽ đè)**: Giống như việc bạn dùng tẩy xóa một góc ảnh rồi bảo AI vẽ một cái Sofa mới vào đúng vị trí đó.
-   **Inference (Suy luận)**: Quá trình AI đang "vắt óc" suy nghĩ để tạo ra bức ảnh cuối cùng.

---

## ❓ 3. FAQ dành cho "Tay mơ" (Bộ 25 câu hỏi chi tiết)

#### ⭐ Nhóm 1: Câu hỏi Cơ bản về AI
1. **AI là gì trong ứng dụng này?**
   > Nó là trí tuệ nhân tạo có khả năng "học" hàng tỷ hình ảnh để hiểu quy luật về màu sắc, không gian và vật liệu.
2. **AI lấy ảnh của tôi đi đâu không?**
   > Không, ảnh chỉ được dùng để phân tích cấu trúc ngay tại thời điểm bạn yêu cầu thiết kế.
3. **Tại sao kết quả mỗi lần lại hơi khác nhau?**
   > Vì AI có tính ngẫu nhiên sáng tạo (như một họa sĩ mỗi lần vẽ một bức tranh khác nhau dù cùng một chủ đề).
4. **AI có hiểu về kích thước thực của phòng không?**
   > Hiện tại AI chỉ hiểu về "tỷ lệ" và "chiều sâu" qua hình ảnh, chưa đo được chính xác mét vuông thực tế.
5. **Kết quả tạo ra có phải là ảnh chụp thật không?**
   > Không, đó là ảnh được "tổng hợp" từ hàng triệu pixel, mô phỏng lại thực tế với chất lượng như ảnh chụp.

#### ⚙️ Nhóm 2: Cách thức hoạt động & Kỹ thuật
6. **"Seed" là gì mà hay nghe nhắc tới?**
   > Là "mã số may mắn" của bức ảnh. Nếu giữ nguyên mã số này, AI sẽ tạo ra các kết quả có bố cục tương tự nhau.
7. **Tại sao AI biết đâu là Sàn, đâu là Trần?**
   > Nó dùng kỹ thuật "Segmentation" - giống như việc tô màu phân biệt các vùng dựa trên màu sắc và hình khối của ảnh gốc.
8. **Inpainting là gì?**
   > Là kỹ thuật "xóa và vẽ đè". AI xóa một vùng (như chỗ đặt Sofa) và vẽ một vật thể mới vào đó sao cho hòa hợp với ánh sáng xung quanh.
9. **Tại sao đôi khi AI vẽ đồ vật trông hơi lạ?**
   > Có thể do ảnh gốc quá mờ hoặc vùng đó bị lóa sáng, khiến AI không "hiểu" được không gian phía sau nên nó phải "tự chế".
10. **Làm sao AI giữ được cửa sổ cũ không bị thay đổi?**
    > Nhờ ControlNet - nó tạo ra một bản đồ khung xương của căn phòng và bắt AI phải tuân thủ nghiêm ngặt khung xương đó.
11. **Negative Prompt là gì?**
    > Là danh sách "những điều cấm kỵ" (như: mờ, xấu, dị dạng, có người...) để AI tránh vẽ vào ảnh.
12. **AI có biết về ánh sáng tự nhiên không?**
    > Có, nó phân tích hướng sáng từ cửa sổ trong ảnh gốc để tự động đổ bóng cho các đồ vật mới thêm vào.

#### 💡 Nhóm 3: Mẹo để có ảnh đẹp
13. **Tôi nên chụp ảnh phòng như thế nào để AI vẽ đẹp nhất?**
    > Chụp đủ sáng, góc rộng bao quát căn phòng và hạn chế để nhiều đồ vật lộn xộn trên sàn.
14. **Tại sao phong cách Indochine lại ra toàn gỗ tối màu?**
    > Vì AI đã được học rằng đặc trưng của Indochine là sự kết hợp giữa kiến trúc Pháp và vật liệu gỗ, mây tre địa phương.
15. **Tôi có thể yêu cầu vật liệu cụ thể như "Sàn gỗ" hay "Tường đá" không?**
    > Có, bạn có thể nhập yêu cầu này vào mục "Custom Style" để AI ưu tiên sử dụng vật liệu đó.
16. **Nên chọn "Canny" hay "Lineart" cho ControlNet?**
    > Canny bắt chi tiết rất chặt (giống ảnh gốc 99%), còn Lineart thì "mềm mại" hơn, cho phép AI sáng tạo thêm một chút.
17. **Tại sao ảnh tạo ra thỉnh thoảng hơi mờ?**
    > Do giới hạn về bộ nhớ xử lý (Resolution), bạn có thể dùng các công cụ "Upscale" để làm nét ảnh sau khi tạo.

#### 🏡 Nhóm 4: Ứng dụng & Nghề nghiệp
18. **AI có thay thế được kiến trúc sư không?**
    > Không, AI chỉ là công cụ hỗ trợ "phác thảo ý tưởng" nhanh. Kiến trúc sư thực thụ mới là người hiểu về kỹ thuật thi công và công năng sử dụng.
19. **Mọi người có dùng AI này để thi công thật được không?**
    > Hoàn toàn được, đây là nguồn cảm hứng tuyệt vời để khách hàng và thợ thi công hiểu nhau hơn về tông màu và phong cách.
20. **Tại sao thỉnh thoảng AI vẽ thêm cửa sổ mới mà thực tế không có?**
    > Đó là do AI bị "ảo giác" (Hallucination) khi nó thấy một mảng tường trống và nghĩ rằng thêm cửa sổ ở đó sẽ đẹp hơn.
21. **Làm sao để hạn chế AI vẽ linh tinh vào ảnh?**
    > Tăng chỉ số "Control Strength" (Độ mạnh kiểm soát) để ép AI bám sát ảnh gốc hơn.
22. **AI có hiểu về phong thủy không?**
    > Không, AI chỉ quan tâm đến thẩm mỹ hình ảnh. Bạn cần phải là người kiểm tra các yếu tố phong thủy sau khi AI thiết kế.
23. **Tại sao quá trình tạo ảnh lại tốn nhiều điện/điện năng lớn?**
    > Vì các con chip đồ họa (GPU) phải chạy hết công suất để giải các phương trình toán học phức tạp cho mỗi pixel ảnh.
24. **Tôi có thể tạo ảnh thiết kế từ bản vẽ tay không?**
    > Được! Chỉ cần chụp bản vẽ tay của bạn và chọn chế độ "Scribble" hoặc "Lineart", AI sẽ biến nó thành ảnh nội thất thật.
25. **Tương lai của AI trong nội thất sẽ như thế nào?**
    > Nó sẽ ngày càng hiểu sâu về vật liệu thật, có thể xuất ra danh sách đồ nội thất bạn có thể mua ngay trên sàn thương mại điện tử.

---
*Tài liệu này được soạn thảo bởi **Antigravity AI Assistant**.*
