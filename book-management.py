import json  
import os  

class Book:  
    def __init__(self, book_id, title, author, year, genre=""):  
        self.id = book_id  
        self.title = title  
        self.author = author  
        self.year = year  
        self.genre = genre  

    def to_dict(self):  
        return {  
            "id": self.id,  
            "title": self.title,  
            "author": self.author,  
            "year": self.year,  
            "genre": self.genre  
        }  

class BookManager:  
    def __init__(self, filename="books.json"):  
        self.filename = filename  
        self.books = []  
        self.load_books()  

    def load_books(self):  
        if os.path.exists(self.filename):  
            with open(self.filename, "r") as file:  
                data = json.load(file)  
                self.books = [Book(**book) for book in data]  

    def save_books(self):  
        with open(self.filename, "w") as file:  
            json.dump(  
                [book.to_dict() for book in self.books],  
                file,  
                indent=4  
            )  

    def add_book(self, book):  
        self.books.append(book)  
        self.save_books()  
        print("Book added successfully!")  

    def list_books(self):  
        if not self.books:  
            print("No books available.")  
            return  

        for book in self.books:  
            print(  
                f"ID: {book.id}, "  
                f"Title: {book.title}, "  
                f"Author: {book.author}, "  
                f"Year: {book.year}, "  
                f"Genre: {book.genre}"  
            )  

    def search_book(self, keyword):  
        results = [  
            book for book in self.books  
            if keyword.lower() in book.title.lower()  
            or keyword.lower() in book.author.lower()  
        ]  

        if results:  
            for book in results:  
                print(  
                    f"ID: {book.id}, "  
                    f"Title: {book.title}, "  
                    f"Author: {book.author}"  
                )  
        else:  
            print("No matching books found.")  

    def edit_book(self, book_id):  
        for book in self.books:  
            if book.id == book_id:  
                book.title = input("New title: ")  
                book.author = input("New author: ")  
                book.year = int(input("New year: "))  
                book.genre = input("New genre: ")  
                self.save_books()  
                print("Book updated successfully!")  
                return  

        print("Book not found.")  

    def delete_book(self, book_id):  
        for book in self.books:  
            if book.id == book_id:  
                self.books.remove(book)  
                self.save_books()  
                print("Book deleted successfully!")  
                return  

        print("Book not found.")  

def main():  
    manager = BookManager()  

    while True:  
        print("\n--- Book Management System ---")  
        print("1. Add Book")  
        print("2. List Books")  
        print("3. Search Book")  
        print("4. Edit Book")  
        print("5. Delete Book")  
        print("6. Exit")  

        choice = input("Enter choice: ")  

        if choice == "1":  
            book = Book(  
                int(input("Book ID: ")),  
                input("Title: "),  
                input("Author: "),  
                int(input("Year: ")),  
                input("Genre: ")  
            )  
            manager.add_book(book)  

        elif choice == "2":  
            manager.list_books()  

        elif choice == "3":  
            keyword = input("Enter title or author: ")  
            manager.search_book(keyword)  

        elif choice == "4":  
            manager.edit_book(int(input("Enter Book ID: ")))  

        elif choice == "5":  
            manager.delete_book(int(input("Enter Book ID: ")))  

        elif choice == "6":  
            print("Goodbye!")  
            break  

        else:  
            print("Invalid choice.")  

if __name__ == "__main__":  
    main()