from paddleocr import PaddleOCR

# Initialize PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang='en')

# Function to extract text
def extract_text(image_path):
    results = ocr.ocr(image_path, cls=True)
    extracted_text = [line[1][0] for res in results for line in res]
    return extracted_text

# Test on a sample business card
text_data = extract_text("uploads/sample_card.jpg")
print("Extracted Text:\n", "\n".join(text_data))