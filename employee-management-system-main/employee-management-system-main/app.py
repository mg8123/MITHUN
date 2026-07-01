from flask import Flask, render_template, request, redirect, jsonify
import sqlite3

app = Flask(__name__)

# Create DB
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            department TEXT,
            salary INTEGER,
            email TEXT,
            phone TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Home page
@app.route('/')
def index():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees")
    data = cursor.fetchall()
    conn.close()
    return render_template('index.html', employees=data)

# Add Employee
@app.route('/add', methods=['POST'])
def add():
    data = request.form
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO employees (name, department, salary, email, phone) VALUES (?, ?, ?, ?, ?)",
                   (data['name'], data['department'], data['salary'], data['email'], data['phone']))
    conn.commit()
    conn.close()
    return redirect('/')

# Delete Employee
@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM employees WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect('/')

# Update Employee
@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    data = request.form
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE employees 
        SET name=?, department=?, salary=?, email=?, phone=? 
        WHERE id=?
    """, (data['name'], data['department'], data['salary'], data['email'], data['phone'], id))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
