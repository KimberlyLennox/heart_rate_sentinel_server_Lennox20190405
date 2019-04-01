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

HR = {
     "patient_id": "1",
     "heart_rate": 100
     }
r3 = requests.post("http://127.0.0.1:5000/api/heart_rate", json=HR)
print(r3.text)

HR = {
     "patient_id": "1",
     "heart_rate": 90
     }

r3 = requests.post("http://127.0.0.1:5000/api/heart_rate", json=HR)
print(r3.json())

r2 = requests.get("http://127.0.0.1:5000/api/heart_rate/1")
print("Retrieved HR")
print(r2.json())

r4 = requests.get("http://127.0.0.1:5000/api/heart_rate/status/1")
print(r4.json())
