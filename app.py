from flask import Flask, render_template, request, redirect, url_for, jsonify

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


# RESTful API stuff
def get_books():
    books = session.query(Book).all()
    return jsonify(books=[b.serialize for b in books])

def get_book(book_id):
    books = session.query.filter_by(id = book_id).one()
    return jsonify(books=books.serialize)

def make_a_new_book(title, author):
    added_book = Book(title=title, author=author)
    session.add(added_book)
    session.commit()
    return jsonify(Book=added_book.serialize)

def update_a_book(id, title, author):
    updated_book = session.query(Book).filter_by(id=id).one()
    if not title:
        updated_book.title = title
    if not author:
        updated_book.author = author

    session.add(updated_book)
    session.commit()
    return 'Updated a book with id %s' % id

def delete_a_book(id):
    book_to_delete = session.query(Book).filter_by(id=id).one()
    session.delete(book_to_delete)
    session.commit()
    return 'Removed Book with id %s' % id


@app.route('/')
@app.route('/booksApi', methods=['GET', 'POST'])
def books_function():
    if request.method == 'GET':
        return get_books()
    elif request.method == 'POST':
        title = request.args.get('title', '')
        author = request.args.get('author', '')
        return make_a_new_book(title, author)

@app.route('/booksApi/', methods=['GET', 'PUT', 'DELETE'])
def book_function_id(id):
    if request.method == 'GET':
        return get_book(id)

    elif request.method == 'PUT':
        title = request.args.get('title', '')
        author = request.args.get('author', '')
        return update_a_book(id, title, author)

    elif request.method == 'DELETE':
        return delete_book(id)



if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=4996)
    