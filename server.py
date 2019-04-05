import logging
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from flask import Flask, jsonify, request
from pymodm import connect
from pymodm import MongoModel, fields
import numpy as np
import datetime
import math
app = Flask(__name__)
connect("mongodb+srv://Kim:Password"
        "cluster0-cxyhs.mongodb.net/test?retryWrites=true")
for handler in logging.root.handlers[:]:  # This line makes the log file work
    logging.root.removeHandler(handler)
logging.basicConfig(filename="server_log.log", filemode="w",
                    level=logging.INFO)


class User(MongoModel):
    """
    MongoDB user class that stores heart rate,
    timestamp of all heart rate data, user age
    patient ID number (Primary key), and
    attending physician email address.
    """
    patientID = fields.CharField(primary_key=True)
    email = fields.EmailField()
    user_age = fields.IntegerField()
    status = fields.CharField()
    timestamp = fields.ListField()
    heart_rate = fields.ListField()


def HRStatus(HR, user):
    """
    Determines whether patient is tachycardic
    Args: HR, patient herat rate
    Returns: outstring: whether or not patient is tachycardic
    """
    if HR == []:
        outstring = "No heart rate data has been entered"
    else:
        HR = HR[0]
        if HR > 90:
            outstring = "tachycardic"
        else:
            outstring = "not tachycardic"
    if outstring == "tachycardic":
        try:
            tach = SendStatus(user)
            logging.info("Patient " + user.patientID+" is tachycardic. " +
                         "Emailed " + user.email)
        except AttributeError:  # Avoid sending email during testing
            a = 1
    user.status = outstring
    try:
        user.save()
    except AttributeError:  # Avoid saving during testing
        a = 1
    return outstring


def CalcAverage(HR):
    """
    Calculates average heart rates from a list
    Args: HR, list of heart rates
    Returns: avg, average value
    """
    if HR == []:
        avg = "No heart rate data has been entered"
    else:
        vec = np.array(HR)
        avg = np.mean(HR)
    return avg


def GetIndex(T, time):
    """
    Finds all timestamp values after a timestamp specified
    by the user, assuming timestamps are in order
    Args:
        T: vector of timestamps
        time: timestamp reference
    Returns:
        idx_min: minimum index of timestamp after the reference time
    """
    T_array = np.array(T, dtype='datetime64')
    idx = np.where(T_array >= time)
    if np.size(idx) == 0:
        idx_min = -1
    else:
        idx_min = (idx[0])
        idx_min = idx_min[0]
    return idx_min


def CheckFormat(r):
    """
    Makes sure that input data for a new patient has the correct entries
    in the correct data types
    Args:
        r: dictionary created from user input
    Returns:
        x: string assessing format correctness
    """
    try:
        t = str(r["patient_id"])
        a = str(r["attending_email"])
        u = int(r["user_age"])
        u_test = u-1
        x = "Patient saved successfully"
    except KeyError:
        x = "Incorrect format: please try again"
        logging.warning(x)
    except TypeError:
        x = "Incorrect format: please try again"
        logging.warning(x)
    except ValueError:
        x = "Incorrect format: please try again"
        logging.warning(x)
    return x


def CheckHRData(r):
    """
    Makes sure that heart rate data has been input successfully
    Args:
        r: dictionary created from user input
    Returns:
        x: string/int assessing format correctness
    """
    x = 0
    try:
        t = str(r["patient_id"])
        m = (r["heart_rate"])
        n = math.sqrt(m)  # Check if value is positive
        m = m/3
        if m < 0:
            x = "Incorrect format: please try again"
    except KeyError:
        x = "Incorrect format: please try again"
    except TypeError:
        x = "Incorrect format: please try again"
    except ValueError:
        x = "Incorrect format: please try again"
    return x


