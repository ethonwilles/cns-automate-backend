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
CORS(app)
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



@app.route("/todo-check" , methods=["GET", "POST"])
def todo_check():
    todo = mydb["ToDo"]

    if request.method == "POST":
        task = request.json["task"]
        complete = request.json["completed"]
        insert = todo.insert_one({"todo" :{ "task" : task, "completed" : complete}})
        return f"{insert}"

    if request.method == "GET":
        items = todo.find()
        list_of = []
        for item in items:
            list_of.append(item["todo"])
        return {"items" : list_of}

if __name__ == "__main__":
    app.run(debug=True)