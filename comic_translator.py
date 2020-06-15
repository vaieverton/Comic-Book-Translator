import unidecode
from translate import Translator
import cv2 as cv
import pytesseract as ocr
from pre_processing import *
import requests

# Here you define your native language
# "ko" = korean | "en" = english | "ar" = arabic |
# In my case "pt" for portuguese


class ComicTranslator:
    def __init__(self, target_lang, file, initial_page, final_page):
        self.target_lang = target_lang
        self.file = file
        self.initial_page = initial_page
        self.final_page = final_page

    def get_translated_text(self, text_list):
        joined_text = ''.join(text_list)
        translator = Translator(to_lang=self.target_lang)
        try:
            import ipdb
            ipdb.set_trace()
            return translator.translate(
                text=joined_text)
        except ValueError:
            raise ValueError

    def put_text_page(self, data, img):
        font = cv.FONT_HERSHEY_SIMPLEX
        translated_text = self.get_translated_text(data)
        for x, b in enumerate(translated_text.splitlines()):
            import ipdb
            ipdb.set_trace()
            if x != 0:
                b = b.split()
            if len(b) == 12:
                x, y, w, h = int(b[6]), int(b[7]), int(b[8]), int(b[9])
                cv.rectangle(img, (x, y), (w+x, h+y), (255, 255, 255), -1)
                word = b[11]
                cv.putText(img, word, (x+10, y+40),
                           font, 1, (0, 0, 0), 1)  # put text on the screen

    # function that read the image with pytesseract
    def get_data_from_file(self, img):
        custom_config = r'--oem 3 --psm 6'
        data = ocr.image_to_data(img, config=custom_config)
        print(data)
        return data

    def tesseract_it(self, cropped_imgs_list):
        script = ocr.image_to_string(cropped_imgs_list)
        for char in script:
            if char not in ' -QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm,.?!1234567890"":;[]<>()\'':
                script = script.replace(char, '')
        return script

    def find_speech_bubbles(self, image):
        gray_image = get_grayscale(image)
        gray_blurred = get_blur(gray_image)
        image_gray_blur_canny = canny(gray_blurred, 50, 500)
        binary = thresholding(image_gray_blur_canny, 235, 255)
        contours = cv.findContours(
            binary, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        contours = contours[0]
        cropped_image_list = []

        for contour in contours:
            rect = cv.boundingRect(contour)
            [x, y, w, h] = rect

            if w < 500 and w > 60 and h < 500 and h > 25:
                cropped_image = image[y:y+h, x:x+w]
                cropped_image_list.append(cropped_image)
        return cropped_image_list

    def run(self):
        # here you define the number of the comic page with want to start translating
        # and the final page number
        # in my case, page 2 | page 1

        # loop through every page and translate it
        while self.initial_page < self.final_page:
            num = str(self.initial_page)
            img = cv.imread(self.file)
            cropped_image_list = self.find_speech_bubbles(img)

            # data = self.get_data_from_file(img)
            data = []
            for image in cropped_image_list:
                data.append(self.tesseract_it(image))

            # translated_text = self.get_translated_text(images_list)
            self.put_text_page(data, img)

            cv.imwrite('Page Translated'+num+'.png', img)
            print("PAGE "+num+" COMPLETED")

            self.initial_page += 1

        print('COMIC-BOOK TRANSLATED SUCCESSFULLY!')
