const API = "http://localhost:5000"

// Notater
async function saveNote() {
    const title = document.getElementById("title").value;
    const content = document.getElementById("content").value;

    await fetch(API + "/notes", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title, content })
    });

    loadNotes()
}

async function loadNotes() {
    const res = await fetch(API + "/notes");
    const notes = await res.json();

    const list = document.getElementById("notes");
    list.innerHTML = "";

    notes.forEach(n => {
        const li = document.createElement("li");
        li.innerText = n.title + ": " + n.content;
        list.appendChild(li);
    });
}

// ToDos
let tasks = [];

function addTask() {
    const text = getElementById("taskInput").value;
    tasks.push({ text, done: false });
    renderTasks();
}

function renderTasks() {
    const list = document.getElementById("taskList").value;
    list.innerHTML = "";

    tasks.forEach(t => {
        const li = document.createElement("li");
        li.innerText = t.text;
        list.appendChild(li);
    })
}

async function saveTodo() {
    const title = document.getElementById("todoTitle").value;

    await fetch(API + "/todos", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title, tasks })
    });
    
    tasks = [];
    renderTasks();
    loadTodos();
}

async function loadTodos() {
    const res = await fetch(API + "/todos");
    const todos = await res.json();

    const list = document.getElementById("todos");
    list.innerHTML = "";

    todos.forEach(todo => {
        const li = document.createElement("li");
        li.innerText = todo.title;

        const ul = document.createElement("ul");

        todo.tasks.forEach(task => {
            const t = document.createElement("li");
            t.innerText = tasks.text + (task.done ? "✔": "");
            ul.appendChild(t);
        })

        li.appendChild(ul);
        list.appendChild(li);
    })
}

// Ved oppstart

loadNotes();
loadTodos();