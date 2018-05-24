from flask import Flask, request, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
# from flask_dance.contrib.twitter import make_twitter_blueprint, twitter
import random
import json
import config
import requests
import uuid


app = Flask(__name__)
app.config['SECRET_KEY'] = 'rybka1'
app.config['SQLALCHEMY_DATABASE_URI'] = config.DB_PATH

db = SQLAlchemy(app)
# migrate = Migrate(app, db)

# manager = Manager(app)
# manager.add_command('db', MigrateCommand)


from models import *

db.create_all()


@app.route("/policy")
def policy():
    return '<p>Policy</p>'


@app.route("/")
def login():
    return render_template('room.html')


@app.route("/json", methods=['POST'])
def book_json():
    print("added new book")
    data = json.loads(request.get_json())
    print(data["genre"])
    genre = Genre.query.filter_by(name=data["genre"]).first()
    if genre is None:
        genre = Genre(name=data["genre"])
    print("genre", data["genre"])
    author = Author.query.filter_by(name=data["author"]).first()
    if author is None:
        author = Author(name=data["author"])
    room = Room.query.filter_by(name=data['room']).first()
    if room is None:
        room = Room(name=data['room'])
    db.session.add(genre)
    db.session.add(author)
    db.session.commit()
    book = Books(title=data["name"], photo=data["picture"],
                 description=data["description"],
                 genre_id=genre.id, author_id=author.id,
                 rating_from_bookstore=data['rating'])
    db.session.add(book)
    db.session.commit()
    db.session.add(room)
    room.rooms_books.append(book)
    db.session.commit()
    return '<p>Book added</p>'


@app.route("/facebook")
def main_page():
    return render_template('facebook.html')


@app.route('/rating', methods=['GET'])
def rating_page():
    books = Books.query.all()
    num_of_book = random.randint(0, len(books))
    upd = []
    for i in range(0,num_of_book):
        book = books[i]
        upd.append(dict(title=book.get_title(),
                           photo=book.get_photo(),
                           description=book.get_description(),
                           likes=book.get_like(), dislikes=book.get_dislike() ))
    upd = sorted(upd, key=lambda x: x['likes'] if x['likes'] else 0, reverse = True)
    return render_template("rating.html", items = upd,)



@app.route('/bookpage1', methods=['POST', 'GET'])
def book_page1():
    # name = request.args['room_id']
    name = session['room_id']
    print(name)
    books = Books.query.filter(Books.rooms_with_books.any(name=name)).all()
    book = books.pop()

    if request.method == 'POST':
        # print(int(request.form['book_id']))
        book = Books.query.get(int(request.form['book_id']))
        # book = books[int(request.form['book_id'])]
        print(book)
        if 'like' in request.form:
            if book.get_like() == None:
                book.set_like(0)
            book.set_like(int(book.get_like()) + 1)
        else:
            if book.get_dislike() == None:
                book.set_dislike(0)
            book.set_dislike(int(book.get_dislike()) + 1)
        db.session.commit()
    return render_template("book.html", books=books)

@app.route("/add_book", methods=['POST'])
def add_book():
    room = request.form['room_id']
    title = request.form.get('book_title')
    print(title)
    photo = request.form.get('photo')
    print(photo)
    author = request.form.get('author')
    print(author)
    description = request.form.get('description')
    print(description)
    book_dict = {'name': title, 'picture': photo, 'author': author,
                 'description': description, 'genre': None,
                 'rating': None, 'room': room}
    json_book = json.dumps(book_dict)
    print('before request')
    requests.post("http://127.0.0.1:5000/json", json=json_book)
    if 'add' in request.form:
        return render_template('adding.html', room_id=room)
    else:
        return render_template('end.html', room_id=room)


@app.route('/room', methods=['POST'])
def room():
    if 'create' in request.form:
        room_id = uuid.uuid4()
        return render_template('adding.html', room_id=room_id)
    if 'submit' in request.form:
        print('summiy')
        room_id = request.form.get('room_id')
        session['room_id'] = room_id
        return redirect(url_for('.book_page1'))


# рандомні книжки з бази даних
@app.route("/bookpage", methods=['POST', 'GET'])
def book_page():
    books = Books.query.all()
    num_of_book = random.randint(0, len(books))
    book = books[num_of_book]
    print('lol')
    if request.method == 'POST':
        print(int(request.form['book_id']))
        book = books[int(request.form['book_id'])]
        print(book)
        if 'like' in request.form:
            if book.get_like() == None:
                book.set_like(0)
            book.set_like(int(book.get_like()) + 1)

        else:
            if book.get_dislike() == None:
                book.set_dislike(0)
            book.set_dislike(int(book.get_dislike()) + 1)
        db.session.commit()
    return render_template("random_book.html", title=book.get_title(),
                           photo=book.get_photo(),
                           description=book.get_description(),
                           book_id=num_of_book)
# @app.route("/action")
# def action():
#     return render_template('choose_option.html')


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
#         return "<h1> Your twitter name is @{}".format(
#             account_info_json['screen_name'])
#     return '<h1>Request failed!</h1>'


if __name__ == "__main__":
    app.run(threaded=True, debug=True)
    # manager.run()
    # app.run(debug=True)
