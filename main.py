from flask import Flask, render_template, request, flash, session, url_for, send_from_directory, redirect
from werkzeug.exceptions import abort
from flask_session import Session
import json
import requests
import sqlite3
import os

app = Flask(__name__,
            static_url_path='', 
            static_folder='static',
            template_folder='templates')
app.config["SECRET_KEY"] = os.environ["key"]
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_post(name):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE name = ?',
                        (name, )).fetchone()
    conn.close()
    if post == None:
      abort(404)
    return post


@app.route('/')
def index():
  try:
    userexists = session.get("user_exists")
  except:
    pass
  return render_template(
    'index.html',
    userexists=userexists)

@app.route('/login')
def login():
  return render_template("login.html")

@app.route('/login', methods = ["GET", "POST"])
def loginrequest():
  if request.method == "POST":
    username = request.form["username"]
    password = request.form["password"]

    check_pass = []
    special_chars = ["`","~","!","@","#","$","%","^","&","*","(",")","[","-","_","=","+","]","{","}","\\","|",";",":","'","\"",",","<",".",">","/","?"]
    for i in password:
      check_pass.append(i)
    if any(i in s for s in special_chars):#i in ["`","~","!","@","#","$","%","^","&","*","(",")","[","-","_","=","+","]","{","}","\\","|",";",":","'","\"",",","<",".",">","/","?"]:
      special_char = True
    else:
      special_char = False
    if special_char:
      if len(password) >= 7:
        passworks = True
      else:
        passworks = False
    else:
      passworks = False
    if passworks != True:
      flash("Invalid password! The password must include at least 7 characters and havea special character! Try again in a few seconds!")
    
    con = sqlite3.connect('database.db')
    c =  con.cursor() 
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='username'")
    con.commit() 
    
    if c == 1:
      flash("Invalid username! It already exists! Try again in a few seconds!")
    else:
      conn = get_db_connection()
      conn.execute("INSERT INTO posts (username, password) VALUES (?, ?)", (username, password))
      conn.commit()
      conn.close()
      session["user_exists"] = True
    return redirect(url_for('index'))

@app.route('/play')
def play():
  return render_template("play.html")

@app.errorhandler(404)
def not_found(e):
  return render_template("404.html")

app.run(host="0.0.0.0", port=5050)