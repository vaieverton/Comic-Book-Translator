# Comic Book Translator

This project is to automatize the translation of all the pages in your comic.

## Installation

Use the package manager [pip3](https://pip.pypa.io/en/stable/) to install the required dependencies.

```bash
pip install opencv-python unidecode
```

```bash
pip install googletrans===3.1.0a0
```

## Usage

```python
# here you set the numbers of pages in your HQ
number_initial_page = 1
number_final_page = 2

# here you defined the name of your HQ less the page number (ex: 'batman-')
# I'm using 'hq-'
orig_img = cv.imread('hq-'+num+'.jpg')
```

```bash
python3 comic_translator_py
```
## Results
![alt text](https://camo.githubusercontent.com/f9841da613b3cd8d5dd220621198e1dcb7a719eec1e3cb97daf457060b7a86bd/68747470733a2f2f692e696d6775722e636f6d2f5654454b436b722e706e67)

![alt text](results/hq-01.jpg)
![alt text](results/hq-01-translated.png)


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)