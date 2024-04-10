import os
import requests
import json
import AI_coatch

from datetime import date
from authlib.integrations.flask_client import OAuth
from flask import Flask, render_template, request, session, redirect, url_for, jsonify

import quotes as quotes

app = Flask(__name__, static_url_path='/static')

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
client_secrets_file = os.environ.get("cs")

appConf = {
    "OAUTH2_META_URL": "https://accounts.google.com/o/oauth2/v2/auth",
    "FLASK_SECRET": "1oifin0inOIFNi1i112323-ca0im",
    "FLASK_PORT": 5000
}
app.secret_key = appConf.get("FLASK_SECRET")
scopes = ["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email",
          "openid"],
redirect_uri = "http://127.0.0.1:5000/callback",

oauth = OAuth(app)
oauth.register(
    name='google',
    client_id=GOOGLE_CLIENT_ID,
    client_secret=client_secrets_file,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid profile https://www.googleapis.com/auth/userinfo.profile'
    }
)


@app.route('/google-login')
def google_login():
    google = oauth.create_client('google')  # Use a descriptive name for clarity
    redirect_uri = url_for('googleCallback', _external=True)
    return google.authorize_redirect(redirect_uri)


@app.route('/callback')
def googleCallback():
    token = oauth.google.authorize_access_token()
    session["user"] = token
    personDataUrl = "https://www.googleapis.com/oauth2/v1/userinfo"
    personData = requests.get(
        personDataUrl,
        headers={
            "Authorization": f"Bearer {token["access_token"]}"
        }
    ).json()
    token["personData"] = personData
    profile_picture_url = personData.get('picture')
    session["picture"] = profile_picture_url

    return redirect(url_for("home"))


@app.route("/")
def home():
    quotes_list = quotes.printQuote()
    name, user_photo = userDataProfile()
    reversed_date, day_name = Date()

    return render_template("index.html", quotes_list=quotes_list, pre_con=preCon(), today=reversed_date,
                           day_name=day_name,
                           photo=user_photo, pretty=name)


@app.route("/prior-tasks", methods=["GET", "POST"])
def priorTask():
    today = date.today()
    reversed_date, day_name = Date()
    name, user_photo = userDataProfile()

    if request.method == "POST":
        task = request.form['task']
        description = request.form['description']

        task_data = {
            'task': task,
            'description': description
        }

        try:
            with open("task.json", "r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            data = []

        data.append(task_data)
        with open("task.json", "w") as file:
            json.dump(data, file, indent=4)

    return render_template("prior-tasks.html", pre_con=preCon(), today=reversed_date,
                           day_name=day_name, photo=user_photo, pretty=name)


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))


@app.route("/ai-coach", methods=["GET", "POST"])
def ai():
    if request.form.get("description"):
        prompt = request.form.get("description")
    else:
        prompt = "Tell me about how to maintain timetable for longer periods"
    responseAi = AI_coatch.generate_prompt(prompt)
    return render_template("/ai-coach.html", responseAi=responseAi)


@app.route("/calender", methods=["GET", "POST"])
def calender():
    with open('events.json') as i:
        event_data = json.load(i)
    Evnt = f"{request.form.get('event')}"
    StrTim = f"{request.form.get('start')}"
    EndTim = f"{request.form.get('end')}"
    Dscr = f"{request.form.get('description')}"
    new_event = {
        "event_name": Evnt,
        "start_time": StrTim,
        "end_time": EndTim,
        "describe": Dscr
    }
    if all([Evnt, StrTim, EndTim, Dscr]):
        event_data.append(new_event)
        with open("events.json", 'w') as file:
            json.dump(new_event, file, indent=4)
    name, user_photo = userDataProfile()
    reversed_date, day_name = Date()

    return render_template('calender.html', today=reversed_date, day_name=day_name,
                           photo=user_photo, pretty=name, calendar_events=event_data)


def preCon():
    with open("task.json", "r") as file:
        tasks = json.load(file)
    return tasks


def userDataProfile():
    user_photo = session.get("picture")
    nameData = session.get("user")
    name = ""
    user_photo = None

    if nameData:
        name = nameData.get("personData", {}).get("name")
        user_photo = session.get("picture")
    return name, user_photo


def is_file_empty(file_path):
    return os.path.getsize(file_path) == 0


def Date():
    today = date.today()
    reversed_date = today.strftime("%d-%m-%Y")
    day_name = today.strftime('%a')
    return format(reversed_date), day_name


if __name__ == "__main__":
    app.run(debug=True)
