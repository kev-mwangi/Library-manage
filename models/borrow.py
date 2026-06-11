import json
import os
from datetime import datetime

DATA_FILE = "data/borrow_records.json"


class BorrowRecord:
    def __init__(self, record_id, book_id, username, borrow_date=None, return_date=None, returned=False):
        self.__record_id = record_id        # Encapsulated
        self.__book_id = book_id            # Encapsulated
        self.username = username
        self.borrow_date = borrow_date or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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
            "returned": self.returned
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            record_id=data["record_id"],
            book_id=data["book_id"],
            username=data["username"],
            borrow_date=data["borrow_date"],
            return_date=data["return_date"],
            returned=data["returned"]
        )

    def __str__(self):
        status = "Returned" if self.returned else "Active"
        return (f"Record ID: {self.__record_id} | Book ID: {self.__book_id} | "
                f"User: {self.username} | Borrowed: {self.borrow_date} | Status: {status}")


class BorrowManager:
    def __init__(self):
        self.records = []
        self._ensure_data_file()
        self._load_records()

    def _ensure_data_file(self):
        """Create data/ folder and borrow_records.json if they don't exist."""
        os.makedirs("data", exist_ok=True)
        if not os.path.exists(DATA_FILE):
            with open(DATA_FILE, "w") as f:
                json.dump([], f)

    def _load_records(self):
        """Load borrow records from JSON file."""
        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                self.records = [BorrowRecord.from_dict(r) for r in data]
        except (json.JSONDecodeError, FileNotFoundError):
            self.records = []

    def _save_records(self):
        """Save all borrow records to JSON file."""
        with open(DATA_FILE, "w") as f:
            json.dump([r.to_dict() for r in self.records], f, indent=4)

    def _generate_id(self):
        """Generate a unique record ID."""
        if not self.records:
            return "BR001"
        last_id = self.records[-1].record_id
        num = int(last_id.replace("BR", "")) + 1
        return f"BR{num:03d}"

    def borrow_book(self, book_id, username, books):
        """
        Borrow a book.
        - books: list of book dicts with 'id' and 'available' fields
        Returns (success: bool, message: str, updated_books: list)
        """
        # Check if book exists and is available
        book = next((b for b in books if b["id"] == book_id), None)
        if not book:
            return False, f"Book with ID '{book_id}' not found.", books

        if not book.get("available", True):
            return False, f"Book '{book_id}' is currently unavailable.", books

        # Check if user already has this book borrowed
        active = [r for r in self.records if r.book_id == book_id and not r.returned]
        if active:
            return False, f"Book '{book_id}' is already borrowed.", books

        # Create borrow record
        record = BorrowRecord(
            record_id=self._generate_id(),
            book_id=book_id,
            username=username
        )
        self.records.append(record)

        # Update book availability
        for b in books:
            if b["id"] == book_id:
                b["available"] = False
                break

        self._save_records()
        return True, f"Book '{book_id}' successfully borrowed by '{username}'.", books

    def return_book(self, book_id, username, books):
        """
        Return a borrowed book.
        - books: list of book dicts with 'id' and 'available' fields
        Returns (success: bool, message: str, updated_books: list)
        """
        record = next(
            (r for r in self.records
             if r.book_id == book_id and r.username == username and not r.returned),
            None
        )
        if not record:
            return False, f"No active borrow record found for book '{book_id}' by '{username}'.", books

        
        record.returned = True
        record.return_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        
        for b in books:
            if b["id"] == book_id:
                b["available"] = True
                break

        self._save_records()
        return True, f"Book '{book_id}' successfully returned by '{username}'.", books

    def get_user_records(self, username):
        """Get all borrow records for a specific user."""
        return [r for r in self.records if r.username == username]

    def get_active_borrows(self):
        """Get all currently borrowed (not returned) records."""
        return [r for r in self.records if not r.returned]

    def get_all_records(self):
        """Get all borrow records."""
        return self.records

    def display_records(self, records=None):
        """Print borrow records to the terminal."""
        records = records or self.records
        if not records:
            print("No borrow records found.")
            return
        print("\n--- Borrow Records ---")
        for r in records:
            print(r)
        print("----------------------\n")