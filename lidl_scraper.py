import easyocr
from paddleocr import PaddleOCR

def start_easyOCR(img):
    reader = easyocr.Reader(['de'])
    result = reader.readtext(img)
    print(result)

def start_paddleOCR(img):
    ocr = PaddleOCR(use_angle_cls=True,lang='de')

    result = ocr.ocr(img, cls=True)

    for line in result[0]:
        bbox, (text, confidence) = line
        print(text, confidence)


if __name__ == "__main__":
    img = 'image.png'
    ''' 
    print("easyOCR interpretation:\n")
    start_easyOCR(img)
    '''
    print("\npaddleOCR interpretation:\n")
    start_paddleOCR(img)