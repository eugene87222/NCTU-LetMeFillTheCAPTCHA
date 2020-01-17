import parse
import train
import numpy as np
import cv2, time, sys
from PIL import Image
from io import BytesIO
from getpass import getpass
from selenium import webdriver

def openWebsite():
    driver = webdriver.Firefox()
    driver.get("https://course.nctu.edu.tw/")
    driver.set_window_size(1295, 704)
    return driver

def getScreenshot(driver):
    image = driver.get_screenshot_as_png()
    image = Image.open(BytesIO(image))
    image = np.asarray(image)
    image = cv2.cvtColor(image, cv2.COLOR_BGRA2RGB)
    return image

def getAnswer(model, digits):
    answer = ''
    for digit in digits:
        number = model.predict([digit.ravel()])[0]
        answer += str(number)
    return answer

def login(driver, ID, passwd, CAPTCHA):
    driver.find_element_by_name('ID').click()
    driver.find_element_by_name('ID').clear()
    driver.find_element_by_name('ID').send_keys(ID)
    driver.find_element_by_name('passwd').click()
    driver.find_element_by_name('passwd').clear()
    driver.find_element_by_name('passwd').send_keys(passwd)
    driver.find_element_by_name('qCode').click()
    driver.find_element_by_name('qCode').clear()
    driver.find_element_by_name('qCode').send_keys(CAPTCHA)

    driver.find_element_by_xpath('//center').click()
    driver.find_element_by_name('Action').click()

    time.sleep(1)
    try:
        driver.find_element_by_id('submit').click()
    except:
        pass
    time.sleep(1)
    try:
        driver.find_element_by_xpath("//input[@value='確定']").click()
    except:
        pass

if __name__ == '__main__':
    if len(sys.argv) < 3:
        ID = input('Student ID: ')
        passwd = getpass('Password: ')
    else:
        ID = sys.argv[1]
        passwd = sys.argv[2]

    driver = openWebsite()
    print('Browser opened')

    screenshot = getScreenshot(driver)
    print('Screenshot')

    x, y, w, h = [836, 494, 150, 75]
    CAPTCHA = screenshot[y:y+h, x:x+w]
    # cv2.imshow('', CAPTCHA)
    # cv2.waitKey()

    print('Start parsing')
    digits = parse.parseImage(CAPTCHA, False, False)
    print('Finish parsing')
    
    model = train.loadModel('SVM_v2.sav')
    print(digits[0].shape)
    answer = getAnswer(model, digits)
    print(answer)

    login(driver, ID, passwd, answer)
    print('Log in')