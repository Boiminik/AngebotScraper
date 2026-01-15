import easyocr
reader = easyocr.Reader(['de'])

result = reader.readtext('image.png')
print(result)