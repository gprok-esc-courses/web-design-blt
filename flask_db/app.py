from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

conn = sqlite3.connect('blog.db')
cursor = conn.cursor()
cursor.execute("""
               CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
               )
               """)



@app.route('/')
def home():
    return render_template('home.html')

@app.route('/blog')
def blog():
    db = sqlite3.connect('blog.db')
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    posts = cursor.execute("SELECT * FROM posts ORDER BY created_at DESC").fetchall()
    db.close()
    return render_template('blog.html', posts=posts)

@app.route('/edit/post/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id): 
    if request.method == 'POST':
        try:
            data = request.form
            db = sqlite3.connect('blog.db')
            cursor = db.cursor()
            cursor.execute("""UPDATE posts 
                              SET title = ?, content = ?
                              WHERE id = ?
                           """, (data['title'], data['content'], post_id))
            db.commit()
            db.close()
            return redirect('/blog')
        except:
            return "ERROR: Unable to update post"
    else:
        data = request.form
        db = sqlite3.connect('blog.db')
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        post = cursor.execute("SELECT * FROM POSTS WHERE id = ?", (post_id,)).fetchone()
        return render_template('edit_post.html', post=post)


@app.route('/add/post', methods=['GET', 'POST'])
def add_post():
    if request.method == 'POST':
        try:
            data = request.form
            db = sqlite3.connect('blog.db')
            cursor = db.cursor()
            cursor.execute("""INSERT INTO posts (title, content)
                            VALUES (?, ?)
                        """, (data['title'], data['content']))
            db.commit()
            db.close()
            return redirect('/blog')
        except:
            return "ERROR: Unable to add post"
    else:
        return render_template('add_post.html')
    

@app.route('/delete/post/<int:post_id>')
def delete_post(post_id):
    try:
        db = sqlite3.connect('blog.db')
        cursor = db.cursor()
        cursor.execute("DELETE FROM posts WHERE id = ?", (post_id,))
        db.commit()
        db.close()
        return redirect('/blog')
    except:
        return "ERROR: Unable to delete post"



if __name__ == '__main__':
    app.run(debug=True)