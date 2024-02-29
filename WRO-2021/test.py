import cv2
import numpy as np
cap = cv2.VideoCapture(1)
while key != 8:
    # subprocess.run('python3 plate_reader.p', shell=True)
    isRead, image = cap.read()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    index=[ 'color','color_name','hex','R','G','B']
    csv = pd.read_csv('colors.csv', names=index, header=None)
    cv2.namedWindow('color detection')
    cv2.setMouseCallback('color detection',draw_function)
    def draw_function(event, x,y,flags,param):
        if event == cv2.EVENT_LBUTTONDBLCLK:
            global b,g,r,xpos,ypos, clicked
            clicked = True
            xpos = x
            ypos = y
            b,g,r = image[y,x]
            b = int(b)
            g = int(g)
            r = int(r)
    def getColorName(R,G,B):
        minimum = 10000
        for i in range(len(csv)):
            d = abs(R- int(csv.loc[i,"R"])) + abs(G-           int(csv.loc[i,"G"]))+ abs(B- int(csv.loc[i,"B"]))
            if(d<=minimum):
                minimum = d
                cname = csv.loc[i,"color_name"]
        return cname

    cv2.imshow("original", image)
    key = cv2.waitKey(1)