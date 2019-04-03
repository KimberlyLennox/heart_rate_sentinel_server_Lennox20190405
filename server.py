from flask import Flask, jsonify, request
from pymodm import connect
from pymodm import MongoModel, fields
import numpy as np
import datetime

app = Flask(__name__)
app.run(debug=True)
connect("mongodb://localhost:27017/SentinelServer")


class User(MongoModel):
    patientID = fields.CharField(primary_key=True)
    email = fields.EmailField()
    user_age = fields.IntegerField()
    status = fields.CharField()
    timestamp = fields.ListField()
    heart_rate = fields.ListField()


@app.route("/", methods=["GET"])
def hello():
    """
    Returns the string "Heart Rate Sentinel Server is ON"
    if the server is active
    """
    return "Heart Rate Sentinel Server is ON"


@app.route("/api/new_patient", methods=["POST"])
def newpatient():
    """
    Allows user to input patient id, email, and age in
    JSON format
    """
    r = request.get_json()
    ID = r["patient_id"]
    a_email = r["attending_email"]
    age = r["user_age"]
    u = User(ID, email=a_email, user_age=age)
    u.save()
    info = "Patient saved successfully"
    return jsonify(info)


@app.route("/api/heart_rate/<patient_id>", methods=["GET"])
def getHR(patient_id):
    """
    This function returns all heart rate data stored within the
    database
    Args: Patient ID
    Returns: All heart rate data ever collected from this patient
    """
    user = User.objects.raw({"_id": patient_id}).first()
    HR = user.heart_rate
    return jsonify(HR)


@app.route("/api/heart_rate/status/<patient_id>", methods=["GET"])
def Status(patient_id):
    """
    Returns most recent HR data for the patient with the given ID
    Args: Patient ID
    returns: latest heart rate, heart rate status (tachycardic or not),
    timestamp of most recent HR data point.
    """
    user = User.objects.raw({"_id": patient_id}).first()
    HR = user.heart_rate[-1:]
    tach = HRStatus(HR)
    T = user.timestamp[-1:]
    info = {
            "heart_rate": HR,
            "status": tach,
            "timestamp": T
            }
    return jsonify(info)


@app.route("/api/heart_rate", methods=["POST"])
def sendHR():
    """
    Posts new heart rate data
    Args:
    Patient ID
    Heart Rate
    Returns:
    Timestamp of request
    """
    r = request.get_json()
    patient_id = str(r["patient_id"])
    HR_ind = r["heart_rate"]
    T_ind = datetime.datetime.now()
    user = User.objects.raw({"_id": patient_id}).first()
    HR = user.heart_rate
    if user.heart_rate is None:
        HR = HR_ind
        T = T_ind
    else:
        T = user.timestamp
        HR.append(HR_ind)
        T.append(T_ind)
    user.heart_rate = HR
    user.timestamp = T
    user.save()
    return jsonify(T_ind)


def HRStatus(HR):
    """
    Determines whether patient is tachycardic
    Args: HR, patient herat rate
    Returns: outstring: whether or not patient is tachycardic
    """
    if HR == []:
        outstring = "None"
    else:
        HR = HR[0]
        if HR > 90:
            outstring = "tachycardic"
        else:
            outstring = "not tachycardic"
    return outstring
