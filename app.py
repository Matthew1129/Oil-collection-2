from flask import Flask, request, redirect, url_for, session, send_file, render_template_string
import sqlite3, csv, os
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'secretkey'
DB = os.path.join('/tmp', 'oil_collection.db')

# === Embedded HTML templates (login_html, index_html, restaurants_html, drivers_html, add_pickup_html, report_html) ===
# (Using the same HTML strings as in the previous single-file version)
# For brevity, we assume all embedded HTML variables are defined here as in the working single-file version

# ---- Database Initialization ----
def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT, role TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS restaurants (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, address TEXT, city TEXT, state TEXT, contact TEXT, frequency_days INTEGER, notes TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS pickups (id INTEGER PRIMARY KEY AUTOINCREMENT, restaurant_id INTEGER, pickup_date TEXT, quantity INTEGER, driver_id INTEGER, notes TEXT)')
    conn.commit()
    conn.close()

def query(sql, params=(), fetch=True):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute(sql, params)
    data = c.fetchall() if fetch else None
    conn.commit()
    conn.close()
    return data

# ---- Routes (login, logout, index, restaurants, drivers, add_pickup, report) ----
# (The full logic here is the same as in the previous single-file working version with embedded templates)

if __name__ == '__main__':
    init_db()
    if not query('SELECT * FROM users WHERE username="admin"'):
        query('INSERT INTO users (username,password,role) VALUES (?,?,?)', ('admin', generate_password_hash('admin123'), 'admin'), fetch=False)
    app.run(host='0.0.0.0', port=5000, debug=True)
