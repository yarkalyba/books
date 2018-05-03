from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
# from flask_dance.contrib.twitter import make_twitter_blueprint, twitter
import random
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'rybka1'

# pythonanywhere
# app.config[
#     'SQLALCHEMY_DATABASE_URI'] = \
#     "sqlite:////home/yarkarybka/books/example20.db"

# localhost
app.config[
    'SQLALCHEMY_DATABASE_URI'] = \
    "sqlite://///home/yarka/PycharmProjects/books/example4.db"

db = SQLAlchemy(app)

from models import *

db.create_all()


@app.route("/")
def main():
    return '<p>Не дивись, я гола <br>(с) cторінка</p>'


@app.route("/login")
def login():
    return render_template('index.html')


@app.route("/json", methods=['POST'])
def book_json():
    data = json.loads(request.get_json())
    genre = Genre.query.filter_by(name=data["genre"]).first()
    if genre is None:
        genre = Genre(name=data["genre"])
    print("genre", data["genre"])
    author = Author.query.filter_by(name=data["author"]).first()
    if author is None:
        author = Author(name=data["author"])

    db.session.add(genre)
    db.session.add(author)
    db.session.commit()
    book = Books(title=data["name"], photo=data["picture"],
                 description=data["description"],
                 genre_id=genre.id, author_id=author.id)
    db.session.add(book)
    db.session.commit()

    return '{"result": "error"}'


@app.route("/facebook")
def main_page():
    return render_template('facebook.html')


@app.route("/bookpage", methods=['POST', 'GET'])
def book_page():
    books = Books.query.all()
    book = books[random.randint(0, len(books))]
    if request.method == 'POST':
        if 'recommend' in request.form:
            if book.get_rating() == None:
                book.set_rating(0)
            book.set_rating(int(book.get_rating()) + 1)
        elif 'another' in request.form:
            pass
        db.session.commit()
    return render_template("book.html", title=book.get_title(),
                           photo=book.get_photo(),
                           description=book.get_description())


# twitter_blueprint = make_twitter_blueprint(
# api_key='f7dUFCVeAspsUmXBZXGLrNF8e',
#
# api_secret='yAjRQ7CXzoOmPjfoVO2QLOnz40sqhIyU3a43WC4NdZXbLXwJMI')
#
# app.register_blueprint(twitter_blueprint, url_prefix="/twitter_login")


# @app.route("/twitter")
# def twitter_login():
#     if not twitter.authorized:
#         return redirect(url_for("twitter.login"))
#     account_info = twitter.get("account/settings.json")
#
#     if account_info.ok:
#         account_info_json = account_info.json()
#         # можна там свякі штуки робити вже
#         return "<h1> Your twitter name is @{}".format(
#             account_info_json['screen_name'])
#     return '<h1>Request failed!</h1>'


if __name__ == "__main__":
    app.run(debug=True)
