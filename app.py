from flask import Flask, render_template, request
import json
import quotes as quotes
import os
from datetime import datetime, date


def is_file_empty(file_path):
    return os.path.getsize(file_path) == 0

app = Flask(__name__, static_url_path='/Project/static')
task_get =""
description_get = ""

def preCon():
    pre_con = []
    del pre_con
    f = open("task.txt","r")
    if is_file_empty("task.txt"):
        pre_con = "No tasks remaining !"
    else:
        with open("task.txt", "r") as file:
            pre_con = file.read()
    return pre_con

@app.route("/")
def home():
    login()
    global quotes_list
    quotes_list = quotes.printQuote() 
    today = date.today()
    day_name = today.strftime('%a') 
    render = "index.html"
    return render_template(render, quotes_list=quotes_list, pre_con = preCon(),today = today,day_name = day_name)

@app.route("/login",methods=["POST"])
def login():

    return render_template("login.html")
    
@app.route("/prior-tasks", methods=["GET", "POST"])
def priorTask():
    if request.method == "POST":
        task_get =f"task :"+ request.form['task'] + f"\n"
        description_get = f"description :" +request.form['description']+f"\n"
        with open("task.txt", "a") as file:
            file.write(task_get)
            file.write(description_get)
            file.write("\n")
        return render_template("prior-tasks.html", pre_con = preCon())
    return render_template("prior-tasks.html",pre_con = preCon())

if __name__ == "__main__":
    app.run(debug =True)
