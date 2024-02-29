import cv2

cap = cv2.VideoCapture('robot.mp4')

for number in range(200):
    isRead,image = cap.read()
    cv2.circle(image, (480,270), 50, (255,0,0), -1)
    cv2.line(image, (480, 0), (480, 540), (0, 255, 0), 3)
    cv2.rectangle(image, (10,10), (950, 520), (255,0, 255), 4)
    cv2.putText(image, "Video Drawing", (10,270), cv2.FONT_HERSHEY_TRIPLEX, 3, (255,255,0), 2)
    cv2.imshow('window', image)
    print(image.shape)
    cv2.waitKey(16)
cap.release()

