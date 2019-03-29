from flask import Flask, jsonify, request
from pymodm import connect
from pymodm import MongoModel, fields
import numpy as np
import datetime

app = Flask(__name__)
connect("mongodb://localhost:27017/SentinelServer")


class User(MongoModel):
    patientID = fields.CharField(primary_key=True)
    email = fields.EmailField()
    user_age = fields.IntegerField()
    status = fields.CharField()
    timestamp = fields.DateTimeField()
    heart_rate = fields.FloatField()


@app.route("/", methods=["GET"])
def hello():
    """
    Returns the string "Heart Rate Sentinel Server is ON"
    if the server is active
    """
    return "Heart Rate Sentinel Server is ON"


@app.route("/api/new_patient", methods=["POST"])
def newpatient():
    r = request.get_json()
    ID = r["patient_id"]
    a_email = r["attending_email"]
    age = r["user_age"]
    u = User(ID, email=a_email, user_age=age)
    u.save()
    return jsonify(a_email)


@app.route("/api/heart_rate/<patient_id>", methods=["GET"])
def getage(patient_id):
    user = User.objects.raw({"_id": patient_id}).first()
    HR = user.user_age
    return jsonify(HR)
