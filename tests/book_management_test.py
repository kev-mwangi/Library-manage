import pytest
from models.book_management import book  


def test_book_init():
    b = book(1, "1984", "George Orwell", 1949, "Dystopian")
    assert b.id == 1
    assert b.title == "1984"
    assert b.author == "George Orwell"
    assert b.year == 1949
    assert b.genre == "Dystopian"



def test_book_default_genre():
    b = book(2, "Animal Farm", "George Orwell", 1945)
    assert b.genre == ""


def test_to_dict():
    b = book(3, "Dune", "Frank Herbert", 1965, "Sci-Fi")
    data = b.to_dict()
    assert data == {
        "id": 3,
        "title": "Dune",
        "author": "Frank Herbert",
        "year": 1965,
        "genre": "Sci-Fi"
    }



def test_from_dict():
    data = {
        "id": 4,
        "title": "Fahrenheit 451",
        "author": "Ray Bradbury",
        "year": 1953,
        "genre": "Dystopian"
    }

    b = book.from_dict(data)

    assert isinstance(b, book)
    assert b.id == 4
    assert b.title == "Fahrenheit 451"
    assert b.author == "Ray Bradbury"
    assert b.year == 1953
    assert b.genre == "Dystopian"



def test_from_dict_missing_genre():
    data = {
        "id": 5,
        "title": "The Hobbit",
        "author": "J.R.R. Tolkien",
        "year": 1937
    }

    b = book.from_dict(data)

    assert b.genre == ""



def test_str_output():
    b = book(6, "Brave New World", "Aldous Huxley", 1932, "Sci-Fi")

    output = str(b)

    assert "Brave New World" in output
    assert "Aldous Huxley" in output
    assert "1932" in output
    assert "Sci-Fi" in output