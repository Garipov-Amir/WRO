import cv2
import numpy

def read_values(filename):
    f = open(filename, 'r')
    data = f.read()
    HSV_split = data.split(', ')
    print(HSV_split)
    for i in range(6):
        HSV_split[i] = int(HSV_split[i])
    f.close()
    return HSV_split

cap = cv2.VideoCapture(1)
h_up, h_down, s_up, s_down, v_up, v_down = read_values('HSV_red.txt')