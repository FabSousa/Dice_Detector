import cv2
import numpy as np
import math
import random

class Dot:
    def __init__(self):
        self.id = 0
        self.cords = []
        self.radius = 0
        self.raw = []
        self.flag = 0

class Dice:
    def __init__(self):
        self.id = 0
        self.sum = 0
        self.dots = []
        self.color = (0, 0, 0)

THRESH_LEVEL = 100
MIN_RADIUS = 8
MIN_DIST = 10
MAX_DIST = 100

ids_colored = []

def main():

    # cap = cv2.VideoCapture('dice_roll.mp4')

    while True:

        # ret, frame = cap.read()

        # if not ret:
        #     print("Camera não identificada")
        #     break
        frame = cv2.imread("dices.jpg")

        # frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)

        img = preprocess(frame)
        all_dots, edges = get_dots(img)

        if all_dots != []:

            dices = get_dices(all_dots)

            draw_dots(frame, dices)

            sum_all = len(all_dots)




        cv2.imshow("cam", frame)
        # cv2.imshow("cam1", img)
        # if edges is not None:
        #     cv2.imshow("cam3", edges)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # cap.release()
    cv2.destroyAllWindows()

def preprocess(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    _, thresh = cv2.threshold(blur, THRESH_LEVEL, 255, cv2.THRESH_BINARY)

    return thresh

def get_dots(img):
    edges = cv2.Canny(img, 9, 150, 3)
    circles=cv2.HoughCircles(edges, cv2.HOUGH_GRADIENT, 1, MIN_DIST, param1=30, param2=15, minRadius=MIN_RADIUS, maxRadius=MIN_RADIUS+5)
    
    if circles is None:
        return [], None

    dots = []
    i = 0
    for circle in circles[0,:]:
        dot = Dot()
        dot.id = i
        dot.cords = [circle[0], circle[1]]
        dot.radius = circle[2]
        dot.raw = circle
        dots.append(dot)
        i = i + 1

    return dots, edges

def draw_dots(img, dices):
    for dice in dices:
        dots = dice.dots
        color = dice.color
        for dot in dots:
            circle = dot.raw
            circle = np.uint16(np.around(circle))
            cv2.circle(img,(circle[0],circle[1]),circle[2],color,2)
            # cv2.putText(img, str(dice.id), (circle[0],circle[1]), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2, cv2.LINE_AA)
  

def get_dices(all_dots):
    dices = []
    i = 0

    print()


    for d1 in all_dots:
        dice = Dice()
        dots = []

        for d2 in all_dots:

            dist = math.dist(d1.cords, d2.cords)

            if dist <= MAX_DIST and d2.flag == 0:
                dots.append(d2)
                d2.flag = 1

        dice.dots = dots
        dice.sum = len(dice.dots)
        
        dice.id = i
        i = i + 1

        set_dice_color(dice)

        dices.append(dice)

    return dices

def set_dice_color(dice):
    for id in ids_colored:
        if dice.id == id[0]:
            dice.color = id[1]
            return
    dice.color = (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255))
    ids_colored.append([dice.id, dice.color])


if __name__ == "__main__":
    main()
