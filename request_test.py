import requests

# requests.post("http://yarkalyba.pythonanywhere.com/api/v0.1/likes", json={"id": "bhjfsbkjdfdkjf", "book_id": 42, "event": "liked"})
data = {"facebook_id": "rybka", "book_id": 42, "user_id": 13, "reaction": 1}
r = requests.post("http://localhost:5000/api/v0.1/likes", json=data)
