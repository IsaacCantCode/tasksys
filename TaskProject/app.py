import json
import os
from flask import Flask, render_template, request, redirect

app = Flask(__name__)
DATA_FILE = 'tasks.json'

def load_tasks():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(DATA_FILE, 'w') as f:
        json.dump(tasks, f)

@app.route('/')
def index():
    tasks = load_tasks()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    tasks = load_tasks()
    task_content = request.form.get('task')
    task_date = request.form.get('date')
    if task_content and task_date:
        tasks.append({'id': len(tasks), 'content': task_content, 'date': task_date})
        save_tasks(tasks)
    return redirect('/')

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    tasks = load_tasks()
    tasks = [t for t in tasks if t['id'] != task_id]
    save_tasks(tasks)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)