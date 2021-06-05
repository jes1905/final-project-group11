from flask import Flask, redirect, url_for, request, render_template, current_app as app
import requests
from sense_hat import SenseHat
from time import sleep
from flask_apscheduler import APScheduler
import sys
import sqlite3

app = Flask(__name__)

@app.route('/', methods = ["GET", "POST"])
def index():
    conn = sqlite3.connect('./static/data/entries.db')
    curs = conn.cursor()
    entries = []
    rows = curs.execute("SELECT * from entries")
    for row in rows:
        entry = {'entry':row[0], 'date':row[1]}
        entries.append(entry)
    conn.close()
    return render_template('journal.html', entries = entries)

@app.route('/journal', methods = ["GET", "POST"])
def journal():
    entry = request.form['entry']
    date = request.form['date']
    conn = sqlite3.connect('./static/data/entries.db')
    curs = conn.cursor()
    curs.execute("INSERT INTO entries(entry, date) VALUES((?),(?))",(entry,date))
    conn.commit()
    conn.close()
    conn = sqlite3.connect('./static/data/entries.db')
    curs = conn.cursor()
    entries = []
    rows = curs.execute("SELECT * from entries")
    for row in rows:
        entry = {'entry':row[0], 'date':row[1]}
        entries.append(entry)
    conn.close()
    return render_template('journal.html', entry = entry, date = date, entries = entries)




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')