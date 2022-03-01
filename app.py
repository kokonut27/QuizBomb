from flask import Flask, render_template, request, flash, url_for, send_from_directory, redirect, jsonify
from werkzeug.exceptions import abort
from replit import db
import sqlite3
import markdown2
import json
import random
import os

app = Flask(__name__,
            static_url_path='', 
            static_folder='static',
            template_folder='templates')
app.config["SECRET_KEY"] = os.environ["key"]


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM quizzes WHERE id = ?',
                        (post_id, )).fetchone()
    conn.close()
    if post == None:
        abort(404)
    return post


f = open('questions.json')
questions = json.load(f)
topics = ['example-question', 'coding', 'math', 'created-by', 'english', 'science', 'history', 'fun', 'gaming', 'random']
# db["username"] = []
# print(db["username"])

@app.route('/')
@app.route('/home')
def index():
  userexists = db["username"]
  conn = get_db_connection()
  quizzes = conn.execute('SELECT * FROM quizzes').fetchall()
  conn.close()

  quizzes = list(reversed(quizzes))
  
  def post(post_id):
    post = get_post(post_id)
    return post["id"]
  
  id = 0
  
  for quiz in quizzes:
    id += 1
    try:
      if post(id):
        db["quizzes"][post(id)] = 
      else:
        abort(404)
    except:
      abort(404)
  return render_template(
    'index.html',
    userexists=userexists,
    quizzes=quizzes
  )

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
    db["username"].append(username)
  return redirect(url_for('index'))

@app.route('/explore')
def explore():
  all_posts = db["posts"]

  for posts in all_posts:
    pass
  
  return render_template(
    "explore.html",
    questions=questions,
    posts=posts
    )

@app.route('/join', methods = ["POST", "GET"])
def join():
  if request.method == "GET":
    return render_template("join.html")
  
  if request.method == "POST":
    pass

@app.errorhandler(404)
def not_found(e):
  return render_template("404.html")

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=8080)