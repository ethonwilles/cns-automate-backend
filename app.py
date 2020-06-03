from flask import Flask, request
from flask_cors import CORS
from flask_heroku import Heroku
import pymongo
import json
import os
from dotenv import load_dotenv

load_dotenv()
password = os.getenv("PASS")
app = Flask(__name__)
heroku = Heroku(app)

myclient = pymongo.MongoClient(f"mongodb+srv://admin:{password}@cluster0-rexpr.mongodb.net/test?retryWrites=true&w=majority")
mydb = myclient["mydb"]
service = mydb["service"]
invoice = mydb["invoice"]



@app.route("/", methods=["GET"])
def get():
    
    return "working"

@app.route("/service-tracker", methods=["GET","POST"])
def service():
    mydb = myclient["mydb"]
    service = mydb["service"]

    
    if request.method == "POST":

        new_num = request.json["num"]
        old_num = service.find()
        query = {}
        for item in old_num:
            query["num"] = item["num"]
        
        service.update_one(query, {"$set": {"num" : new_num}})

        return "worked"
    elif request.method == "GET":
        old_num = service.find()
        query = {}
        for item in old_num:
            query["num"] = item["num"]
        return query

@app.route("/invoice-tracker", methods=["GET","POST"])
def invoice():
    mydb = myclient["mydb"]
    invoice = mydb["invoice"]


    if request.method == "POST":
        new_num = request.json["num"]
        old_num = invoice.find()
        query = {}
        for item in old_num:
            query["num"] = item["num"]

        invoice.update_one(query, {"$set": {"num" : new_num}})

        return "worked"
    elif request.method == "GET":
        old_num = invoice.find()
        query = {}
        for item in old_num:
            query["num"] = item["num"]
        return query


if __name__ == "__main__":
    app.run(debug=True)