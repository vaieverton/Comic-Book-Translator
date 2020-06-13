import cv2 as cv
import pytesseract
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
from googletrans import Translator
translator = Translator()
import unidecode

# Here you define your native language
# "ko" = korean | "en" = english | "ar" = arabic |
# In my case "pt" for portuguese
targeted_lang= "pt"

# main function to perform the translation


def put_text_page(data, img):
    font = cv.FONT_HERSHEY_SIMPLEX
    for x,b in enumerate(data.splitlines()):
        if x != 0:
           b = b.split()
           if len(b)==12:
                x,y,w,h = int(b[6]), int(b[7]), int(b[8]), int(b[9])
                cv.rectangle(img,(x , y), (w+x, h+y), (255,255,255), -1)
                word = b[11]
                word_translated = translator.translate(text=word, dest=targeted_lang) # tranlation
                word_translated = unidecode.unidecode(word_translated.text) # remove weird shit
                cv.putText(img, word_translated, (x+10, y+40), font, 1, (0, 0, 0), 1) # put text on the screen

# function that read the image with pytesseract
def read_text(img):
    data = pytesseract.image_to_data(img)
    print(data)
    return data

def main():
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

        data = read_text(img)
        put_text_page(data, img)

        cv.imwrite('Page Translated'+num+'.png', img)
        print("PAGE "+num+" COMPLETED")

        number_initial_page += 1

    print('COMIC-BOOK TRANSLATED SUCCESSFULLY!')

main()
