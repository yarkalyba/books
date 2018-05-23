import requests
import parser_je
from multiprocessing import Pool

def task(url):
    data = parser_je.parse_book(url)
    print(url)
    print(data)
    requests.post("http://127.0.0.1:5000/json", json=data)

books = parser_je.parse_category()
pool = Pool()
lst_url_for_book = []
for i in books:
    for j in i:
        lst_url_for_book.append(j)
print(lst_url_for_book)
pool.map(task, lst_url_for_book)
