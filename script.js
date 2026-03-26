const API = "http://127.0.0.1:5500"

// Notater
async function saveNote() {
    const title = document.getElementById("title").value;
    const content = document.getElementById("content").value;
    try {
        await fetch(API + "/notes", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title, content })
    });

    loadNotes();
    } catch (error) {
        console.error("Kunne ikke lagre notat:", error);
    }
}

async function loadNotes() {
    try {
         const res = await fetch(API + "/notes");
        const notes = await res.json();

        const list = document.getElementById("notes");
        list.innerHTML = "";

        notes.forEach(n => {
        const li = document.createElement("li");
        li.innerText = n.title + ": " + n.content;
        list.appendChild(li);
    });
    } catch (error) {
        console.error("Kunne ikke hente notater:", error);
    }
}

// ToDos
let tasks = [];

function addTask() {
    const text = getElementById("taskInput").value;
    if (!text.trim()) return;

    tasks.push({ text, done: false });
    document.getElementById("taskInput").value = "";
    renderTasks();
}

function renderTasks() {
    const list = document.getElementById("taskList").value;
    list.innerHTML = "";

    tasks.forEach((t, index) => {
        const li = document.createElement("li");
        li.innerText = t.text;
        list.appendChild(li);
    });
}

async function saveTodo() {
    const title = document.getElementById("todoTitle").value;
    try {
        await fetch(API + "/todos", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title, tasks })
    });

    tasks = [];
    renderTasks();
    loadTodos();
    } catch (error) {
        console.error("Kunne ikke lagre todo:", error);
    }
}

async function loadTodos() {
    try {
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
    } catch (error) {
        console.error("Kunne ikke hente todo:", error)
    }
}

// Ved oppstart

loadNotes();
loadTodos();