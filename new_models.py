from app import db


class Association(db.Model):
    __tablename__ = 'association'
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), primary_key=True)
    seen = db.Column(db.BOOLEAN)

    book = db.relationship('Book', back_populates='rooms')
    room = db.relationship('Room', back_populates='books')

class Book(db.Model):
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
    rooms = db.relationship('Association', back_populates='book')

    def set_like(self, rating):
        self.likes = rating

    def set_dislike(self, rating):
        self.dislikes = rating


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    books = db.relationship("Book", backref='author', lazy=True)


class Genre(db.Model):
    id = db.Column(db.Integer, nullable=True, primary_key=True)
    name = db.Column(db.Text)
    books = db.relationship("Book", backref='genre', lazy=True)


class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=True)
    books = db.relationship('Association', back_populates='room')


class User(db.Model):
    id = db.Column(db.Integer, nullable=True, primary_key=True)
