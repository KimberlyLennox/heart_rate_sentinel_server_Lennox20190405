import requests
import time
import datetime

r = requests.get("http://127.0.0.1:5000")
print(r.text)


patient = {
           "patient_id": "1",
           "attending_email": "lennoxkimberly25@gmail.com",
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
TJ = datetime.datetime.now()
HR = {
     "patient_id": "1",
     "heart_rate": 90
     }

time.sleep(5)
r3 = requests.post("http://127.0.0.1:5000/api/heart_rate", json=HR)
print(r3.text)

TJ = str(TJ)
print(TJ)
print(TJ)

HR = {
     "patient_id": "1",
     "heart_rate": 60
     }


r3 = requests.post("http://127.0.0.1:5000/api/heart_rate", json=HR)
print(r3.json())

r2 = requests.get("http://127.0.0.1:5000/api/heart_rate/1")
print("Retrieved HR")
print(r2.json())


r4 = requests.get("http://127.0.0.1:5000/api/heart_rate/status/1")
print(r4.json())

r5 = requests.get("http://127.0.0.1:5000/api/heart_rate/average/1")
print(r5.json())
time.sleep(5)
T_fut = datetime.datetime.now()
HR = {
     "patient_id": "1",
     "heart_rate_average_since": str(T_fut)
     }

r6 = requests.get("http://127.0.0.1:5000/api/heart_rate/interval_average",
                  json=HR)
print(r6.json())
