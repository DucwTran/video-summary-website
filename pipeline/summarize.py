import json
from models.summary_model import load_summary_model, generate_summary
from pipeline.transcript_summary import summarize_transcript


print("Loading summary model...")
model, tokenizer = load_summary_model()


def summarize(transcript_path, captions_path, output_path):

    print("Reading transcript...")

    with open(transcript_path, encoding="utf-8") as f:
        transcript = f.read()

    print("Reading captions...")

    with open(captions_path, encoding="utf-8") as f:
        captions = json.load(f)

    # Reduce caption tokens and remove "Frame N:" so the model doesn't see them at all
    caption_text = "\n".join(
        [
            f"- {c['caption']}"
            for i, c in enumerate(captions)
            if i % 5 == 0
        ]
    )

    # STEP 1: summarize transcript
    print("Summarizing transcript...")
    short_transcript = summarize_transcript(model, tokenizer, transcript)

    # STEP 2: generate story
    print("Generating story...")

    prompt = f"""<|im_start|>system
Bạn là một nhà văn chuyên nghiệp đang viết truyện ngắn dựa trên tư liệu.

Nhiệm vụ:
Viết CHÍNH XÁC MỘT ĐOẠN VĂN duy nhất kể lại câu chuyện dựa trên lời thoại và hình ảnh.

Quy tắc BẮT BUỘC (Nếu vi phạm sẽ bị phạt):
1. KHÔNG BAO GIỜ dùng từ "ảnh", "khung hình", "video", "nhân vật", "frame".
2. KHÔNG BAO GIỜ chào hỏi hay mở bài (Ví dụ: cấm dùng "Chào mọi người", "Dưới đây là...").
3. KHÔNG BAO GIỜ có định dạng Markdown, danh sách, hay gạch đầu dòng trong câu trả lời.
4. KHÔNG BAO GIỜ giải thích những gì bạn đang làm.
5. Chỉ viết đúng 1 đoạn văn (khoảng 5-8 câu), không xuống dòng.
6. Câu cuối cùng kết lại bằng một bài học ý nghĩa.

--- VÍ DỤ MẪU ---
Lời thoại:
Người cha làm nghề nhặt rác có một người con trai. Cậu con trai luôn xấu hổ vì vẻ ngoài của cha và hay gắt gỏng với ông. Sau khi người cha mất đi vì một tai nạn, người con tìm thấy một cuốn sổ tiết kiệm cũ kỹ. Đó là số tiền cha đã chắt chiu mười năm qua để cậu học đại học. Cậu con trai khóc nức nở và nhận ra tình yêu vĩ đại của cha.

Các hành động diễn ra:
- Người cha đang nhặt rác trên phố bên cạnh chiếc xe đẩy.
- Cậu con trai đi ngang qua cùng bạn bè, quay mặt đi chỗ khác.
- Người cha đang làm việc thì bị ngã gục xuống đường.
- Cậu con trai ngồi trên giường, cầm một cuốn sổ cũ kỹ và khóc.
- Người con trai đứng trước một ngôi mộ, cúi đầu hối hận.

Truyện:
Câu chuyện xoay quanh một người con trai luôn cảm thấy xấu hổ vì vẻ ngoài khắc khổ và đôi bàn tay thô ráp của người cha làm nghề nhặt rác. Anh luôn tìm cách né tránh ông trước mặt bạn bè và không ít lần buông những lời gắt gỏng, coi sự chăm sóc của cha là phiền phức. Chỉ đến khi người cha qua đời vì một tai nạn bất ngờ, anh mới tìm thấy một cuốn sổ tiết kiệm cũ kỹ giấu dưới gối, ghi chép tỉ mỉ từng đồng tiền lẻ ông chắt chiu suốt chục năm qua để dành cho anh học đại học. Cầm cuốn sổ trên tay, người con quỵ ngã trong nước mắt, nhận ra rằng đằng sau vẻ ngoài mà anh từng chối bỏ là một tình yêu thương vô điều kiện và vĩ đại. Đoạn phim kết thúc bằng hình ảnh anh đứng trước mộ cha, gửi đi một lời xin lỗi mà ông không bao giờ còn nghe thấy được nữa, để lại bài học sâu sắc cho người xem về sự trân trọng người thân khi họ còn ở bên.
--- HẾT VÍ DỤ ---<|im_end|>
<|im_start|>user
Lời thoại:
{short_transcript}

Các hành động diễn ra:
{caption_text}

Viết ngay câu chuyện của bạn:<|im_end|>
<|im_start|>assistant
Truyện:"""

    summary = generate_summary(model, tokenizer, prompt)

    # Bỏ chữ Truyện: ở đầu nếu có
    if summary.startswith("Truyện:"):
        summary = summary[7:].strip()
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(summary)

    print("Summary saved to:", output_path)

    return summary
