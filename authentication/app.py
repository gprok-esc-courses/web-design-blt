from flask import Flask, render_template, request, redirect, session, flash
from hashlib import md5 
import sqlite3
from functools import wraps

app = Flask(__name__) 
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = "ldjfhdskjfshkjfdskjfhsdkjshfkjshkjfdsfdskjdsh"

def get_db_cursor():
    db = sqlite3.connect('data.db')
    db.row_factory = sqlite3.Row 
    cursor = db.cursor()
    return cursor 

db = sqlite3.connect('data.db')
cursor = db.cursor()
cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    role TEXT,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
               """)

def roles_permitted(roles):
     def decorator(f):
         @wraps(f) 
         def wrapper(*args, **kwargs):
             if 'userid' in session and session['role'] in roles:
                 return f(*args, **kwargs)
             else:
                 role_str = ''.join(role + ' ' for role in roles)
                 flash("Need to login to access this page with role " + role_str)
                 return redirect('/login')
         return wrapper
     return decorator


@app.route('/')
def home():
    return ("HOME")


@app.route('/register', methods=[ 'GET', 'POST' ])
def register():
    # if POST
        # Get form data
        # Check that username is not in DB
        # IF not hash the password and insert new user
    # if GET 
        # Display the Register form
    return ("REGISTER")


@app.route('/login', methods=[ 'GET', 'POST' ])
def login():
    if request.method == 'POST':
        data = request.form
        username = data['username']
        password = data['password']
        
        cursor = get_db_cursor()
        user = cursor.execute("SELECT * FROM users WHERE username=?", (username,)).fetchone()
        if user:
            hashed = md5((username + password).encode('utf-8')).hexdigest()
            if user['password'] == hashed:
                session.clear()
                session['userid'] = user['id']
                session['role'] = user['role']

                if user['role'] == 'member':
                    return redirect('/profile')
                elif user['role'] == 'admin':
                    return redirect('/dashboard')
                else:
                    return "Invalid role"
            else:
                return "Invalid credentials"
        else: 
            return "User not found"
    return render_template('login.html')


@app.route('/profile')
@roles_permitted(['member'])
def profile():
    cursor = get_db_cursor()
    user = cursor.execute("SELECT * FROM users WHERE id=?", (session['userid'],)).fetchone()
    if user:
        return render_template('profile.html', user=user)
    else:
        flash("User " + session['userid'] + " not found")
        return redirect('/login')
    


@app.route('/dashboard')
@roles_permitted(['admin'])
def dashboard():
    return render_template('dashboard.html')
    

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


if __name__ == '__main__':
    app.run(debug=True)