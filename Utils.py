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

def preprocess(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    _, thresh = cv2.threshold(blur, THRESH_LEVEL, 255, cv2.THRESH_BINARY)

    return thresh

def get_dots(img):
    edges = cv2.Canny(img, 9, 150, 3)
    circles=cv2.HoughCircles(edges, cv2.HOUGH_GRADIENT, 1, MIN_DIST, param1=30, param2=15, minRadius=MIN_RADIUS, maxRadius=MIN_RADIUS+5)

    if circles is None:
        print("No dots")
        return None, edges

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

    for d1 in all_dots:
        dice = Dice()
        dots = []

        for d2 in all_dots:

            dist = math.dist(d1.cords, d2.cords)

            if dist <= MAX_DIST and d2.flag == 0:
                dots.append(d2)
                d2.flag = 1

        if len(dots) == 0:
            continue

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

def draw_sum(img, dices):
    total = 0
    i = 0
    y = 35
    x = 10
    for dice in dices:
        cv2.putText(img, str(dice.sum), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, dice.color, 2, cv2.LINE_AA)
        total = total + dice.sum
        x = x + 20
        i = i + 1
        if i < len(dices):
            cv2.putText(img, "+", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
            x = x + 20
        else:
            cv2.putText(img, "=", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
            x = x + 25
            cv2.putText(img, str(total), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)