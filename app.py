from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

DB = "database.db"

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS notes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT NOT NULL
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS todos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        todo_id INTEGER,
        text TEXT NOT NULL,
        done INTEGER NOT NULL,
        FOREIGN KEY (todo_id) REFERENCES todos(id)
    )
    """)

    conn.commit()
    conn.close()

init_db()

# Notater

@app.route("/notes", methods=["POST"])
def add_note():
    data = request.get_json()

    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute(
        "INSERT INTO notes (title, content) VALUES (?, ?)",
         (data["title"], data["content"])
    )
    conn.commit()
    conn.close()

    return jsonify ({"message": "Notat lagret"})

@app.route("/notes", methods=["GET"])
def get_note():
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("SELECT * FROM notes")
    rows = c.fetchall()

    notes = []
    for r in rows:
        notes.append({
            "id": r[0], 
            "title": r[1], 
            "content": r[2]
    })

    conn.close()
    return jsonify(notes)

# To Do - liste

@app.route("/todos", methods=["POST"])
def add_todo():
    data = request.get_json()

    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("INSERT INTO todos (title) VALUES (?)", (data["title"],))
    todo_id = c.lastrowid

    for task in data["tasks"]:
        c.execute("INSERT INTO tasks (todo_id, text, done) VALUES (?, ?, ?)",
        (todo_id, task["text"], task["done"])
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Oppgave lagret"})

@app.route("/todos", methods=["GET"])
def get_todos():
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("SELECT * FROM todos")
    todos_raw = c.fetchall()

    todos = []

    for t in todos_raw:
        c.execute("SELECT text, done FROM tasks WHERE todo_id=?", (t[0], ))
        tasks = c.fetchall()

        todos.append({
            "id": t[0],
            "title": t[1],
            "tasks": [{"text": task[0], "done": bool(task[1])} for task in tasks] 
        })

    conn.close()
    return jsonify(todos)

if __name__ == "__main__":
    app.run(debug=True)