from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_dance.contrib.facebook import make_facebook_blueprint, facebook
from flask_dance.contrib.twitter import make_twitter_blueprint, twitter
import random

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



twitter_blueprint = make_twitter_blueprint(api_key='f7dUFCVeAspsUmXBZXGLrNF8e',
                                           api_secret='yAjRQ7CXzoOmPjfoVO2QLOnz40sqhIyU3a43WC4NdZXbLXwJMI')

app.register_blueprint(twitter_blueprint, url_prefix="/twitter_login")


facebook_blueprint = make_facebook_blueprint(client_secret='84e3f634967016f48ac1b93987cd3ac6', client_id='548449348874242')
app.register_blueprint(facebook_blueprint, url_prefix="/facebook_login")

@app.route("/facebook")
def facebook_login():
    if not facebook.authorized:
        return redirect(url_for("facebook.login"))
    account_info = facebook.get("/me")

    if account_info.ok:
        account_info_json = account_info.json()
        return "<h1> Your twitter name is @{}".format(
            account_info_json['screen_name'])
    return '<h1>Request failed!</h1>'


@app.route("/twitter")
def twitter_login():
    if not twitter.authorized:
        return redirect(url_for("twitter.login"))
    account_info = twitter.get("account/settings.json")

    if account_info.ok:
        account_info_json = account_info.json()
        # можна там свякі штуки робити вже
        return "<h1> Your twitter name is @{}".format(
            account_info_json['screen_name'])
    return '<h1>Request failed!</h1>'

if __name__ == "__main__":
    app.run(debug=True)
