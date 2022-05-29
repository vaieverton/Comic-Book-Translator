import cv2 as cv
import pytesseract
from googletrans import Translator
translator = Translator()
import unidecode

# Aqui você define sua lingua
# "ko" = korean | "en" = english | "ar" = arabic |
#  No nosso caso, "pt" - Português
targeted_lang= "pt"

font_size = 0.5


# função principal para traduzir a HQ
def put_text_page(data, img):
    font = cv.FONT_HERSHEY_SIMPLEX
    for x,b in enumerate(data.splitlines()):
        if x != 0:
           b = b.split()
           if len(b)==12:
                x,y,w,h = int(b[6]), int(b[7]), int(b[8]), int(b[9])
                
                cv.rectangle(img,(x , y), (w+x, h+y), (255,255,255), -1)

                word = b[11]
                
                word_translated = translator.translate(text=word, dest=targeted_lang) # Tradução
                
                word_translated = unidecode.unidecode(word_translated.text) # Formata o texto
                
                cv.putText(img, word_translated, (x+0, y), font, 0.3, (0, 0, 0), 1) # Insere o texto traduzido na tela

# função que extrai o texto da tela com tesseract ocr
def read_text(img):
    data = pytesseract.image_to_data(img)
    print(data)
    return data

def main():
    # Aqui você define quantas paginas tem a HQ
    # Digite o numero da ultima pagina
    
    number_initial_page = 1
    number_final_page = 2

    # loop por cada página e traduza-a..
    while number_initial_page < number_final_page:
        num = str(number_initial_page)
        orig_img = cv.imread('hq-'+num+'.jpg')
        img = cv.cvtColor(orig_img, cv.COLOR_BGR2GRAY)
        img = cv.medianBlur(img, 1)
        img = cv.threshold(img, 0, 255, cv.THRESH_BINARY  + cv.THRESH_OTSU)[1]

        data = read_text(img)
        put_text_page(data, orig_img)


        cv.imwrite('Página Traduzida'+num+'.png', orig_img)
        print("Página "+num+" Traduzida.")

        number_initial_page += 1

    print('HQ traduzida com sucesso!')

main()
