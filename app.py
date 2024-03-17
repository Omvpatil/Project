from flask import Flask, render_template
import git.quotes as quotes

app = Flask(__name__)

@app.route("/")
def home():
    quotes_list = quotes.printQuote()  
    return render_template("index.html", quotes_list=quotes_list)


if __name__ == "__main__":
    app.run(debug =True)
