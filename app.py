from flask import Flask, jsonify, request, render_template_string
import json
import os
from datetime import datetime

app = Flask(__name__)

DATA_FILE = "data.json"

# Lagre data
def load_data():
    if not os.path.exists(DATA_FILE):
        return {"notes": [], "todos": []}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

data = load_data()

# HTML
HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Produktivitetsapp</title>

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

<h1>Produktivitetsapp</h1>
<button onclick="toggleDark()">Mørk modus</button>

<h2>Søk notater</h2>
<input id="search" oninput="loadNotes()" placeholder="Søk...">

<h2>Notater</h2>

<input id="title" placeholder="Tittel"><br><br>
<textarea id="content" placeholder="Innhold"></textarea><br>
<input id="category" placeholder="Kategori"><br><br>

<button class="btn-primary" onclick="addNote()">Legg til</button>

<div id="notes"></div>

<h2>Todos</h2>

<input id="todoInput" placeholder="Ny todo">
<button class="btn-primary" onclick="addTodo()">Legg til</button>

<select onchange="loadTodos()" id="filter">
<option value="all">Alle</option>
<option value="done">Ferdige</option>
<option value="active">Aktive</option>
</select>

<div id="todos"></div>

<script>

function toggleDark() {
    document.body.classList.toggle("dark");
}

// -------- NOTES --------

async function loadNotes() {
    const search = document.getElementById("search").value.toLowerCase();
    const res = await fetch("/notes");
    let notes = await res.json();

    notes = notes.filter(n =>
        n.title.toLowerCase().includes(search) ||
        n.content.toLowerCase().includes(search)
    );

    notes.sort((a,b)=> b.pinned - a.pinned);

    const div = document.getElementById("notes");
    div.innerHTML = "";

    notes.forEach((n,i)=>{
        div.innerHTML += `
        <div class="card">
            <b>${n.title}</b> ${n.pinned ? "Favoritt" : ""}<br>
            <small>${n.category} | ${n.date}</small><br><br>
            ${n.content}<br><br>

            <button class="btn-success" onclick="pin(${i})">Pinn</button>
            <button class="btn-secondary" onclick="editNote(${i})">Rediger</button>
            <button class="btn-delete" onclick="deleteNote(${i})">Slett</button>
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

async function deleteNote(i){
    await fetch("/notes/"+i,{method:"DELETE"});
    loadNotes();
}

async function pin(i){
    await fetch("/notes/"+i+"/pin",{method:"PATCH"});
    loadNotes();
}

async function editNote(i){
    const title = prompt("Ny tittel:");
    const content = prompt("Nytt innhold:");

    await fetch("/notes/"+i,{
        method:"PUT",
        headers:{"Content-Type":"application/json"},
        body: JSON.stringify({title, content})
    });

    loadNotes();
}

// -------- TODOS --------

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
            <span class="${t.done?"done":""}">${t.task}</span>
            <button class="btn-success" onclick="toggle(${i})">Utført</button>
            <button class="btn-secondary" onclick="editTodo(${i})">Rediger</button>
            <button class="btn-delete" onclick="deleteTodo(${i})">Slett</button>
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

async function toggle(i){
    await fetch("/todos/"+i+"/toggle",{method:"PATCH"});
    loadTodos();
}

async function deleteTodo(i){
    await fetch("/todos/"+i,{method:"DELETE"});
    loadTodos();
}

async function editTodo(i){
    const task = prompt("Ny tekst:");
    await fetch("/todos/"+i,{
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

# Routing
@app.route("/")
def index():
    return render_template_string(HTML)

# Notater
@app.route("/notes", methods=["GET"])
def get_notes():
    return jsonify(data["notes"])

@app.route("/notes", methods=["POST"])
def add_note():
    d = request.json
    note = {
        "title": d["title"],
        "content": d["content"],
        "category": d.get("category",""),
        "pinned": False,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    data["notes"].append(note)
    save_data(data)
    return "", 201

@app.route("/notes/<int:i>", methods=["DELETE"])
def delete_note(i):
    data["notes"].pop(i)
    save_data(data)
    return ""

@app.route("/notes/<int:i>/pin", methods=["PATCH"])
def pin_note(i):
    data["notes"][i]["pinned"] = not data["notes"][i]["pinned"]
    save_data(data)
    return ""

@app.route("/notes/<int:i>", methods=["PUT"])
def edit_note(i):
    d = request.json
    data["notes"][i]["title"] = d["title"]
    data["notes"][i]["content"] = d["content"]
    save_data(data)
    return ""

# To Dos

@app.route("/todos", methods=["GET"])
def get_todos():
    return jsonify(data["todos"])

@app.route("/todos", methods=["POST"])
def add_todo():
    d = request.json
    data["todos"].append({"task": d["task"], "done": False})
    save_data(data)
    return ""

@app.route("/todos/<int:i>/toggle", methods=["PATCH"])
def toggle(i):
    data["todos"][i]["done"] = not data["todos"][i]["done"]
    save_data(data)
    return ""

@app.route("/todos/<int:i>", methods=["DELETE"])
def delete_todo(i):
    data["todos"].pop(i)
    save_data(data)
    return ""

@app.route("/todos/<int:i>", methods=["PUT"])
def edit_todo(i):
    d = request.json
    data["todos"][i]["task"] = d["task"]
    save_data(data)
    return ""

if __name__ == "__main__":
    app.run(debug=True)