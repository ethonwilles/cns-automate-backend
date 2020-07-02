from flask import Flask, request
from flask_cors import CORS
from flask_heroku import Heroku
import pymongo
import json
import os
from dotenv import load_dotenv
from twilio.rest import Client



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



@app.route("/todo-check" , methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
def todo_check():
    todo = mydb["ToDo"]

    if request.method == "POST":
        task = request.json["task"]
        complete = request.json["completed"]
        date = request.json["date"]
        insert = todo.insert_one({"todo" :{"completed" : complete, "task" : task, "date" : date}})
        return f"{insert}"

    if request.method == "GET":
        items = todo.find()
        list_of = []
        for item in items:
            list_of.append(item["todo"])
        return {"items" : list_of}
    if request.method == "PUT":
        task = request.json["task"]
        complete = request.json["completed"]
        date = request.json["date"]
        myquery = {"todo" : {"completed" : False, "task" : task, "date" : date}}
        new_values = {"$set" :{ "todo": {"completed" : True, "task" : task, "date" : date}}}
        todo.update_one(myquery, new_values)
        client = Client(os.getenv("account_sid"), os.getenv("twilio_auth"))
        message = client.messages.create(
            to="+18017068523",
            from_=f"{os.getenv('number')}",
            body=f"Task: '{task}' was marked as completed today."
        )
        
        return f"worked"
    
        
    if request.method == "DELETE":
        task = request.json["task"]
        complete = request.json["completed"]
        date = request.json["date"]
        myquery = {"todo" : {"completed" : complete, "task" : task, "date" : date}}

        todo.delete_one(myquery)
        return "worked"
    
@app.route("/push-todo", methods=["POST"])
def push():
    todo = mydb["ToDo"]
    task = request.json["task"]
    complete = request.json["completed"]
    old_date = request.json["old_date"]
    new_date = request.json["new_date"]
    myquery = {"todo" : {"completed" : complete, "task" : task, "date" : old_date}}
    new_values = {"$set" :{ "todo": {"completed" : complete, "task" : task, "date" : new_date}}}
    todo.update_one(myquery, new_values)
    return "worked"

@app.route("/hours", methods=["GET", "POST", "PUT"])
def hours():
    hoursdb = myclient["Hours"]
    employee = request.json["employee"]
    if request.method == "GET":
        user = hoursdb[employee]
        data = []
        temp_data = {}
        items = user.find()
        for item in items:
            temp_data["date"] = item["date"]
            temp_data["hours"] = item["hours"]
            data.append(temp_data)
        return {"items" : data}
    if request.method == "POST":
        user = hoursdb[employee]
        date = request.json["date"]
        hours = request.json["hours"]
        query = {"date" : date, "hours" : hours}
        user.insert_one(query)
        items = user.find({"date" : date, "hours" : hours})
        data = {}
        for item in items:
            data["date"] = item["date"]
            data["hours"] = item["hours"]
        return data
@app.route("/fetch-hours", methods=["GET"])
def fetch_hours():
    hoursdb = myclient["Hours"]
    items = hoursdb.list_collection_names()
    
    return {"names" : items}
if __name__ == "__main__":
    app.run(debug=True, port=6000)