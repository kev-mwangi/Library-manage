import json
import os
from datetime import datetime
DATA_FILE = "data/reservations.json"
class Reservation:
  def __init__(self,name, reservation_id,reservation_date, reservation_time, number_of_people):
    self.name = name
    self.reservation_id = reservation_id
    self.reservation_date = reservation_date
    self.reservation_time = reservation_time
    self.number_of_people = number_of_people
  pass



  def to_dict(self):
        return {
            "name": self.name,
            "reservation_id": self.reservation_id,
            "reservation_date": self.reservation_date,
            "reservation_time": self.reservation_time,
            "number_of_people": self.number_of_people
        }

  def __str__(self):
    return (
            f"Reservation ID: {self.reservation_id}"
            f"Name: {self.name}"
            f"Date: {self.reservation_date}"
            f"Time: {self.reservation_time}"
            f"Number of People: {self.number_of_people}"
        )
def remove_expired_reservations():
    data = load_data()
    today = datetime.now().date()

    updated_data = []

    for r in data:
        reservation_date = datetime.strptime(r["reservation_date"], "%Y-%m-%d").date()

        if reservation_date >= today:
            updated_data.append(r)

    save_data(updated_data)
def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
  while True:
    print("1. Make a reservation")
    print("2. View reservations")
    print("3. Clean expired reservations")
    print("4. Exit")

    choice = input("Choose an option: ")

    if choice == "1":
        name = input("Enter your name: ")
        reservation_id = input("Enter library ID: ")
        reservation_date = input("Enter reservation date (YYYY-MM-DD): ")
        reservation_time = input("Enter reservation time (HH:MM): ")
        number_of_people = int(input("Enter number of people: "))

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

        print("Reservation saved successfully!")

    elif choice == "2":
        data = load_data()

        if not data:
            print("No reservations found.")
        else:
            for r in data:
                print("Reservation ")
                print("ID:", r["reservation_id"])
                print("Name:", r["name"])
                print("Date:", r["reservation_date"])
                print("Time:", r["reservation_time"])
                print("People:", r["number_of_people"])

    elif choice == "3":
        remove_expired_reservations()
        print("Expired reservations cleaned.")

    elif choice == "4":
        print("Exiting system...")
        break

    else:
        print("Invalid option. Try again.")