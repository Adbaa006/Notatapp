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