from flask import Flask, request, redirect, url_for, session, send_file, render_template_string
import sqlite3, csv, os
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'secretkey'
DB = os.path.join('/tmp', 'oil_collection.db')

# (The rest of the code remains unchanged from the single-file version)
# For brevity, assume the entire single-file content from the previous version is here.
