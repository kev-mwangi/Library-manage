from models.borrow import BorrowManager
from models.auth import register_user, login, logout
from models.reservation import Reservation, remove_expired_reservations, load_data, save_data
from models.book_management import book

borrow_manager = BorrowManager()
book_manager = book("title", "author", "year", "genre")

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

#Book management
def add_book(book_id, title, author, year, genre=""):
    return book(book_id, title, author, year, genre)

def list_books():
    return book_manager.list_books()

def delete_book(book_id):
    return book_manager.delete_book(book_id) 

#Create a reservation
def create_reservation(
    name,
    reservation_id,
    reservation_date,
    reservation_time,
    number_of_people
):
    reservation = Reservation(
        name,
        reservation_id,
        reservation_date,
        reservation_time,
        number_of_people
    )

    data = load_data()
    data.append(reservation.to_dict())
    save_data(data)

    print("Your reservation has been saved successfully.")

def view_reservations():
    data = load_data()

    if not data:
        print("No reservations found.")
    else:
        print("Your reservations:")
        for r in data:
            print("Reservation ")
            print("ID:", r["reservation_id"])
            print("Name:", r["name"])
            print("Date:", r["reservation_date"])
            print("Time:", r["reservation_time"])
            print("People:", r["number_of_people"])

#user logout
def logout_user():
    logout()