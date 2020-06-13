import unidecode
from googletrans import Translator
import cv2 as cv
import pytesseract
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
translator = Translator()

# Here you define your native language
# "ko" = korean | "en" = english | "ar" = arabic |
# In my case "pt" for portuguese

# main function to perform the translation


class ComicTranslator:
    def __init__(self, target_lang, file, initial_page, final_page):
        self.target_lang = target_lang
        self.file = file
        self.initial_page = initial_page
        self.final_page = final_page

    def put_text_page(self, data, img):
        font = cv.FONT_HERSHEY_SIMPLEX
        for x, b in enumerate(data.splitlines()):
            if x != 0:
                b = b.split()
            if len(b) == 12:
                x, y, w, h = int(b[6]), int(b[7]), int(b[8]), int(b[9])
                cv.rectangle(img, (x, y), (w+x, h+y), (255, 255, 255), -1)
                word = b[11]
                word_translated = translator.translate(
                    text=word, dest=self.targeted_lang)  # tranlation
                word_translated = unidecode.unidecode(
                    word_translated.text)  # remove weird shit
                cv.putText(img, word_translated, (x+10, y+40),
                           font, 1, (0, 0, 0), 1)  # put text on the screen

    # function that read the image with pytesseract
    def get_data_from_file(self, img):
        data = pytesseract.image_to_data(img)
        print(data)
        return data

    def run(self):
        # here you define the number of the comic page with want to start translating
        # and the final page number
        # in my case, page 2 | page 10
        number_initial_page = 2
        number_final_page = 3

        # loop through every page and translate it
        while number_initial_page < number_final_page:
            num = str(number_initial_page)
            img = cv.imread('Dexter Down Under 002-00'+num+'.jpg')
            img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

            data = self.get_data_from_file(img)
            self.put_text_page(data, img)

            cv.imwrite('Page Translated'+num+'.png', img)
            print("PAGE "+num+" COMPLETED")

            number_initial_page += 1

        print('COMIC-BOOK TRANSLATED SUCCESSFULLY!')
