# Let me help you to fill the CAPTCHA

```
./
├── Download/
│   ├── Partition/
│   │   ├── 3/
|   |   |   └── *.jpg
|   |   ├── 4/
|   |   |   └── *.jpg
|   |   ├── 5/
|   |   |   └── *.jpg
|   |   ├── 6/
|   |   |   └── *.jpg
|   |   ├── 7/
|   |   |   └── *.jpg
|   |   ├── 8/
|   |   |   └── *.jpg
|   |   └── 9/
|   |       └── *.jpg
│   └── *.jpg (origin CAPTCHA image)
├── config.ini
├── login.py
├── parse.py
├── SVM_v1.sav
├── SVM_v2.sav
├── toolkit.py
└── train.py
```
> Since size of `Download` folder is a little big, the zipped `Donwload` can be downloaded [here](https://drive.google.com/open?id=1hnARadcYP3_0T-LRBHVdKUnI8JBnC4kd)

## Requirement

- python3 >= 3.6.4
- `pip3 install numpy opencv-python scikit-learn selenium Pillow`
    - Remember to download the selenium webdriver [here](https://selenium.dev/documentation/en/webdriver/driver_requirements/#quick-reference)

## Usage
```
python3 login.py
```
