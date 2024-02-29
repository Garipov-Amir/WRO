import cv2

cap = cv2.VideoCapture(1)

key = 0
keyStop = 32


def detect_zone(image, x_center, y_center):
    image_y, image_x, channel = image.shape
    cv2.line(image, (0, int(image_y / 2)), (image_x, int(image_y / 2)), (255, 255, 0), 2)
    cv2.line(image, (int(image_x / 2), 0), (int(image_x / 2), image_y), (255, 255, 0), 2)

    if x_center < image_x / 2 and y_center < image_y / 2:
        cv2.putText(image, "Zone Two", (30, 30), cv2.FONT_HERSHEY_TRIPLEX, 1, (255, 0, 255), 2)
    elif x_center < image_x / 2 and y_center > image_y / 2:
        cv2.putText(image, "Zone Three", (30, 30), cv2.FONT_HERSHEY_TRIPLEX, 1, (255, 0, 255), 2)
    elif x_center > image_x / 2 and y_center > image_y / 2:
        cv2.putText(image, "Zone Four", (30, 30), cv2.FONT_HERSHEY_TRIPLEX, 1, (255, 0, 255), 2)
    elif x_center > image_x / 2 and y_center < image_y / 2:
        cv2.putText(image, "Zone One", (30, 30), cv2.FONT_HERSHEY_TRIPLEX, 1, (255, 0, 255), 2)

def find_center(image, c):
    x, y, width, height = cv2.boundingRect(c)
    x_center = int(x + (width/2))
    y_center = int(y + (height/2))
    cv2.rectangle(image, (x, y), (x + width, y + height), (0, 255, 0), 2)
    cv2.circle(image, (x_center, y_center), 3, (255, 0, 0), -1)
    detect_zone(image, x_center, y_center)


while key != keyStop:
    isRead, image = cap.read()
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    value_threshold, image_threshold = cv2.threshold(image_gray, 40, 255, cv2.THRESH_BINARY_INV)
    cv2.imshow("Black Highlited", image_threshold)

    image_median_blur = cv2.medianBlur(image_threshold, 15)
    cv2.imshow("Median Blur", image_median_blur)

    contours, service = cv2.findContours(image_median_blur, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(image, contours, -1, (255,0,255), 1)

    for c in contours:
        #x,y, width, height = cv2.boundingRect(c)
        #if width*height > 180:
            #cv2.rectangle(image, (x,y), (x+width, y+height), (0,255,0), 2)
            #cv2.circle(image, (int(x+width/2), int(y+height/2)), 3, (255, 0, 0), -1)
        find_center(image, c)

    cv2.imshow("Contours", image)

    key = cv2.waitKey(20)