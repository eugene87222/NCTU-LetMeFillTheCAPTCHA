"""
openImage -> open image with given file name

train -> train a SVC model with the pictures under the directory specified in `config.ini`

loadModel -> load the pickle file
"""

import numpy as np
from sklearn import svm
import os, cv2, pickle, configparser

config = configparser.ConfigParser()
config.read('config.ini')

def openImage(filename):
    img = cv2.imread(filename)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = img.ravel()
    return img

def train(saveModel, modelName=''):
    X = []
    y = []
    for i in range(3, 10):
        for filename in os.listdir(f"{config['PATH']['TRAINING']}/{i}"):
            img = openImage(f"{config['PATH']['TRAINING']}/{i}/{filename}")
            X.append(img)
            y.append(i)
    model = svm.SVC()
    model.fit(X, y)
    
    if saveModel:
        pickle.dump(model, open(modelName, 'wb'))
    
    return model

def loadModel(modelName):
    model = pickle.load(open(modelName, 'rb'))
    return model
