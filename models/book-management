class book:
    def __init__(self, book_id: int, title: str, author: str, year: int, genre: str = "")

        self.id = book_id
        self.title = title
        self.author = author
        self.year = year
        self.genre = genre

    def to_dict(self) -> dict:
        return{
            "id": self.id,
            "title": self.title,
            "author":self.author,
            "year": self.year,
            "genre": self.genre
        }

    @classmethod
    def from_dict(cls, data: dict) -> "book":
        return cls(
            book_id=data["id"],
            title=data["title"],
            author=data["author"],
            year=data["year"],
            genre=data.get("genre","")
        )

    def __str__(self) ->str:
        genre_str = f" genre : {self.genre}" if self.genre else ""
        return(
            f" ID : {self.id}\n"
            f" Title : {self.title}\n"
            f" Author : {self.author}\n"
            f" Year : {self.year}\n"
            f"{genre_str}"
        ).rstrip()