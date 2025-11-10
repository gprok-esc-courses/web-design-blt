from flask import Flask, request, render_template, flash, session, redirect
import sqlite3 
import hashlib 

app = Flask(__name__)
app.secret_key = "akjdsbkjas&^absdjkajbdkasbdksajbdksadbkbj"

def get_db_conn():
    db = sqlite3.connect('task_manager.db')
    db.row_factory = sqlite3.Row
    return db 


def initialize_db():
    db = get_db_conn()
    cursor = db.cursor() 

    cursor.execute("PRAGMA foreign_keys=ON")

    # Users table
    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL, 
                        password TEXT NOT NULL,
                        role TEXT DEFAULT 'member',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                   """)
    
    # Projects table 
    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS projects (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        description TEXT,  
                        user_id INTEGER NOT NULL, 
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users (id)
                    )
                   """)
    
    # Tasks table 
    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS tasks (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        description TEXT, 
                        project_id INTEGER NOT NULL,
                        completed INTEGER DEFAULT 0,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (project_id) REFERENCES projects (id)
                    )        
                   """)
    
    db.commit()
    db.close()


def hash_password(username, password):
    pw = username + password
    hashed = hashlib.sha512(pw.encode('utf-8')).hexdigest()
    return hashed


@app.route('/')
def home():
    return "HOME PAGE"


@app.route('/register', methods=[ 'GET', 'POST' ])
def register():
    username = ''
    db = get_db_conn()
    cursor = db.cursor()
    if request.method == 'POST':
        # return(f"{request.form['username']} {request.form['password']} {request.form['password2']}")
        username = request.form['username']
        password = request.form['password']
        password2 = request.form['password2']
        if password != password2:
            flash("ERROR: Passwords do not match")
            return render_template('register_form.html', username=username)
        else:
            user = cursor.execute("SELECT * FROM users WHERE username=?", (username,)).fetchone()
            if user:
                flash("ERROR: Username is taken")
                return render_template('register_form.html', username=username)
            else: 
                hashed_password = hash_password(username, password)
                cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                               (username, hashed_password))
                db.commit()
                return redirect('/')
    else:
        return render_template('register_form.html', username=username)



if __name__ == '__main__':
    initialize_db()
    app.run(debug=True)