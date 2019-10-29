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
        return render_template('new_book.html')

@app.route('/books/<int:book_id>/edit/', methods=['GET', 'POST'])
def edit_book(book_id):
    edited_book = session.query(Book).filter_by(id=book_id).one()
    if request.method == 'POST':
        if request.form['name']:
            edit_book.title = request.form['name']
            return redirect(url_for('show_books'))
    else:
        return render_template('edited_book.html', book=edited_book)

@app.route('/books/<int:book_id>/delete/', methods=['GET', 'POST'])
def delete_book(book_id):
    book_to_delete = session.query(Book).filter_by(id=book_id).one()
    if request.method == 'POST':
        session.delete(book_to_delete)
        session.commit()
        return redirect(url_for('show_books', book_id=book_id))
    else:
        return render_template('delete_book.html', book=book_to_delete)

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=4996)
    