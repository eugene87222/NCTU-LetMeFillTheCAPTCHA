"""
parseImage -> crop the original CAPTCHA into five digits
"""

import numpy as np
import os, cv2, configparser

config = configparser.ConfigParser()
config.read('config.ini')

def show(image, size=None):
    if size:
        cv2.imshow('', cv2.resize(image, size))
    else:
        cv2.imshow('', image)
    cv2.waitKey()

def toGray(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    gray = cv2.threshold(gray, 170, 255, cv2.THRESH_BINARY)[1]
    return gray

def merge(contours):
    contours.sort(key=lambda x: x[0])
    boxes = []
    for i in range(len(contours)):
        x, y, w, h = contours[i]
        box = cv2.rectangle(np.zeros((60, 110)), (x, y), (x+w, y+h), 1, 1)
        boxes.append(box)

    status = np.zeros(len(boxes))
    intermediate = []
    for i in range(len(boxes)):
        if status[i]:
            continue
        if i == len(boxes) - 1:
            status[i] = 1
            intermediate.append(contours[i])
            continue
        intersect = np.logical_and(boxes[i], boxes[i + 1])
        if True in intersect:
            x = min(contours[i][0], contours[i + 1][0])
            y = min(contours[i][1], contours[i + 1][1])
            w = max(contours[i][0] + contours[i][2], contours[i + 1][0] + contours[i + 1][2]) - x
            h = max(contours[i][1] + contours[i][3], contours[i + 1][1] + contours[i + 1][3]) - y
            if w <= 20 and h <= 20:
                status[i] = 1
                status[i + 1] = 1
                intermediate.append((x, y, w, h))
        if status[i] != 1:
            status[i] = 1
            intermediate.append(contours[i])
    
    final_contours = []
    for contour in intermediate:
        if contour[2] >= 15 or contour[3] >= 15:
            final_contours.append(contour)
    
    return final_contours

def eraseSmall(contours):
    valid = []
    for c in contours:
        if c[2] < 12  or c[3] < 12:
            continue
        valid.append(c)
    return valid

def mergeContours(image, contours):
    while 1:
        final_contours = merge(contours)
        final_contours = merge(final_contours)
        final_contours = eraseSmall(final_contours)
        temp = np.array(image)
        for i in range(len(final_contours)):
            x, y, w, h = final_contours[i]
            cv2.rectangle(temp, (x, y), (x+w, y+h), (0, 255, 0), 1)
        show(temp)
        print(final_contours)
        contours = final_contours
        if len(final_contours) <= 5:
            break
    return final_contours

def validContour(contours):
    valid = []
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        if (w < 8 and h < 8) or (w > 25 and h > 25) or w > 40 or h > 40:
            continue
        valid.append((x, y, w, h))
    return valid

def parseImage(file, save2Partition, showContours):
    if save2Partition and not os.path.exists(config['PATH']['PARTITION']):
        os.makedirs(config['PATH']['PARTITION'])

    img = file
    if isinstance(file, str):
        img = cv2.imread(f"{config['PATH']['DOWNLOAD']}/{file}.jpg")
    
    img = cv2.resize(img, (100, 50))
    
    img = cv2.copyMakeBorder(img, 5, 5, 5, 5, cv2.BORDER_CONSTANT, value=(255, 255, 255))
    img_gray = toGray(img)
    img_blur = cv2.medianBlur(img_gray, 3)
    img_blur_gray = cv2.threshold(img_blur, 170, 255, cv2.THRESH_BINARY)[1]
    
    contours, hierarchy = cv2.findContours(img_blur_gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    contours = validContour(contours)
    
    print('merge...')
    contours = mergeContours(img, contours)
    print('merge done...')
    
    img_gray = cv2.cvtColor(img_gray, cv2.COLOR_GRAY2BGR)
    digits = []
    for i in range(len(contours)):
        x, y, w, h = contours[i]
        digit = cv2.resize(img_gray[y:y+h, x:x+w], (28, 28))
        digit = cv2.medianBlur(digit, 5)
        digit = cv2.cvtColor(digit, cv2.COLOR_BGR2GRAY)
        digit = cv2.threshold(digit, 170, 255, cv2.THRESH_BINARY)[1]
        digits.append(digit)
        if save2Partition:
            cv2.imwrite(f"{config['PATH']['PARTITION']}/{file}_{i}.jpg", digit)
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 1)
    
    if showContours:
        show(img)
        for digit in digits:
            show(digit)
    
    return digits
