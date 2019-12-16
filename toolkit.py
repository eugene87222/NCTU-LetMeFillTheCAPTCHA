import parse
import train
import os, shutil, configparser
from datetime import datetime

config = configparser.ConfigParser()
config.read('config.ini')

if __name__ == '__main__':
    # Crop each CAPTCHA into five digits
    # for i in range(7000):
    #     parse.parseImage(i, True, False)
    
    # Train the SVM model
    model = train.train(True, 'SVM_v2.sav')
    model = train.loadModel('SVM_v2.sav')

    # Categorize each digits into different folders and re-train the model
    iteration = 0
    while iteration < 10:
        count = 0
        for filename in os.listdir(config['PATH']['PARTITION']):
            if len(filename) != 1:
                img = train.openImage(f"{config['PATH']['PARTITION']}/{filename}")
                ans = model.predict([img])[0]
                shutil.move(f"{config['PATH']['PARTITION']}/{filename}", f"{config['PATH']['PARTITION']}/{ans}/{filename}")
                count += 1
            if count == 2000:
                break
        iteration += 1
        print(f'Iter: {iteration}')
        time = datetime.now().strftime('SVM_%Y-%m-%d_%H%M%S.sav')
        model = train.train(True, time)
        print(f'Re-train: {iteration}')