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
body {
    font-family: Arial;
    margin: 0;
    padding: 20px;
    background: var(--bg);
    color: var(--text);
}

:root {
    --bg: #f4f6fb;
    --text: #111;
    --card: white;
}

.dark {
    --bg: #1e1e1e;
    --text: #eee;
    --card: #2c2c2c;
}

button {
    cursor: pointer;
}

.card {
    background: var(--card);
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 15px;
}

.done {
    text-decoration: line-through;
    color: green;
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

<button onclick="addNote()">Legg til</button>

<div id="notes"></div>

<h2>Todos</h2>

<input id="todoInput" placeholder="Ny todo">
<button onclick="addTodo()">Legg til</button>

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

"""