import requests
import parser_multi
from multiprocessing import Pool


def task(url):
    data = parser_multi.parse_book(url)
    requests.post("http://127.0.0.1:5000/json", json=data)


books = parser_multi.parse_bookstore()
pool = Pool()
lst_url_for_book = []
for i in books:
    for j in i:
        lst_url_for_book.append(j)
print(lst_url_for_book)
pool.map(task, lst_url_for_book)
