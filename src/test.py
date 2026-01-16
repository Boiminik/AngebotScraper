from paddleocr import PaddleOCR

ocr = PaddleOCR(use_angle_cls=True, lang='de')

result = ocr.predict("image.png")
print(result)
