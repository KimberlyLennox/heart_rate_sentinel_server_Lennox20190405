import requests
import time
import datetime

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

time.sleep(5)
r3 = requests.post("http://127.0.0.1:5000/api/heart_rate", json=HR)
print(r3.text)
TJ = r3.text
TJ = TJ.rstrip("\n")
TJ = TJ.replace('"', '')
T = datetime.datetime.strptime(TJ, "%a, %d %b %Y %H:%M:%S %Z")
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
HR = {
     "patient_id": "1",
     "heart_rate_average_since": TJ
     }

r6 = requests.get("http://127.0.0.1:5000/api/heart_rate/interval_average",
                  json=HR)
print(r6.json())
