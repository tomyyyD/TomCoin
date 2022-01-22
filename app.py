from flask import Flask
from flask import render_template

app = Flask ("BritCoin server")

@app.route('/')
def hello ():
    return render_template('homepage.html', )