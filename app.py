from flask import Flask, render_template, request, redirect
import mysql.connector
from datetime import datetime

app = Flask(_name_)

# Connect to MySQL
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # default for XAMPP
        database="crime_db"
    )

@app.route('/')
def index():
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM criminals")
    criminals = cursor.fetchall()
    db.close()
    return render_template('index.html', criminals=criminals)

@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    age = request.form['age']
    crime_type = request.form['crime_type']
    status = request.form['status']

    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute("INSERT INTO criminals (name, age, crime_type, status) VALUES (%s, %s, %s, %s)",
                   (name, age, crime_type, status))
    cursor.execute("INSERT INTO logs (action) VALUES (%s)", (f"Added criminal: {name}",))
    db.commit()
    db.close()

    return redirect('/')

if _name_ == '_main_':
    app.run(debug=True)