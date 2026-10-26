# # import pdfplumber
# # import logging

# # # Configure logging first
# # logging.basicConfig(
# #     filename="invoice_extractor.log",
# #     level=logging.INFO,
# #     format="%(asctime)s - %(levelname)s - %(message)s"
# # )

# # # PDF extraction
# # with pdfplumber.open("sample_document/invoice_08.pdf") as pdf:
# #     for page in pdf.pages:
# #         text = page.extract_text() or ""
# #         char_count = len(text.strip())

# #         print(f"char_count: {char_count}")

# #         if char_count > 100:
# #             print("PDF text extraction successful")
# #             logging.info("PDF text extraction successful")
# #         else:
# #             print("PDF needs OCR")
# #             logging.warning("OCR fallback needed for invoice_08.pdf")

# # logging.info("PDF processing completed")


# from PIL import Image
# import pytesseract  
# from pytesseract import Output


# image = Image.open("sample_document/invoice_02.png")

# data = pytesseract.image_to_data(
#     image,
#     output_type=pytesseract.Output.DICT
#     )

# confidences = []

# for confidence in data['conf']:
#     if confidence >= 0:  
#         confidences.append(float(confidence))

# if confidences:
#     print(f"No. of valid confidence values: {len(confidences)}")
#     mean_confidence = sum(confidences) / len(confidences)
#     print(f"Mean OCR confidence: {mean_confidence:.2f}")

# else:
#     print("No valid confidence values found.")

# for i in range(5):
#     text = data['text'][i]
#     conf = data['conf'][i]
#     print(f"Text: {text}, Confidence: {conf}")

# print("First five words:", data['text'][:5])

# import cv2

# image = cv2.imread("sample_document/invoice_07.png")

# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# threshold = cv2.adaptiveThreshold(
#     gray,
#     255,
#     cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
#     cv2.THRESH_BINARY,
#     31,
#     11
# )

# cv2.imwrite(
#     "intermediate_images/invoice_07_threshold.png",
#     threshold
# )

import cv2

image = cv2.imread("sample_document/invoice_02.png")

denoised = cv2.fastNlMeansDenoising(
    image,
    None,
    10,
    7,
    21
)

cv2.imwrite(
    "intermediate_images/invoice_02_denoised.png",
    denoised
)