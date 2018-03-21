from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
# from flask_dance.contrib.twitter import make_twitter_blueprint, twitter
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'rybka{}'.format(random.randint)

# app.config['SQLALCHEMY_DATABASE_URI'] =
# "sqlite:////home/yarkarybka/books/example19.db"
app.config[
    'SQLALCHEMY_DATABASE_URI'] = \
    "sqlite://///home/yarka/PycharmProjects/books/example19.db"

db = SQLAlchemy(app)

from models import *

db.create_all()


@app.route("/")
def main():
    return '<p>Не дивись, я гола <br>(с) cторінка</p>'


@app.route("/login")
def login():
    return render_template('index.html')


@app.route("/facebook")
def main_page():
    return render_template('facebook.html')


@app.route("/bookpage", methods=['POST', 'GET'])
def book_page():
    books = Books.query.all()
    book = books[random.randint(0, len(books))]
    # book = books[0]
    if request.method == 'POST':
        if 'recommend' in request.form:
            # id = book.get_id()
            # book1 = Books.query.filter_by(id=id)
            if book.get_rating() == None:
                book.set_rating(0)
            book.set_rating(int(book.get_rating()) + 1)
        elif 'another' in request.form:
            pass

    return render_template("book.html", title=book.get_title(),
                           photo=book.get_photo(),
                           description=book.get_description())


@app.route("/api/v0.1/likes", methods=["POST"])
def parse_likes():
    data = request.get_json()
    print(data)
    user = User(fb=data['facebook_id'])
    db.session.add(user)

    event = Event(user_id=data['user_id'], book_id=data['book_id'],
                  reaction=data['reaction'])
    db.session.add(event)
    db.session.commit()

    return '{"result": "error"}'


@app.route("/events")
def event():
    events = Event.query.all()
    return '<br>'.join([str(event) for event in events])


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
