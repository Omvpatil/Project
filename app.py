import json
import os
import requests

from datetime import date
from authlib.integrations.flask_client import OAuth
from flask import Flask, render_template, request, session, redirect, url_for

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
    token = oauth.TimetableManager.authorize_access_token()
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
    today = date.today()
    reversed_date = today.strftime("%d-%m-%Y")
    day_name = today.strftime('%a')
    user_photo = session.get("picture")
    return render_template("index.html", quotes_list=quotes_list, pre_con=preCon(), today=format(reversed_date),
                           day_name=day_name,
                           photo=user_photo, pretty=json.dumps(session.get("user"), indent=4))


@app.route("/prior-tasks", methods=["GET", "POST"])
def priorTask():
    if request.method == "POST":
        taskGet = f"task :" + request.form['task'] + f"\n"
        descriptionGet: str = f"description :" + request.form['description'] + f"\n"
        with open("task.txt", "a") as file:
            file.write(f"""{taskGet}\n{descriptionGet}""")
        return render_template("prior-tasks.html", pre_con=preCon())
    return render_template("prior-tasks.html", pre_con=preCon())


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))


def fetch_profile_photo(access_token):
    personDataUrl = "https://people.googleapis.com/v1/people/me?personFields=photos"
    response = requests.get(
        personDataUrl,
        headers={
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json"
        }
    )
    if response.status_code == 200:
        data = response.json()
        if "photos" in data:
            photos = data["photos"]
            if photos:
                # Assuming the first photo is the profile photo
                return photos[0]["url"]
    return None


def preCon():
    if is_file_empty("task.txt"):
        return "No tasks remaining!"
    else:
        with open("task.txt", "r") as file:
            text = file.read()
            return text


def is_file_empty(file_path):
    return os.path.getsize(file_path) == 0


if __name__ == "__main__":
    app.run(debug=True)
