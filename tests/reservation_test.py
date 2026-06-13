import pytest
import models.reservation as res  
from datetime import datetime, timedelta



@pytest.fixture
def temp_file(tmp_path, monkeypatch):
    test_file = tmp_path / "reservations.json"
    monkeypatch.setattr(res, "DATA_FILE", str(test_file))
    return test_file



def test_reservation_to_dict():
    r = res.Reservation(
        "John",
        "R001",
        "2026-06-20",
        "12:00",
        4
    )

    data = r.to_dict()

    assert data["name"] == "John"
    assert data["reservation_id"] == "R001"
    assert data["reservation_date"] == "2026-06-20"
    assert data["reservation_time"] == "12:00"
    assert data["number_of_people"] == 4



def test_save_and_load(temp_file):
    data = [
        {
            "name": "Alice",
            "reservation_id": "R100",
            "reservation_date": "2026-06-25",
            "reservation_time": "10:00",
            "number_of_people": 2
        }
    ]

    res.save_data(data)

    loaded = res.load_data()

    assert len(loaded) == 1
    assert loaded[0]["name"] == "Alice"



def test_remove_expired_reservations(temp_file):
    today = datetime.now().date()

    valid_date = (today + timedelta(days=2)).strftime("%Y-%m-%d")
    expired_date = (today - timedelta(days=2)).strftime("%Y-%m-%d")

    data = [
        {
            "name": "Valid",
            "reservation_id": "R1",
            "reservation_date": valid_date,
            "reservation_time": "10:00",
            "number_of_people": 3
        },
        {
            "name": "Expired",
            "reservation_id": "R2",
            "reservation_date": expired_date,
            "reservation_time": "11:00",
            "number_of_people": 2
        }
    ]

    res.save_data(data)

    res.remove_expired_reservations()

    remaining = res.load_data()

    assert len(remaining) == 1
    assert remaining[0]["name"] == "Valid"



def test_load_empty_file(temp_file):
    result = res.load_data()
    assert result == []