import unidecode
from PIL import Image
from translate import Translator
import cv2 as cv
import pytesseract as ocr
from pre_processing import get_grayscale, thresholding
import numpy as np
import sys
if sys.platform.startswith('win32') or sys.platform.startswith('cygwin'):
    try:
        ocr.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
    except FileNotFoundError as err:
        raise (
            'Se você está utilizando o sistema Windows, favor instalar o Tesseract-OCR',
            err)


class ComicTranslator:
    def __init__(self, target_lang, file, initial_page, final_page):
        self.target_lang = target_lang
        self.file = file
        self.initial_page = initial_page
        self.final_page = final_page

    def put_text_page(self, data, img):
        font = cv.FONT_HERSHEY_COMPLEX_SMALL
        translator = Translator(to_lang=self.target_lang)
        for x, b in enumerate(data.splitlines()):
            if x != 0:
                b = b.split()
            if len(b) == 12:
                x, y, w, h = int(b[6]), int(b[7]), int(b[8]), int(b[9])
                cv.rectangle(img, (x, y), (w+x, h+y), (255, 255, 255), -1)
                word = b[11]
                try:
                    word_translated = translator.translate(
                        text=word)  # tranlation
                    word_translated = unidecode.unidecode(
                        word_translated)  # remove weird shit
                except ValueError as err:
                    print(str(err))
                    continue
                cv.putText(img, word_translated, (x-7, y+20),
                           font, 1, (0, 0, 0), 1)  # put text on the screen
                          
    # function that read the image with pytesseract
    def get_data_from_file(self, img):
        custom_config = r'--oem 3 --psm 4'
        data = ocr.image_to_data(img, lang="eng", config=custom_config)
        print(data)
        return data
        
    def run(self):
        # here you define the number of the comic page with want to start translating
        # and the final page number
        # in my case, page 2 | page 1

        # loop through every page and translate it
        while self.initial_page < self.final_page:
            num = str(self.initial_page)
            img = Image.open(self.file)
            img = get_grayscale(np.float32(img))

            data = self.get_data_from_file(img)
            self.put_text_page(data, img)

            cv.imwrite('Page Translated'+num+'.png', img)
            print("PAGE "+num+" COMPLETED")

            self.initial_page += 1

        print('COMIC-BOOK TRANSLATED SUCCESSFULLY!')
