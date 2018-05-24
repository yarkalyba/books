from multiprocessing import Pool
from bs4 import BeautifulSoup
from models import *
import json


def parse_bookstore():
    """
    function for moving thought the pages with hole lists of books
    """
    lst = ["https://www.bookclub.ua/ukr/catalog/books/?gc=100&listmode=2" \
           "&i={}".format(i) for i in range(0, 2300, 100)]
    pool = Pool()
    return pool.map(parse_page, lst)


def parse_page(url):
    """
    :param url: url for page with list of books
    function gets the url of a certain book
    """
    print(url)
    import urllib.request
    r = urllib.request.urlopen(url)
    soup = BeautifulSoup(r, "html.parser")
    finn = soup.find_all("div", class_="mainGoodContent")
    lst = []
    for fin in finn:
        lst.append("http://bookclub.ua" + fin.find("a")["href"])
    return lst


def parse_book(url):
    """
    function to parse book page, writes main information into the database
    :param url: url for certain book
    """

    import urllib.request
    r = urllib.request.urlopen(url)
    soup = BeautifulSoup(r, 'html.parser')
    name = soup.find('article', class_='prd-m-info-block').h1.string.strip()
    picture = soup.find('div', class_='zooming').a["href"]
    picture_add = "http://bookclub.ua" + picture

    author_div = soup.find('div', class_='prd-author-name').a

    if author_div is None:
        author_add = None
    else:
        author_add = author_div.get_text()

    try:
        rating_from_bookstore = soup.find(id='reitingstar')['alt']
    except TypeError:
        rating_from_bookstore = None

    d = soup.find('div', class_='proddesc')
    description = ' '.join(d.stripped_strings)
    genre_add = soup.find_all('div', class_='prodchap')[-1].a.get_text()

    genre = Genre.query.filter_by(name=genre_add).first()
    if genre is None:
        genre = Genre(name=genre_add)
    author = Author.query.filter_by(name=author_add).first()
    if author is None:
        author = Author(name=author_add)
    print(rating_from_bookstore)
    book_dict = {'name': name, 'picture': picture_add, 'author': author_add,
                 'description': description, 'genre': genre_add,
                 'rating': rating_from_bookstore}
    json_book = json.dumps(book_dict)
    return json_book
