BOOKS = {
    'Hamlet':{
        "title":"Hamlet",
        "author_fname":"William",
        "author_lname":"Shakespeare",
    },
    'Midsummer':{
        "title":"Midsummer",
        "author_fname":"William",
        "author_lname":"Shakespeare",
    },
}

def read():
    """
    creates list of books
    """
    return [BOOKS[key] for key in sorted(BOOKS.keys())]