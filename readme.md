# Comic Translator
![](https://i.imgur.com/VTEKCkr.png)


## Instalation


* Git Clone the project.
* run pip install -r requirements.txt (preferentially on a virtual environment)

Windows
--
* In windows we need to install the tesseract application on `C:\Program Files\Tesseract-OCR\tesseract.exe`


### Running
It's pretty simple. Just type
`python translate_comic.py <lang> <file> <pages>`

* lang = i.e pt
* file = i.e comic.jpg
* page = i.e 1-2

So, following this guide, the script would be:
`python translate_comic.py pt comic.jpg 1-2`

The result file will be saved in the same directory with the name `Page Translated<num>.png`, i.e `Page Translated 1.png`