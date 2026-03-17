from models.summary_model import generate_summary


def summarize_transcript(model, tokenizer, transcript):

    prompt = f"""<|im_start|>system
Bạn là biên tập viên giúp tóm tắt lời thoại của một video.

Quy tắc:
- Chỉ sử dụng thông tin có trong transcript.
- Không thêm chi tiết mới, không suy đoán.
- TRỰC TIẾP tóm tắt, KHÔNG dùng lời chào hay mở bài rườm rà.

Yêu cầu:
- Tóm tắt nội dung chính thành 1 đoạn văn duy nhất.
- Khoảng 5–7 câu.
- Giữ đúng trình tự sự kiện.<|im_end|>
<|im_start|>user
Transcript:

{transcript}

Hãy tóm tắt nội dung lời thoại ngay lập tức mà không có lời dẫn.<|im_end|>
<|im_start|>assistant
"""

    summary = generate_summary(model, tokenizer, prompt)

    return summary
