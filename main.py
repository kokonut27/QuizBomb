from flask import Flask, render_template, request, flash, session, url_for, send_from_directory, redirect
import json
import requests
import sqlite3 as sql

app = Flask(__name__)

def add_data_userpass(username, password):  
  try:
    # Connecting to database
    con = sql.connect('userpass.db')
    # Getting cursor
    c =  con.cursor() 
    # Adding data
    c.execute("INSERT INTO Shots (username, password) VALUES (%s, %s)" %(username, password))
    # Applying changes
    con.commit() 
  except:
    print("An error has occured!")

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
    for i in password:
      if i in ["`","~","!","@","#","$","%","^","&","*","(",")","[","-","_","=","+","]","{","}","\\","|",";",":","'","\"",",","<",".",">","/","?"]:
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
    return render_template("loginoutput.html", username=username, password=password)


@app.errorhandler(404)
def not_found(e):
  return render_template("404.html")

app.run(host="0.0.0.0", port=8080)