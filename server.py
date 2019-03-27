from flask import Flask, jsonify, request
app = Flask(__name__)


@app.route("/", methods=["GET"])
def hello():
    """
    Returns the string "Heart Rate Sentinel Server is ON"
    if the server is active
    """
    return "Heart Rate Sentinel Server is ON"
