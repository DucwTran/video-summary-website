# 🎬 AI Video Summarizer

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-green.svg)
![PyTorch](https://img.shields.io/badge/PyTorch-2.0%2B-ee4c2c.svg)

Một hệ thống AI toàn diện giúp tự động phân tích video, tạo bản tóm tắt nội dung chi tiết và trích xuất các video highlight ấn tượng dựa trên sự kết hợp của nhiều mô hình trí tuệ nhân tạo (Whisper, LLM/VLM, Scene Detection). Hệ thống hỗ trợ tốt nội dung tiếng Việt, cung cấp cả giao diện Web trực quan lẫn CLI linh hoạt.

---

## 🌟 Tính Năng Nổi Bật

- **Nhận dạng giọng nói (Speech-to-Text)**: Trích xuất transcript từ video với độ chính xác cao bằng **OpenAI Whisper**.
- **Trích xuất khung hình thông minh**: Áp dụng phát hiện cảnh quay (Scene Detection) kết hợp phân tích mốc thời gian giọng nói để lấy ra các khung hình (frames) mang nhiều ý nghĩa nhất.
- **Mô tả hình ảnh (Frame Captioning)**: Tự động phân tích ngữ cảnh ảnh và tạo caption chi tiết cho từng khung hình.
- **Tóm tắt nội dung mạch lạc**: Kết hợp transcript và caption để tạo ra một bài tóm tắt nội dung bao quát diễn biến chính.
- **Tự động tạo Highlight Video**: Chấm điểm các cảnh quay dựa trên thông tin âm thanh/kịch bản và tự động cắt ghép các phân cảnh nổi bật thành 1 clip ngắn.
- **Giao diện Web FastAPI**: Cho phép người dùng dễ dàng tải video lên không đồng bộ (Async Job), theo dõi trạng thái xử lý theo thời gian thực và xem kết quả trực tiếp.

---

## 🛠️ Trải Nghiệm & Cài Đặt

### Yêu Cầu Hệ Thống

*   **Python:** Môi trường `Python 3.8` trở lên.
*   **FFmpeg:** Bắt buộc phải cài đặt `ffmpeg` trên hệ thống máy chủ và đưa bin vào biến môi trường (`PATH`).
*   **Phần cứng:** Khuyến nghị có GPU (NVIDIA) với CUDA Toolkit để tăng tốc tối đa khi xử lý video và infer các mô hình AI.

### Cài Đặt

1. **Vào thư mục dự án:**

```bash
cd video-summary
```

2. **Chạy môi trường ảo (Khuyến khích thiết lập một Virtual Environment):**

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate
```

3. **Cài đặt các thư viện cần thiết đã được chỉ định:**

```bash
pip install -r requirements.txt
```

---

## 🚀 Hướng Dẫn Sử Dụng

Bạn có thể tương tác với hệ thống theo 2 cách: qua **Giao Diện Web** (đề xuất cho người dùng) hoặc chạy trực tiếp bằng **Command Line (CLI)**.

### Cách 1: Sử Dụng Giao Diện Web (UI FastAPI)

1. Khởi chạy server FastAPI HTTP:
   ```bash
   python app.py
   ```
   *(Lệnh tương đương chạy qua cổng Uvicorn: `uvicorn app:app --host 0.0.0.0 --port 3000`)*

2. Mở trình duyệt và truy cập vào địa chỉ:
   **[http://localhost:3000](http://localhost:3000)**
   
3. **Thao tác:** Tải tệp tin video `.mp4`/`.avi` của bạn lên qua Box giao diện. Tiến trình backend sẽ tự động phân rã vào `data/uploads` và `data/output`. Bạn có thể theo dõi thanh Process cho đến khi màn hình trả lại **Transcript**, đoạn **Tài liệu ngắn gọn** và video Highlight đã được xuất xưởng.

### Cách 2: Sử Dụng CLI nội bộ (Developer)

1. Bạn có thể sử dụng file `main.py` để test nhanh từng luồng pipeline của AI.
2. Kiểm tra/Chỉnh sửa đường dẫn file video đầu vào tại biến `VIDEO_PATH` trong thư mục `config.py`.
3. Chạy lệnh gốc:
   ```bash
   python main.py
   ```
   Ngay sau đó, quá trình xử lý sẽ lần lượt in ra Log các bước. Kết quả sau cùng (âm thanh, caption, transcript, tóm tắt, video highlight) sẽ nằm gọn gàng tại đường dẫn Output được khai báo trong `config.py`.

---

## 📂 Tổ Chức Thư Mục Mã Nguồn

```plaintext
video-summary/
├── models/             # Mã nguồn config, load và giao tiếp với Model (Whisper, Caption, Summary)
├── pipeline/           # Thư mục cốt lõi chứa các Module Pipeline xử lý nối tiếp:
│   ├── extract_audio.py    # Xử lý âm thanh
│   ├── speech_to_text.py   # Chuyển đổi Audio -> Text
│   ├── extract_frames.py   # Trích xuất khung hình
│   ├── caption_frames.py   # Nêu ngữ cảnh Frame
│   ├── summarize.py        # Output nội dung Text Summary
│   ├── scene_detect.py     # Lọc tính năng Scene Detection
│   └── highlight_score.py  # Algorithms chấm ưu tiên và tạo Clip Highlight
├── data/               # Nơi lưu trữ tập tin Video đầu vào và Kết quả (File được tạo runtime)
├── static/             # Chứa CSS, Fonts, Images phục vụ cho UI
├── templates/          # Jinja2 Layout HTML cho giao diện Web
├── app.py              # File chứa cấu hình API endpoint và Flow điều phối chung của App
├── config.py           # Chứa các Hằng số, Path, cấu trúc thư mục Pipeline Config
├── main.py             # Script gỡ lỗi cho Workflow tuần tự của Pipeline CLI
└── requirements.txt    # Danh sách PIP Package
```

---

## 📖 Sơ Lược Quy Trình Thuật Toán (Pipeline Engine)

Cả FastAPI Web và `main.py` đều tuân thủ nguyên tắc chạy Background Async:
1. `Extract Audio`: Ly trích WAV tách biệt từ MP4.
2. `Speech to Text`: Dùng mô hình nhận dạng để có chuỗi hội thoại văn bản, chứa Time-stamps.
3. `Scene & Voice Detection`: Tạo danh sách Phân cảnh có ý nghĩa.
4. `Extract Frames & Captioning`: Gửi mảng ảnh cho Vision AI đánh giá biểu cảm, không gian xung quanh.
5. `Score & Gen Highlight`: Cập nhật bảng xếp hạng phân đoạn cao điểm nhất + Biên tập FFmpeg để chốt clip Highlight.
6. `Generative Text Summarize`: Gọi LLM đọc qua mọi Text đã khai thác để đưa ra đoạn Tóm tắt bài bản cuối cùng!

> **Note:** Đối với các tác vụ yêu cầu bộ nhớ GPU lớn, đảm bảo Model Endpoint hoặc System Resources của bạn cung cấp đủ dung lượng. Nếu bị lỗi VRAM (OOM), hãy cân nhắc thiết lập Model cục bộ dùng Quantization INT4/INT8 hoặc đẩy bớt lên các dịch vụ API inference!
