import argparse
from auth import register_user
from models.borrow import BorrowManager
import utilities.functions

borrow_manager = BorrowManager()

def main():
    parser = argparse.ArgumentParser(prog="Library Management System")

    subparsers = parser.add_subparsers(dest="user_command")

    # Registration
    register_parser = subparsers.add_parser("register")
    register_parser.add_argument("--username", required=True)
    register_parser.add_argument("--password", required=True)

    # User login
    login_parser = subparsers.add_parser("login")
    login_parser.add_argument("--username", required=True)
    login_parser.add_argument("--password", required=True)

    # Borrowing a book

    borrow_parser = subparsers.add_parser("borrow")
    borrow_parser.add_argument("--book_id", required=True)
    borrow_parser.add_argument("--username", required=True)

    # Returning a book
    return_parser = subparsers.add_parser("return")
    return_parser.add_argument("--book_id", required=True)
    return_parser.add_argument("--username", required=True)

    # View my borrowed books
    subparsers.add_parser("my_borrows")

    # View all borrows (librarian only)
    subparsers.add_parser("all_borrows")

    # User logout
    subparsers.add_parser("logout")

    args = parser.parse_args()

    global books

    # User commands
    if args.user_command == "register":
        register_user(args.username, args.password)

    elif args.user_command == "login":
        utilities.functions.login_user(args.username, args.password)

    elif args.user_command == "borrow":
        success, msg, books = borrow_book(args.book_id, args.username, books)
        print(msg)

    elif args.user_command == "return":
        success, msg, books = return_book(args.book_id, args.username, books)
        print(msg)

    elif args.user_command == "my_borrows":
        utilities.functions.my_borrowed_books(args.username)

    elif args.user_command == "all_borrows":
        utilities.functions.all_borrows()

    elif args.user_command == "logout":
        utilities.functions.logout_user()

    else:
        parser.print_help()

# These avoid input() inside functions.py and allow us to pass parameters directly from the CLI
def borrow_book(book_id, username, books):
    return borrow_manager.borrow_book(book_id, username, books)


def return_book(book_id, username, books):
    return borrow_manager.return_book(book_id, username, books)