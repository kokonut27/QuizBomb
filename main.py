from flask import Flask, render_template, request, flash, session, url_for, send_from_directory, redirect
from werkzeug.exceptions import abort
import json
import requests
import sqlite3

app = Flask(__name__)

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
  return render_template(
    'index.html',
    )

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
      return render_template("invalidpass.html")
    
    con = sqlite3.connect('database.db')
    c =  con.cursor() 
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='username'")
    con.commit() 
    
    if c == 1:
      return render_template("invaliduser.html")
    else:
      conn = get_db_connection()
      conn.execute("INSERT INTO posts (username, password) VALUES (?, ?)", (username, password))
      conn.commit()
      conn.close()
    return render_template("loginoutput.html", username=username, password=password)


@app.errorhandler(404)
def not_found(e):
  return render_template("404.html")

app.run(host="0.0.0.0", port=8080)