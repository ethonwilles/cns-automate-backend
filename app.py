from flask import Flask, request
from flask_cors import CORS
from flask_heroku import Heroku
import pymongo

app = Flask(__name__)
heroku = Heroku(app)

@app.route("/", methods=["GET"])
def get():
    return "working"

@app.route("/service-tracker", methods=["POST"])
def service():
    return None

@app.route("/invoice-tracker", methods=["POST"])
def invoice():
    return None


if __name__ == "__main__":
    app.run(debug=True)