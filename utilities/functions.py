from models.borrow import BorrowManager
from auth import register_user, login, logout

borrow_manager = BorrowManager()

#User authentication
def register():
    username = input("Enter username: ")
    password = input("Enter password: ")
    role = input("Enter role (member/librarian): ")
    register_user(username, password, role)

def login_user():
    username = input("Enter username: ")
    password = input("Enter password: ")
    login(username, password)

#Borrowing and returning of books
def borrow_book():
    book_id = input("Enter the book ID of the book you want to borrow: ")
    username = input("Enter your username: ")
    borrow_manager.borrow_book(username, book_id)

    print(f"Book with ID {book_id} has been borrowed by {username}.")
    
def return_book():
    book_id = input("Enter the book ID of the book you want to return: ")
    username = input("Enter your username: ")
    borrow_manager.return_book(username, book_id)

    print(f"Book with ID {book_id} has been returned by {username}.")

def my_borrowed_books():
    username = input("Enter your username: ")
    records = borrow_manager.get_user_records(username)
    if not records:
        print("You have no borrowed books.")
        return
    print("Your borrowed books:")
    for record in records:
        status = "Returned" if record.returned else "Borrowed"
        print(f"- Book ID: {record.book_id}, Status: {status}, Borrow Date: {record.borrow_date}, Return Date: {record.return_date}")

def all_borrows():
    records = borrow_manager.get_all_records()

def main_menu():
    while True:
        print("\nMain Menu:")
        print("1. Register")
        print("2. Login")
        print("3. Borrow a Book")
        print("4. Return a Book")
        print("5. View My Borrowed Books")
        print("6. View All Borrows (Librarian Only)")
        print("7. Logout")
        print("0. Exit")

        choice = input("Enter your choice: ")
        
        if choice == "1":
            register()
        elif choice == "2":
            login_user()
        elif choice == "3":
            borrow_book()
        elif choice == "4":
            return_book()
        elif choice == "5":
            my_borrowed_books()
        elif choice == "6":
            all_borrows()
        elif choice == "7":
            logout()
        elif choice == "0":
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")

