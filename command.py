import argparse
from comic_translator import ComicTranslator

parser = argparse.ArgumentParser(
    description='Convert page to specific language')
parser.add_argument('target_lang', metavar='-l', type=str,
                    help='Choose language. Ex.: pt')

parser.add_argument('file', metavar='-f', type=str, 
                    help='Type filename. Ex.: page.jpeg')

parser.add_argument('page_range', metavar='-r', type=str,
                    help='Specify range, divided by hifen. Ex.: 1-10')


arguments = parser.parse_args()


def get_page_numbers(page_range):
    return page_range.split('-')


initial_page, final_page = get_page_numbers(arguments.page_range)

comic = ComicTranslator(arguments.target_lang, arguments.file, int(initial_page), int(final_page))

comic.run()
