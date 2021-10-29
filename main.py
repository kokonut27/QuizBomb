from flask import Flask, render_template, request, flash, session, url_for, send_from_directory, redirect
import json, requests

app = Flask(__name__)

@app.route('/')
def index():
  return render_template(
    'index.html',
    )

@app.route('/login')
def login():
  return render_template("login.html")

@app.route('/login', methods = ["GET", "POST"])
def loginrequest():
  if request.method == "POST":
    yn = request.form["playnow"]
  
  return redirect(url_for('login'))


app.run(host="0.0.0.0", port=8080)