import json
import os
from datetime import datetime

DATA_FILE = "data/borrow_records.json"


class BorrowRecord:
    def __init__(
        self,
        record_id,
        book_id,
        username,
        borrow_date=None,
        return_date=None,
        returned=False,
    ):
        self.__record_id = record_id
        self.__book_id = book_id
        self.username = username
        self.borrow_date = borrow_date or datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        self.return_date = return_date
        self.returned = returned

    @property
    def record_id(self):
        return self.__record_id

    @property
    def book_id(self):
        return self.__book_id

    def to_dict(self):
        return {
            "record_id": self.__record_id,
            "book_id": self.__book_id,
            "username": self.username,
            "borrow_date": self.borrow_date,
            "return_date": self.return_date,
            "returned": self.returned,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            record_id=data["record_id"],
            book_id=data["book_id"],
            username=data["username"],
            borrow_date=data["borrow_date"],
            return_date=data["return_date"],
            returned=data["returned"],
        )

    def __str__(self):
        status = "Returned" if self.returned else "Active"

        return (
            f"Record ID: {self.__record_id} | "
            f"Book ID: {self.__book_id} | "
            f"User: {self.username} | "
            f"Borrowed: {self.borrow_date} | "
            f"Status: {status}"
        )


class BorrowManager:
    def __init__(self):
        print("BorrowManager initialized...")

        self.records = []

        self._ensure_data_file()
        self._load_records()

        print(f"{len(self.records)} record(s) loaded.\n")

    def _ensure_data_file(self):
        os.makedirs("data", exist_ok=True)

        if not os.path.exists(DATA_FILE):
            with open(DATA_FILE, "w") as f:
                json.dump([], f)

    def _load_records(self):
        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)

            self.records = [
                BorrowRecord.from_dict(record)
                for record in data
            ]

        except (json.JSONDecodeError, FileNotFoundError):
            self.records = []

    def _save_records(self):
        with open(DATA_FILE, "w") as f:
            json.dump(
                [record.to_dict() for record in self.records],
                f,
                indent=4,
            )

    def _generate_id(self):
        if not self.records:
            return "BR001"

        last_id = self.records[-1].record_id
        number = int(last_id.replace("BR", "")) + 1

        return f"BR{number:03d}"

    def borrow_book(self, book_id, username, books):
        book = next(
            (book for book in books if book["id"] == book_id),
            None,
        )

        if not book:
            return (
                False,
                f"Book with ID '{book_id}' not found.",
                books,
            )

        if not book.get("available", True):
            return (
                False,
                f"Book '{book_id}' is currently unavailable.",
                books,
            )

        active_record = next(
            (
                record
                for record in self.records
                if record.book_id == book_id and not record.returned
            ),
            None,
        )

        if active_record:
            return (
                False,
                f"Book '{book_id}' is already borrowed.",
                books,
            )

        record = BorrowRecord(
            record_id=self._generate_id(),
            book_id=book_id,
            username=username,
        )

        self.records.append(record)

        for book in books:
            if book["id"] == book_id:
                book["available"] = False
                break

        self._save_records()

        return (
            True,
            f"Book '{book_id}' successfully borrowed by '{username}'.",
            books,
        )

    def return_book(self, book_id, username, books):
        record = next(
            (
                record
                for record in self.records
                if record.book_id == book_id
                and record.username == username
                and not record.returned
            ),
            None,
        )

        if not record:
            return (
                False,
                f"No active borrow record found for '{book_id}'.",
                books,
            )

        record.returned = True
        record.return_date = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        for book in books:
            if book["id"] == book_id:
                book["available"] = True
                break

        self._save_records()

        return (
            True,
            f"Book '{book_id}' successfully returned by '{username}'.",
            books,
        )

    def get_user_records(self, username):
        return [
            record
            for record in self.records
            if record.username == username
        ]

    def get_active_borrows(self):
        return [
            record
            for record in self.records
            if not record.returned
        ]

    def get_all_records(self):
        return self.records

    def display_records(self, records=None):
        records = records if records is not None else self.records

        if len(records) == 0:
            print("No borrow records found.")
            return

        print("\n--- Borrow Records ---")

        for record in records:
            print(record)

        print("----------------------\n")


# ==================================================
# TESTING SECTION
# ==================================================

if __name__ == "__main__":

    books = [
        {
            "id": "B001",
            "title": "Python Programming",
            "available": True,
        },
        {
            "id": "B002",
            "title": "Data Structures",
            "available": True,
        },
        {
            "id": "B003",
            "title": "Algorithms",
            "available": True,
        },
    ]

    manager = BorrowManager()

    print("===== LIBRARY BORROW SYSTEM TEST =====\n")

    success, message, books = manager.borrow_book(
        "B001",
        "Wilson",
        books,
    )

    print(message)

    print("\nCurrent Borrow Records:")
    manager.display_records()

    success, message, books = manager.return_book(
        "B001",
        "Wilson",
        books,
    )

    print(message)

    print("\nBorrow Records After Return:")
    manager.display_records()

    print("\nAvailable Books Status:")
    for book in books:
        print(
            f"{book['id']} - "
            f"{book['title']} - "
            f"Available: {book['available']}"
        )