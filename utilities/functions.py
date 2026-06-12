from models.borrow import BorrowManager
from auth import register_user, login, logout

borrow_manager = BorrowManager()

#User authentication
def register(username, password, role):
    register_user(username, password, role)

def login_user(username, password):
    login(username, password)

#Borrowing and returning of books
def borrow_book(username, book_id):
    borrow_manager.borrow_book(username, book_id)

    print(f"Book with ID {book_id} has been borrowed by {username}.")

def return_book(username, book_id):
    borrow_manager.return_book(username, book_id)

    print(f"Book with ID {book_id} has been returned by {username}.")

def my_borrowed_books(username):
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

    print("All borrowed books:")

#user logout
def logout_user():
    logout()