from replit import db
import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
  connection.executescript(f.read())

cur = connection.cursor()

"""
questions = {
  "question-1": {
    "topic": "example-question", 
    "question": "How is QuizBomb so far?", 
    "answer": None
  }, 
  "question-2": {
    "topic": "example-question", 
    "question": "Are you having fun with QuizBomb?", 
    "answer": None
  }
}
"""
questions = db["quizzes"][1]

cur.execute("INSERT INTO quizzes (title, topic, displayContent) VALUES (?, ?, ?)", ('Welcome to QuizBomb!', 'example-quiz', 'Welcome to QuizBomb! We hope you have lots of fun here, and we hope you enjoy!',))

connection.commit()
connection.close()