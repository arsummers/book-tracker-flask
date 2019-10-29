from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Book

engine = create_engine('sqlite:///books-collection.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/books')
def show_books():
    books = session.query(Book).all()
    return render_template('books.html', books=books)

@app.route('/books/new', methods=['GET', 'POST'])
def new_book():
    if request.method == 'POST':
        new_book = Book(title=request.form['name'], author=request.form['author'])
        session.add(new_book)
        session.commit()
        return redirect(url_for('show_books'))
    else:
        return render_template('newBook.html')

@app.route('/books/<int:book_id>/edit/', methods=['GET', 'POST'])
def edit_book(book_id):
    edited_book = session.query(Book).filter_by(id=book_id).one()
    