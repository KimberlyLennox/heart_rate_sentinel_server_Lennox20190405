import requests

r = requests.get("http://127.0.0.1:5000")
print(r.text)

patient = {
           "patient_id": "1",
           "attending_email": "lennox_kimberly@yahoo.com",
           "user_age": 50,
           }

r = requests.post("http://127.0.0.1:5000/api/new_patient", json=patient)
print(r.json())

r2 = requests.get("http://127.0.0.1:5000/api/heart_rate/1")
print(r2.json())
