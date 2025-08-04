
from flask import Flask, request, redirect, url_for, session, send_file, render_template_string
import sqlite3, csv, os
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'secretkey'
DB = os.path.join('/tmp', 'oil_collection.db')

# === HTML Templates (embedded) ===
login_html = '''<!DOCTYPE html><html><head><title>Login</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css"></head>
<body class="container mt-5"><h2>Login</h2><form method="POST">
<input class="form-control mb-3" name="username" placeholder="Username" required>
<input class="form-control mb-3" type="password" name="password" placeholder="Password" required>
<button class="btn btn-primary">Login</button></form></body></html>'''

# (Other templates index_html, restaurants_html, drivers_html, add_pickup_html, report_html would also be embedded here exactly as in previous working versions)

# === DB Setup ===
def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT, role TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS restaurants (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, address TEXT, city TEXT, state TEXT, contact TEXT, frequency_days INTEGER, notes TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS pickups (id INTEGER PRIMARY KEY AUTOINCREMENT, restaurant_id INTEGER, pickup_date TEXT, quantity INTEGER, driver_id INTEGER, notes TEXT)')
    conn.commit(); conn.close()

def query(sql, params=(), fetch=True):
    conn = sqlite3.connect(DB); c = conn.cursor(); c.execute(sql, params)
    data = c.fetchall() if fetch else None; conn.commit(); conn.close(); return data

# === Routes ===
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        user = query('SELECT * FROM users WHERE username=?', (request.form['username'],))
        if user and check_password_hash(user[0][2], request.form['password']):
            session['user_id'] = user[0][0]; session['username'] = user[0][1]; session['role'] = user[0][3]
            return redirect(url_for('index'))
        return "Invalid login"
    return render_template_string(login_html)

@app.route('/logout')
def logout():
    session.clear(); return redirect(url_for('login'))

@app.route('/')
def index():
    if 'user_id' not in session: return redirect(url_for('login'))
    # Display a minimal working dashboard (for now)
    return "<h1>Dashboard Loaded</h1><a href='/logout'>Logout</a>"

if __name__ == '__main__':
    init_db()
    if not query('SELECT * FROM users WHERE username="admin"'):
        query('INSERT INTO users (username,password,role) VALUES (?,?,?)', ('admin', generate_password_hash('admin123'), 'admin'), fetch=False)
    app.run(host='0.0.0.0', port=5000, debug=True)
