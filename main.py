from flask import Flask, render_template, request, flash, session, url_for, send_from_directory, redirect, jsonify
from werkzeug.exceptions import abort
from flask_session import Session
from replit import db
import json
import random
import os

app = Flask(__name__,
            static_url_path='', 
            static_folder='static',
            template_folder='templates')
app.config["SECRET_KEY"] = os.environ["key"]
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

f = open('questions.json')
questions = json.load(f)
topics = ['example-question', 'coding', 'math', 'created-by', 'english', 'science', 'history', 'fun']
# db["username"] = []
# print(db["username"])

@app.route('/')
@app.route('/home')
def index():
  userexists = session.get("user_exists")
  return render_template(
    'index.html',
    userexists=userexists)

@app.route('/login')
def login():
  return render_template("login.html")

@app.route('/login', methods = ["GET", "POST"])
def loginrequest():
  if request.method != "POST":
      return

  username = request.form["username"]
  password = request.form["password"]

  check_pass = []
  special_chars = ["`","~","!","@","#","$","%","^","&","*","(",")","[","-","_","=","+","]","{","}","\\","|",";",":","'","\"",",","<",".",">","/","?"]
  for i in password:
    check_pass.append(i)
  special_char = any(i in s for s in special_chars)
  passworks = special_char and len(password) >= 7
  if not passworks:
    flash("Invalid password! The password must include at least 7 characters and have a special character! Try again in a few seconds!")

  if username in db["username"]:
    flash("Invalid username! It already exists! Try again in a few seconds!")
  else:
    session["user_exists"] = True
    db["username"].append(username)
  return redirect(url_for('index'))

@app.route('/play')
def play():
  return render_template(
    "play.html",
    questions=questions
    )

@app.errorhandler(404)
def not_found(e):
  return render_template("404.html")

app.run(host="0.0.0.0", port=8080)