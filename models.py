from app import db

rooms = db.Table('rooms',
                 db.Column('book_id', db.Integer, db.ForeignKey('books.id'),
                           primary_key=True),
                 db.Column('room_id', db.Integer, db.ForeignKey('room.id')))


class Books(db.Model):
    """
    Class to form a table in a database
    Represents a book with such columns as title, description, p
    """
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    title = db.Column(db.Text)
    description = db.Column(db.Text)
    photo = db.Column(db.Text)
    likes = db.Column(db.Integer)
    dislikes = db.Column(db.Integer)
    rating_from_bookstore = db.Column(db.Float)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))

    def get_title(self):
        return self.title

    def get_photo(self):
        return self.photo

    def get_like(self):
        return self.likes

    def get_dislike(self):
        return self.dislikes

    def get_description(self):
        return self.description

    def get_id(self):
        return self.id

    def set_like(self, rating):
        self.likes = rating

    def set_dislike(self, rating):
        self.dislikes = rating


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    books = db.relationship("Books", backref='author', lazy=True)


class Genre(db.Model):
    id = db.Column(db.Integer, nullable=True, primary_key=True)
    name = db.Column(db.Text)
    books = db.relationship("Books", backref='genre', lazy=True)


class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=True)
    rooms_books = db.relationship('Books', secondary=rooms, lazy='subquery',
                                  backref=db.backref('rooms_with_books',
                                                     lazy=True))
    visited = db.Column(db.BOOLEAN)


class User(db.Model):
    id = db.Column(db.Integer, nullable=True, primary_key=True)
