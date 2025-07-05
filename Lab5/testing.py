from flask import Flask , render_template , request, redirect, url_for
import os   
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import joinedload

app = Flask(__name__)

def decor(func1):
  def inner():
    s=func1()
    return s.upper()
  return inner  
 
def decor1(func2):
  def wrapper():
    s=func2()
    return s.split()
  return wrapper  
  
def decor2(func3):
  def wrapper1():
    s=func3()
    return s.lower()
  return wrapper1
   
@decor1
@decor
@decor2
def print_s():
 return "hello world!"

print(print_s())

def My_func1(a, b):
    sum1 = a + b
    print(sum1)
def update(original_func):
    def My_func2(*args):
        My_func1(*args)          # Calls the original My_func1
        a, b = args
        print((a + b) ** 2)      # Prints the square of the sum
    return My_func2
My_func_1 = update(print_s)
My_func_1(2, 3)  # This will print 5 and then 25 (the square of the sum)

# test url_for 
from flask import url_for  

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# just testing url_for  

@app.route('/')
def index():
    return "Hello, World!"  

@app.route('/static/<path:filename>')
def static_files(filename):
    return f"Static file requested: {filename}" 


with app.app_context():
    print(url_for('static_files', filename='style.css'))  # Example usage of url_for