def CheckIntervalData(r):
    """
    Makes sure that heart rate data and timestamp has been
    input successfully
    Args:
        r: dictionary created from user input
    Returns:
        x: string/int assessing format correctness
    """
    x = 0
    try:
        ID = str(r["patient_id"])
        time = str(r["heart_rate_average_since"])
        time = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S.%f")
    except KeyError:
        x = "Incorrect format: please try again"
    except TypeError:
        x = "Incorrect format: please try again"
    except ValueError:
        x = "Incorrect format: please try again"
    return x


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
    x = CheckFormat(r)
    if x == "Incorrect format: please try again":
        info = "Incorrect input patient format; please try again"
        logging.warning(info)
    else:
        ID = str(r["patient_id"])
        a_email = r["attending_email"]
        age = r["user_age"]
        u = User(ID, email=a_email, user_age=age)
        u.save()
        info = x
        logging.info("Patient "+ID+" added to database")
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
    return(jsonify(HR))


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
    T = user.timestamp[-1:]
    info = {
            "heart_rate": HR,
            "status": user.status,
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
    x = CheckHRData(r)
    T_ind = datetime.datetime.now()
    if x == "Incorrect format: please try again":
        outjson = "Incorrect HR Data format; please try again"
        logging.warning(outjson)
    else:
        patient_id = str(r["patient_id"])
        HR_ind = int(r["heart_rate"])
        user = User.objects.raw({"_id": patient_id}).first()
        HR = user.heart_rate
        outjson = T_ind
        if user.heart_rate is None:
            HR = HR_ind
            T = T_ind
        else:
            T = user.timestamp
            HR.append(HR_ind)
            T.append(T_ind)
        tach = HRStatus([HR_ind], user)
        user.heart_rate = HR
        user.timestamp = T
        user.save()
        outjson = {
                   "Time": T_ind,
                   "Status": tach
                   }
    return jsonify(outjson)


@app.route("/api/heart_rate/average/<patient_id>", methods=["GET"])
def GetAverage(patient_id):
    """
    Returns average of all previous heart rate measurements
    Args:
        patient_id: patient identification number
    returns:
        Patient ID
        avg: HR average
    """
    patient_id = str(patient_id)
    user = User.objects.raw({"_id": patient_id}).first()
    avg = CalcAverage(user.heart_rate)
    out = {"Patient ID": patient_id,
           "HR Average": avg}
    return jsonify(out)


@app.route("/api/heart_rate/interval_average", methods=["GET"])
def IntervalAverage():
    """
    Returns average heart rate over given time interval
    Args:
        r: json input with entries
        patient ID
        heart_rate_average_since: timestamp for start of measurements
    Returns:
        out: Heart rate average over given time interval
    """
    r = request.get_json()
    x = CheckIntervalData(r)
    if x == "Incorrect format: please try again":
        out = "Incorrect interval average format; please try again"
        logging.warning(out)
    else:
        time = r["heart_rate_average_since"]
        time = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S.%f")
        patient_id = str(r["patient_id"])
        user = User.objects.raw({"_id": patient_id}).first()
        HRmat = user.heart_rate
        T = user.timestamp
        if user.heart_rate == []:
            out = "None"
        else:
            idx = GetIndex(T, time)
            if idx == []:
                out = "None"
            elif idx == -1:
                out = "No measurements after input time"
            else:
                HR = HRmat[idx:len(HRmat)]
                out = CalcAverage(HR)
    return jsonify(out)


# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
def SendStatus(user):
    """
    Sends email to attending physician if patient is tachycardic
    Args: user: MongoDB user object
    """
    HR = (user.heart_rate[-1:])
    HRstring = str(HR[0])
    time = user.timestamp[-1]
    outstring = ("Patient <b>" + str(user.patientID) +
                 "</b> is tachycardic with a heart rate of <b>" +
                 HRstring + "</b> on " +
                 time.strftime("%m/%d/%Y, at %H:%M:%S"))
    message = Mail(
        from_email='kimberly.lennox@duke.edu',
        to_emails=user.email,
        subject='Patient '+str(user.patientID)+" Status",
        html_content=outstring)
    try:
        sg = SendGridAPIClient(os.environ.get('API Key'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)
    return user.email
