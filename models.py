from app import db


class Books(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    title = db.Column(db.Text)
    description = db.Column(db.Text)
    photo = db.Column(db.Text)
    rating = db.Column(db.Integer)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    events = db.relationship("Event", backref='books', lazy=True)

    def get_title(self):
        return self.title

    def get_photo(self):
        return self.photo

    def get_rating(self):
        return self.rating

    def get_description(self):
        return self.description

    def get_id(self):
        return self.id

    def set_rating(self, rating):
        self.rating = rating


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    books = db.relationship("Books", backref='author', lazy=True)


class Genre(db.Model):
    id = db.Column(db.Integer, nullable=True, primary_key=True)
    name = db.Column(db.Text)
    books = db.relationship("Books", backref='genre', lazy=True)


class User(db.Model):
    id = db.Column(db.Integer, nullable=True, primary_key=True)
    fb = db.Column(db.Text)
    events = db.relationship("Event", backref='user', lazy=True)


class Event(db.Model):
    id = db.Column(db.Integer, nullable=True, primary_key=True)
    reaction = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))

    def __repr__(self):
        return "{0}".format(self.book_id, self.reaction)
