from flask import Flask, request, render_template, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import random
import json
import config
import requests
import secrets
from new_models2 import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'rybka1'
app.config['SQLALCHEMY_DATABASE_URI'] = config.DB_PATH

db = SQLAlchemy(app)

db.create_all()


@app.route('/')
def start():
    return render_template('login_user.html')


@app.route('/start', methods=['POST', 'GET'])
def login():
    return render_template('room.html')


@app.route('/rating', methods=['GET'])
def rating_page():
    books = Book.query.all()
    upd = []
    for i in range(len(books)):
        book = books[i]
        upd.append(dict(title=book.title,
                        photo=book.photo,
                        description=book.description,
                        likes=book.likes, dislikes=book.dislikes))
    upd = sorted(upd, key=lambda x: x['likes'] if x['likes'] else 0,
                 reverse=True)
    return render_template("rating.html", items=upd, )


@app.route("/facebook")
def main_page():
    return render_template('facebook.html')


@app.route("/json", methods=['POST'])
def book_json():
    """
    method to add the book to db
    method gets json,
    """

    data = json.loads(request.get_json())
    genre = Genre.query.filter_by(name=data["genre"]).first()
    print("added new book")
    if genre is None:
        genre = Genre(name=data["genre"])
    print("genre: ", data["genre"])
    author = Author.query.filter_by(name=data["author"]).first()
    if author is None:
        author = Author(name=data["author"])
    db.session.add(author)
    db.session.add(genre)
    db.session.commit()
    book = Book(title=data["name"], photo=data["picture"],
                description=data["description"],
                genre_id=genre.id, author_id=author.id,
                rating_from_bookstore=data['rating'])
    db.session.add(book)
    # db.session.commit()
    association = Association(seen=False)
    room = Room.query.filter_by(name=data['room']).first()
    if room is None:
        room = Room(name=data['room'])
    # db.session.add(room)
    association.room = room
    book.rooms.append(association)
    # room.rooms_books.append(book)
    db.session.commit()
    return '<p>Book added</p>'


@app.route('/bookpage1', methods=['POST', 'GET'])
def book_page1():
    if request.method == 'POST':
        book = Book.query.get(int(request.form['book_id']))
        print(book.id)
        if request.form['action'] == 'like':
            if book.likes == None:
                book.set_like(0)
            book.set_like(int(book.likes) + 1)
        else:
            if book.dislikes == None:
                book.set_dislike(0)
            book.set_dislike(int(book.dislikes) + 1)
        db.session.commit()
    room_id = session['room_id']
    try:
        assoc = Association.query.filter_by(room_id=room_id, seen=0).first()
        assoc.seen = 1
        db.session.commit()
    except AttributeError:
        return redirect(url_for('.rating_page'))
    book = Book.query.filter_by(id=assoc.book_id).first()
    book_id = book.id
    print(book_id)
    return render_template("random_book.html", title=book.title,
                           photo=book.photo,
                           description=book.description,
                           book_id=book_id)
    # return render_template("book.html", books=books)


# рандомна книжка з бази даних
# @app.route("/bookpage", methods=['POST', 'GET'])
# def book_page():
#     books = Book.query.all()
#     num_of_book = random.randint(0, len(books))
#     book = books[num_of_book]
#     print('lol')
#     if request.method == 'POST':
#         print(int(request.form['book_id']))
#         book = books[int(request.form['book_id'])]
#         print(book)
#         if 'like' in request.form:
#             if book.get_like() == None:
#                 book.set_like(0)
#             book.set_like(int(book.get_like()) + 1)
#         else:
#             if book.get_dislike() == None:
#                 book.set_dislike(0)
#             book.set_dislike(int(book.get_dislike()) + 1)
#         db.session.commit()
#     return render_template("book.html", title=book.get_title(),
#                            photo=book.get_photo(),
#                            description=book.get_description(),
#                            book_id=num_of_book)


@app.route("/add_book", methods=['POST'])
def add_book():
    room = request.form['book_id']

    title = request.form.get('book_title')
    photo = request.form.get('photo')
    author = request.form.get('author')
    description = request.form.get('description')
    book_dict = {'name': title, 'picture': photo, 'author': author,
                 'description': description, 'genre': None,
                 'rating': None, 'room': room}
    json_book = json.dumps(book_dict)
    requests.post("http://127.0.0.1:5000/json", json=json_book)
    if request.form['action'] == "add":
        return render_template('adding.html', room_id=room)
    else:
        return render_template('end.html', room_id=room)


@app.route('/room', methods=['POST'])
def room():
    if 'create' in request.form:
        room_id = secrets.token_hex(4)
        return render_template('adding.html', room_id=room_id)
    if 'submit' in request.form:
        room_id = request.form.get('room_id')
        session['room_id'] = Room.query.filter_by(name=room_id).first().id
        return redirect(url_for('.book_page1'))


# twitter_blueprint = make_twitter_blueprint(
# api_key='f7dUFCVeAspsUmXBZXGLrNF8e',
#
# api_secret='yAjRQ7CXzoOmPjfoVO2QLOnz40sqhIyU3a43WC4NdZXbLXwJMI')
#
# app.register_blueprint(twitter_blueprint, url_prefix="/twitter_login")


# from flask_dance.contrib.twitter import make_twitter_blueprint, twitter
# @app.route("/twitter")
# def twitter_login():
#     if not twitter.authorized:
#         return redirect(url_for("twitter.login"))
#     account_info = twitter.get("account/settings.json")
#
#     if account_info.ok:
#         account_info_json = account_info.json()
#         return "<h1> Your twitter name is @{}".format(
#             account_info_json['screen_name'])
#     return '<h1>Request failed!</h1>'


if __name__ == "__main__":
    app.run(threaded=True, debug=True)
    # manager.run()
