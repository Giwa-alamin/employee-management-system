import sqlite3

# Connect to the database
conn = sqlite3.connect("employees.db", check_same_thread=False)
cursor = conn.cursor()

# Create the employees table
cursor.execute("""
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    department TEXT NOT NULL,
    position TEXT NOT NULL,
    salary REAL NOT NULL
)
""")

conn.commit()


def add_employee(name, email, department, position, salary):
    cursor.execute(
        "INSERT INTO employees (name, email, department, position, salary) VALUES (?, ?, ?, ?, ?)",
        (name, email, department, position, salary)
    )
    conn.commit()


def get_employees():
    cursor.execute("SELECT * FROM employees")
    return cursor.fetchall()
