from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/yarka/Documents/PycharmProjects/books/example19.db'

db = SQLAlchemy(app)

from models import *

db.create_all()


@app.route("/books")
def books():
    books = Books.query.all()
    return '<br>'.join([str(book) for book in books])


@app.route("/api/v0.1/likes", methods=["POST"])
def parse_likes():
    data = request.get_json()
    print(data)
    user = User(fb=data['facebook_id'])
    db.session.add(user)

    event = Event(user_id=data['user_id'], book_id=data['book_id'], reaction=data['reaction'])
    db.session.add(event)
    db.session.commit()

    return '{"result": "error"}'


@app.route("/events")
def event():
    events = Event.query.all()
    return '<br>'.join([str(event) for event in events])


if __name__ == "__main__":
    app.run(debug=True)
