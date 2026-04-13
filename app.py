from flask import Flask, jsonify, request, render_template_string
import sqlite3
from datetime import datetime

app = Flask(__name__)

DB = "app.db"

# Database
def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cur = conn.cursor()

    # Notater
    cur.execute("""
    CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        content TEXT,
        category TEXT,
        pinned INTEGER DEFAULT 0,
        created_at TEXT
    )
    """)

    # To Dos
    cur.execute("""
    CREATE TABLE IF NOT EXISTS todos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT,
        done INTEGER DEFAULT 0
    )
    """)

    conn.commit()
    conn.close()

init_db()

# Frontend
HTML = """
<!DOCTYPE html>
<html lang="no">
<head>
<meta charset="UTF-8">
<title>Notatapplikasjon</title>

<style>
* {
    box-sizing: border-box;
}

body {
    margin-left: 20rem;
    margin-right: 20rem;
    font-family: "Segoe UI", Arial, sans-serif;
    background: linear-gradient(135deg, #eef2ff, #f8fafc);
    color: #111;
}

.container {
    max-width: 500px;
    margin: 40px auto;
    padding: 20px;
}

h1 {
    text-align: center;
    margin-bottom: 30px;
}

.card {
    background: white;
    padding: 16px;
    border-radius: 14px;
    margin-bottom: 15px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.08);
    transition: 0.2s;
}

.card:hover {
    transform: translateY(-2px);
}

input, textarea, select {
    width: 100%;
    padding: 10px;
    margin-bottom: 10px;
    border-radius: 10px;
    border: 1px solid #ccc;
    font-size: 14px;
}

button {
    border: none;
    border-radius: 10px;
    padding: 8px 12px;
    margin-right: 5px;
    cursor: pointer;
    font-weight: 600;
    transition: 0.2s;
}

.btn-primary {
    background: #3b82f6;
    color: white;
}

.btn-primary:hover {
    background: #2563eb;
}

.btn-delete {
    background: #ef4444;
    color: white;
}

.btn-delete:hover {
    background: #dc2626;
}

.btn-success {
    background: #22c55e;
    color: white;
}

.btn-success:hover {
    background: #16a34a;
}

.btn-secondary {
    background: #e5e7eb;
}

.done {
    text-decoration: line-through;
    color: #16a34a;
    font-weight: bold;
}

.row {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

small {
    color: #666;
}

.dark {
    background: #1e1e1e;
    color: #eee;
}

.dark .card {
    background: #2c2c2c;
}

</style>
</head>

<body>

<div class="container">

<h1>Notatapplikasjon</h1>
<button onclick="toggleDark()">Mørk modus</button>

<h2>Notater</h2>

<input id="title" placeholder="Tittel">
<textarea id="content" placeholder="Innhold"></textarea><br>
<input id="category" placeholder="Kategori">

<button class="btn-primary" onclick="addNote()">Legg til</button>

<div id="notes"></div>

<h2>Todos</h2>

<input id="todoInput" placeholder="Ny oppgave">
<button class="btn-primary" onclick="addTodo()">Legg til</button>

<select id="filter" onchange="loadTodos()">
<option value="all">Alle</option>
<option value="done">Ferdige</option>
<option value="active">Aktive</option>
</select>

<div id="todos"></div>

</div>

<script>

function toggleDark() {
    document.body.classList.toggle("dark");
}

// Notater

async function loadNotes() {
    const res = await fetch("/notes");
    const notes = await res.json();

    const div = document.getElementById("notes");
    div.innerHTML = "";

    notes.forEach(n => {
        div.innerHTML += `
        <div class="card">
            <b>${n.title}</b> ${n.pinned ? "Festet" : ""}<br>
            <small>${n.category || "" } | ${n.created_at}</small><br><br>
            ${n.content}<br><br>

            <button class="btn-success" onclick="pin(${n.id})">Fest</button>
            <button class="btn-secondary" onclick="editNote(${n.id})">Rediger</button>
            <button class="btn-delete" onclick="deleteNote(${n.id})">Slett</button>
        </div>
        `;
    });
}

async function addNote() {
    const title = document.getElementById("title").value;
    const content = document.getElementById("content").value;
    const category = document.getElementById("category").value;

    await fetch("/notes", {
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body: JSON.stringify({title, content, category})
    });

    loadNotes();
}

async function deleteNote(id){
    await fetch("/notes/"+id,{method:"DELETE"});
    loadNotes();
}

async function pin(id){
    await fetch("/notes/"+id+"/pin",{method:"PATCH"});
    loadNotes();
}

async function editNote(id){
    const title = prompt("Ny tittel:");
    const content = prompt("Nytt innhold:");

    await fetch("/notes/"+id,{
        method:"PUT",
        headers:{"Content-Type":"application/json"},
        body: JSON.stringify({title, content})
    });

    loadNotes();
}

// To Dos

async function loadTodos(){
    const filter = document.getElementById("filter").value;
    const res = await fetch("/todos");
    let todos = await res.json();

    if(filter==="done") todos = todos.filter(t=>t.done);
    if(filter==="active") todos = todos.filter(t=>!t.done);

    const div = document.getElementById("todos");
    div.innerHTML="";

    todos.forEach((t,i)=>{
        div.innerHTML+=`
        <div class="card">
            <span class="${t.done?"done":""}">${t.task}</span><br><br>
            <button class="btn-success" onclick="toggle(${t.id})">Utført</button>
            <button class="btn-secondary" onclick="editTodo(${t.id})">Rediger</button>
            <button class="btn-delete" onclick="deleteTodo(${t.id})">Slett</button>
        </div>
        `;
    });
}

async function addTodo(){
    const task = document.getElementById("todoInput").value;

    await fetch("/todos",{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body: JSON.stringify({task})
    });

    loadTodos();
}

async function toggle(id){
    await fetch("/todos/"+id+"/toggle",{method:"PATCH"});
    loadTodos();
}

async function deleteTodo(id){
    await fetch("/todos/"+id,{method:"DELETE"});
    loadTodos();
}

async function editTodo(id){
    const task = prompt("Ny tekst:");
    await fetch("/todos/"+id,{
        method:"PUT",
        headers:{"Content-Type":"application/json"},
        body: JSON.stringify({task})
    });
    loadTodos();
}

loadNotes();
loadTodos();

</script>
</body>
</html>
"""

