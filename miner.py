import asyncio
from bs4 import BeautifulSoup
from models import *
from app import db


async def parse_bookstore():
    for i in range(0, 2300, 100):
        url = "https://www.bookclub.ua/ukr/catalog/books/?gc=100&listmode=2" \
              "&i={}".format(
            i)
        await parse_page(url)


async def parse_page(url):
    lst = []
    import urllib.request
    r = urllib.request.urlopen(url)
    soup = BeautifulSoup(r, "html.parser")
    finn = soup.find_all("div", class_="mainGoodContent")
    lst = list(map(lambda i: "http://bookclub.ua" + i.find("a")["href"], finn))
    with open("urls.txt", "a") as f:
        for i in lst:
            f.write(i)

        await parse_book(i)


async def parse_book(url):
    import urllib.request
    r = urllib.request.urlopen(url)
    soup = BeautifulSoup(r, "html.parser")

    name = soup.find('article', class_='prd-m-info-block').h1.string.strip()
    picture = soup.find('div', class_='zooming').a["href"]
    picture_add = "http://bookclub.ua" + picture

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
    book = Books(title=name, photo=picture_add, description=description,
                 genre_id=genre.id, author_id=author.id)
    db.session.add(book)
    db.session.commit()


loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.run_until_complete(parse_bookstore())
loop.close()
