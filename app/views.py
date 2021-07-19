from app import app

from flask import Flask,render_template


@app.route('/')
def home():
    return render_template("home.html")

@app.route('/acltest')
def acltest():
    return render_template("acltest.html")