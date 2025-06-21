import sqlite3
import os

# Ensure DB folder exists
os.makedirs('Database_Project', exist_ok=True)

# Connect to DB
conn = sqlite3.connect('Database_Project/employee.db')
cursor = conn.cursor()

# Create Departments table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Departments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT NOT NULL UNIQUE,
        name TEXT NOT NULL
    )
''')

# Create Employees table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        department_id INTEGER NOT NULL,
        salary REAL NOT NULL,
        joining_date TEXT NOT NULL,
        FOREIGN KEY (department_id) REFERENCES Departments(id)
    )
''')

conn.commit()

# Insert initial departments if table is empty
cursor.execute('SELECT COUNT(*) FROM Departments')
count = cursor.fetchone()[0]

if count == 0:
    departments = [
        ('HR', 'Human Resources'),
        ('FIN', 'Finance'),
        ('SAL', 'Sales'),
        ('MKT', 'Marketing'),
        ('IT', 'Information Technology'),
        ('RND', 'Research and Development'),
        ('CS', 'Customer Support'),
        ('LEG', 'Legal'),
        ('ADM', 'Administration'),
        ('OPS', 'Operations')
    ]
    cursor.executemany('INSERT INTO Departments (code, name) VALUES (?, ?)', departments)
    conn.commit()

# Functions
def add_employee():
    name = input("Enter employee name: ")
    age = int(input("Enter employee age: "))

    # Show department list
    cursor.execute('SELECT id, code, name FROM Departments')
    depts = cursor.fetchall()
    print("Departments:")
    for d in depts:
        print(f"{d[0]}. [{d[1]}] {d[2]}")
    dept_id = int(input("Enter Department ID: "))

    salary = float(input("Enter employee salary: "))
    joining_date = input("Enter joining date (YYYY-MM-DD): ")

    cursor.execute('''
        INSERT INTO Employees (name, age, department_id, salary, joining_date)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, age, dept_id, salary, joining_date))
    conn.commit()
    print("Employee added successfully.")

def view_employees():
    cursor.execute('''
        SELECT e.id, e.name, e.age, d.code, d.name, e.salary, e.joining_date
        FROM Employees e
        JOIN Departments d ON e.department_id = d.id
        ORDER BY e.id
    ''')
    rows = cursor.fetchall()

    print("\n--- Employee List ---")
    print(f"{'ID':<5} {'Name':<20} {'Age':<5} {'Dept Code':<10} {'Department':<25} {'Salary':<10} {'Joining Date':<12}")
    print("-" * 100)
    for row in rows:
        print(f"{row[0]:<5} {row[1]:<20} {row[2]:<5} {row[3]:<10} {row[4]:<25} {row[5]:<10} {row[6]:<12}")

def update_salary():
    emp_id = int(input("Enter Employee ID to update salary: "))
    new_salary = float(input("Enter new salary: "))
    cursor.execute('UPDATE Employees SET salary = ? WHERE id = ?', (new_salary, emp_id))
    conn.commit()
    print("Salary updated.")

def delete_employee():
    emp_id = int(input("Enter Employee ID to delete: "))
    cursor.execute('DELETE FROM Employees WHERE id = ?', (emp_id,))
    conn.commit()
    print("Employee deleted.")

def search_employee():
    name_query = input("Enter name to search: ")
    cursor.execute('''
        SELECT e.id, e.name, e.age, d.code, d.name, e.salary, e.joining_date
        FROM Employees e
        JOIN Departments d ON e.department_id = d.id
        WHERE e.name LIKE ?
    ''', ('%' + name_query + '%',))
    rows = cursor.fetchall()

    print("\n--- Search Results ---")
    for row in rows:
        print(row)

def view_by_department():
    cursor.execute('SELECT id, code, name FROM Departments')
    depts = cursor.fetchall()
    print("Departments:")
    for d in depts:
        print(f"{d[0]}. [{d[1]}] {d[2]}")
    dept_id = int(input("Enter Department ID: "))

    cursor.execute('''
        SELECT e.id, e.name, e.age, d.code, d.name, e.salary, e.joining_date
        FROM Employees e
        JOIN Departments d ON e.department_id = d.id
        WHERE d.id = ?
    ''', (dept_id,))
    rows = cursor.fetchall()

    print(f"\n--- Employees in Department ID {dept_id} ---")
    for row in rows:
        print(row)

# Main menu loop
while True:
    print("\n=== Employee Management System ===")
    print("1. Add Employee")
    print("2. View Employees")
    print("3. Update Employee Salary")
    print("4. Delete Employee")
    print("5. Search Employee by Name")
    print("6. View Employees by Department")
    print("7. Exit")

    option = input("Enter your choice: ")

    if option == '1':
        add_employee()
    elif option == '2':
        view_employees()
    elif option == '3':
        update_salary()
    elif option == '4':
        delete_employee()
    elif option == '5':
        search_employee()
    elif option == '6':
        view_by_department()
    elif option == '7':
        print("Goodbye.")
        break
    else:
        print("Invalid choice. Please try again.")

# Close connection
conn.close()