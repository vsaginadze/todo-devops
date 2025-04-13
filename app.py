from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DB_NAME = "todo.db"
def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                done BOOLEAN NOT NULL DEFAULT 0
            )
        ''')

@app.route("/")
def index():
    with sqlite3.connect(DB_NAME) as conn:
        tasks = conn.execute("SELECT * FROM tasks").fetchall()
    return render_template("index.html", tasks=tasks)

@app.route("/add", methods=["POST"])
def add():
    content = request.form.get("content")
    if content:
        with sqlite3.connect(DB_NAME) as conn:
            conn.execute("INSERT INTO tasks (content) VALUES (?)", (content,))
    return redirect(url_for("index"))

@app.route("/delete/<int:task_id>")
def delete(task_id):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    return redirect(url_for("index"))

@app.route("/done/<int:task_id>")
def done(task_id):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("UPDATE tasks SET done = NOT done WHERE id = ?", (task_id,))
    return redirect(url_for("index"))

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)

