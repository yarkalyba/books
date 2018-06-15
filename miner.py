# File: miner.py
# parsing the internet bookstore using BeautifulSoup
from bs4 import BeautifulSoup
from models import *


def parse_bookstore():
    """
    function for moving thought the pages with hole lists of books
    """
    for i in range(0, 2300, 100):
        url = "https://www.bookclub.ua/ukr/catalog/books/?gc=100&listmode=2" \
              "&i={}".format(
            i)
        parse_page(url)


def parse_page(url):
    """
    :param url: url for page with list of books
    function gets the url of a certain book
    """
    lst = []
    import urllib.request
    r = urllib.request.urlopen(url)
    soup = BeautifulSoup(r, "html.parser")
    finn = soup.find_all("div", class_="mainGoodContent")
    for fin in finn:
        book_url = "http://bookclub.ua" + fin.find("a")["href"]
        parse_book(book_url)


def parse_book(url):
    """
    function to parse book page, writes main information into the database
    :param url: url for certain book
    """

    import urllib.request
    r = urllib.request.urlopen(url)
    soup = BeautifulSoup(r, "html.parser")
    print(url)
    name = soup.find('article', class_='prd-m-info-block').h1.string.strip()
    picture = soup.find('div', class_='zooming').a["href"]
    picture_add = "http://bookclub.ua" + picture

    rating_from_bookstore = soup.find(class_='prd_reit_stars').img['alt']

    author_div = soup.find('div', class_='prd-author-name').a

    if author_div is None:
        author_add = None
    else:
        author_add = author_div.get_text()

    d = soup.find('div', class_='proddesc')
    description = ' '.join(d.stripped_strings)
    genre_add = soup.find_all('div', class_='prodchap')[-1].a.get_text()

    print(author_add)
    genre = Genre.query.filter_by(name=genre_add).first()
    if genre is None:
        genre = Genre(name=genre_add)
    author = Author.query.filter_by(name=author_add).first()
    if author is None:
        author = Author(name=author_add)



    db.session.add(genre)
    db.session.add(author)
    db.session.commit()
    book = Book(title=name, photo=picture_add, description=description,
                 rating_from_bookstore=rating_from_bookstore,
    genre_id = genre.id, author_id = author.id)
    db.session.add(book)
    db.session.commit()
