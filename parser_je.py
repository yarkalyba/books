from multiprocessing import Pool
from bs4 import BeautifulSoup
import json
import urllib.request

url = "https://book-ye.com.ua/catalog/khudozhnya-literatura/?PAGEN_1=251"


def parse_category():
    """
    function for moving thought the pages with hole lists of books
    """
    lst = ['https://book-ye.com.ua/catalog/khudozhnya-literatura/?PAGEN_1={}'.format(i) for i in range(1, 19)]
    lst1 = ['https://book-ye.com.ua/catalog/ekonomichna-literatura/?PAGEN_1={}'.format(i) for i in range(1, 18)]
    lst2 = ['https://book-ye.com.ua/catalog/biznes-literatura/?PAGEN_1={}'.format(i) for i in range(1, 12)]
    all_pages = lst + lst1 + lst2
    pool = Pool()
    return pool.map(parse_page, all_pages)

def parse_page(url):
    """
    :param url: url for page with list of books
    function gets the url of a certain book
    """
    request_page = urllib.request.urlopen(url)
    soup = BeautifulSoup(request_page, 'html.parser')
    href_book = soup.find_all('div', class_='col-sm-6 col-md-6 col-lg-4 product product--shadow')
    print(url)
    all_books = ['https://book-ye.com.ua' + i.find('a')['href'] for i in href_book]
    return all_books

def parse_book(url):
    """
    function to parse book page, writes main information into the database
    :param url: url for certain book
    """

    book = urllib.request.urlopen(url)
    soup = BeautifulSoup(book, 'html.parser')
    try:
        name = soup.find('h1', class_='card__title').string.strip()
    except AttributeError:
        name = None
    print(name)
    try:
        author = soup.find('div', class_='col-sm-6 card__info').a.string.strip()
    except AttributeError:
        author = None

    photo_url = soup.find(class_='card__preview preview').img["src"]
    photo = 'https://book-ye.com.ua' + photo_url
    try:
        description = soup.find('p', class_='article__description content__txt').string.strip()
    except AttributeError:
        description = None
    genre = soup.find_all('a', class_='breadcrumbs__elem')[-1].span.text
    book_dict = {'name': name, 'picture': photo, 'author': author, 'description': description, 'genre': genre, 'rating': 0, 'room': 'книгарня є'}
    return json.dumps(book_dict)

