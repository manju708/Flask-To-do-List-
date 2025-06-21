from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Database initialization
def init_db():
    conn = sqlite3.connect('todos.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS todos
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 task TEXT NOT NULL,
                 description TEXT,
                 created_at TEXT,
                 completed INTEGER DEFAULT 0)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    conn = sqlite3.connect('todos.db')
    c = conn.cursor()
    
    # Filter for completed/incomplete tasks if requested
    filter_type = request.args.get('filter', 'all')
    
    if filter_type == 'completed':
        c.execute("SELECT * FROM todos WHERE completed = 1 ORDER BY created_at DESC")
    elif filter_type == 'incomplete':
        c.execute("SELECT * FROM todos WHERE completed = 0 ORDER BY created_at DESC")
    else:
        c.execute("SELECT * FROM todos ORDER BY created_at DESC")
    
    todos = c.fetchall()
    conn.close()
    return render_template('index.html', todos=todos, filter_type=filter_type)

@app.route('/add', methods=['POST'])
def add():
    task = request.form['task']
    description = request.form.get('description', '')
    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    conn = sqlite3.connect('todos.db')
    c = conn.cursor()
    c.execute("INSERT INTO todos (task, description, created_at) VALUES (?, ?, ?)",
              (task, description, created_at))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/edit/<int:todo_id>', methods=['GET', 'POST'])
def edit(todo_id):
    conn = sqlite3.connect('todos.db')
    c = conn.cursor()
    
    if request.method == 'POST':
        task = request.form['task']
        description = request.form.get('description', '')
        c.execute("UPDATE todos SET task = ?, description = ? WHERE id = ?",
                  (task, description, todo_id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    
    c.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
    todo = c.fetchone()
    conn.close()
    return render_template('edit.html', todo=todo)

@app.route('/complete/<int:todo_id>')
def complete(todo_id):
    conn = sqlite3.connect('todos.db')
    c = conn.cursor()
    c.execute("UPDATE todos SET completed = 1 WHERE id = ?", (todo_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/uncomplete/<int:todo_id>')
def uncomplete(todo_id):
    conn = sqlite3.connect('todos.db')
    c = conn.cursor()
    c.execute("UPDATE todos SET completed = 0 WHERE id = ?", (todo_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    conn = sqlite3.connect('todos.db')
    c = conn.cursor()
    c.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)