import cv2
from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

key = 1
cap = cv2.VideoCapture(0)
cascade = cv2.CascadeClassifier('haarcascade_licence_plate_rus_16stages.xml')
while key != 32:
    isRead, image = cap.read()

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    plates = cascade.detectMultiScale(gray)
    for plate in plates:
        x, y, w, h = plate
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 255), 10)
        crop = gray[y:y+50 + h, x:x+50 + w]
        value, mask = cv2.threshold(crop, 100, 255, cv2.THRESH_BINARY_INV)
        cv2.imshow('window_mask', mask)
        text2 = pytesseract.image_to_string(mask, lang='eng')
        print(text2)
        cv2.putText(image, text2, (50, 50), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255), 3)
    cv2.imshow("original", image)
    key = cv2.waitKey(20)