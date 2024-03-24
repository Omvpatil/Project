from flask import Flask, render_template, request, session, redirect, abort, url_for
# from flask_googleauth import GoogleAuth
import requests
import json
import quotes as quotes
import os, string, secrets
from datetime import datetime, date
from google.oauth2 import id_token
from google_auth_oauthlib import flow
from pip._vendor import cachecontrol
import google.auth.transport.requests
import pathlib
from functools import wraps

app = Flask(__name__, static_url_path='/Project/static')
app.secret_key = secrets.token_urlsafe(16)
# google_auth = GoogleAuth(app)

def generate_secret_key(length=24):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(characters) for i in range(length))

task_get =""
description_get = ""

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
client_secrets_file = os.environ.get("cs")
flow = flow.Flow.from_client_config(
    client_config={
        "web": {
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": client_secrets_file,
            "redirect_uris": ["http://127.0.0.1:5000/callback"],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://accounts.google.com/o/oauth2/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "redirect_uris": ["http://127.0.0.1:5000/callback"],
            "javascript_origins": ["http://127.0.0.1:5000"]
        }
    },
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://127.0.0.1:5000/callback",
)

def is_file_empty(file_path):
    return os.path.getsize(file_path) == 0

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

def login_is_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return redirect("/login")  # Redirect to login page if not authenticated
        return function(*args, **kwargs)
    return wrapper


@app.route('/login')
def login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/callback')
def callback():
    authorization_response = request.url
    if not session["state"] == request.args["state"]:
        abort(500)
    
    try:
        flow.fetch_token(authorization_response=authorization_response)
    except Exception as e:
        print("Error fetching token:", e)
        abort(500)
    credentials = flow.credentials
    request_session = requests.Session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)
    
    id_info = id_token.verify_oauth2_token(
        id_token = credentials._id_token,
        request = token_request,
        audience = GOOGLE_CLIENT_ID
        
    )
    
    # auth = google.auth.transport.requests.AuthorizedSession(credentials)
    # user_info = auth.get_user_info()
    # name = user_info['name']
    name = id_info.get("name")

    return redirect("/",name)



@app.route("/")
@login_is_required
def home():
    global quotes_list
    quotes_list = quotes.printQuote() 
    today = date.today()
    day_name = today.strftime('%a') 
    render = "index.html"
    name = user.email.split('@')[0]
    return render_template(render, quotes_list=quotes_list, pre_con = preCon(),today = today,day_name = day_name,name = name)


@app.route("/prior-tasks", methods=["GET", "POST"])
def priorTask():
    if request.method == "POST":
        task_get =f"task :"+ request.form['task'] + f"\n"
        description_get = f"description :" +request.form['description']+f"\n"
        with open("task.txt", "a") as file:
            file.write(task_get + "\n" + description_get)
            file.write("_div_")
        return render_template("prior-tasks.html", pre_con = preCon())
    return render_template("prior-tasks.html",pre_con = preCon())


if __name__ == "__main__":
    app.run(debug =True)