@app.route("/")
def index():
    return HTML 

# Notater

@app.route("/notes", methods=["GET"])
def get_notes():
    conn = get_db()
    notes = conn.execute("SELECT * FROM notes ORDER BY pinned DESC, id DESC").fetchall()
    conn.close()
    return jsonify([dict(n) for n in notes])

@app.route("/notes", methods=["POST"])
def add_note():
    data = request.json
    conn = get_db()
    conn.execute("""
        INSERT INTO notes (title, content, category, created_at)
        VALUES (?, ?, ?, ?)
    """, (
        data["title"],
        data["content"],
        data.get("category", ""),
        datetime.now().strftime("%Y-%m-%d %H:%M")
    ))
    conn.commit()
    conn.close()
    return "", 201

@app.route("/notes/<int:id>", methods=["DELETE"])
def delete_note(id):
    conn = get_db()
    conn.execute("DELETE FROM notes WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return ""

@app.route("/notes/<int:id>/pin", methods=["PATCH"])
def pin_note(id):
    conn = get_db()
    conn.execute("""
        UPDATE notes
        SET pinned = NOT pinned
        WHERE id=?
    """, (id,))
    conn.commit()
    conn.close()
    return ""

@app.route("/notes/<int:id>", methods=["PUT"])
def edit_note(id):
    data = request.json
    conn = get_db()
    conn.execute("""
        UPDATE notes
        SET title=?, content=?
        WHERE id=?
    """, (data["title"], data["content"], id))
    conn.commit()
    conn.close()
    return ""

# To Dos

@app.route("/todos", methods=["GET"])
def get_todos():
    conn = get_db()
    todos = conn.execute("SELECT * FROM todos ORDER BY id DESC").fetchall()
    conn.close()
    return jsonify([dict(t) for t in todos])

@app.route("/todos", methods=["POST"])
def add_todo():
    data = request.json
    conn = get_db()
    conn.execute("INSERT INTO todos (task) VALUES (?)", (data["task"],))
    conn.commit()
    conn.close()
    return ""

@app.route("/todos/<int:id>/toggle", methods=["PATCH"])
def toggle_todo(id):
    conn = get_db()
    conn.execute("""
        UPDATE todos
        SET done = NOT done
        WHERE id=?
    """, (id,))
    conn.commit()
    conn.close()
    return ""

@app.route("/todos/<int:id>", methods=["DELETE"])
def delete_todo(id):
    conn = get_db()
    conn.execute("DELETE FROM todos WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return ""

@app.route("/todos/<int:id>", methods=["PUT"])
def edit_todo(id):
    data = request.json
    conn = get_db()
    conn.execute("UPDATE todos SET task=? WHERE id=?", (data["task"], id))
    conn.commit()
    conn.close()
    return ""

# Kjør
if __name__ == "__main__":
    app.run(debug=True)



