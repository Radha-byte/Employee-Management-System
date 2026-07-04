from werkzeug.utils import secure_filename
import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, session
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.secret_key = 'secretkey'

# MySQL Configuration
app.config.from_pyfile('config.py')

mysql = MySQL(app)

# LOGIN ROUTE
@app.route('/', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        cur = mysql.connection.cursor()

        query = """
        SELECT * FROM users
        WHERE username=%s AND password=%s AND role=%s
        """

        cur.execute(query, (username, password, role))

        user = cur.fetchone()

        cur.close()

        if user:

            session['username'] = username
            session['role'] = role

            # Redirect According To Role
            if role == 'admin':
                return redirect('/admin_dashboard')

            elif role == 'employee':
                return redirect('/employee_dashboard')

        else:
            return "Invalid Username, Password, or Role"

    return render_template('login.html')


# ADMIN DASHBOARD
@app.route('/admin_dashboard')
def admin_dashboard():

    if 'username' in session and session['role'] == 'admin':

        cur = mysql.connection.cursor()

        # TOTAL EMPLOYEES
        cur.execute("SELECT COUNT(*) FROM employees")
        total_employees = cur.fetchone()[0]

        # TOTAL DEPARTMENTS
        cur.execute("SELECT COUNT(*) FROM departments")
        total_departments = cur.fetchone()[0]

        # COMPLETED TASKS
        cur.execute(
            "SELECT COUNT(*) FROM tasks WHERE status='Completed'"
        )
        completed_tasks = cur.fetchone()[0]

        # PENDING TASKS
        cur.execute(
            "SELECT COUNT(*) FROM tasks WHERE status='Pending'"
        )
        pending_tasks = cur.fetchone()[0]
        
        # OVERDUE TASKS

        cur.execute("""
        SELECT COUNT(*)
        FROM tasks
        WHERE due_date < CURDATE()
        AND status='Pending'
        """)

        overdue_tasks = cur.fetchone()[0]

        # TASK COMPLETION RATE
        total_tasks = completed_tasks + pending_tasks

        if total_tasks > 0:
            completion_rate = round(
                (completed_tasks / total_tasks) * 100,
            2
        )
        else:
            completion_rate = 0

        # RECENT EMPLOYEES
        cur.execute("""
    SELECT employee_id,
           name,
           department,
           profile_photo
    FROM employees
    ORDER BY id DESC
    LIMIT 5
""")

        recent_employees = cur.fetchall()

        # RECENT TASKS
        cur.execute("""
    SELECT employee_id,        
           employee_name,
           task_title,
           status
    FROM tasks
    ORDER BY id DESC
    LIMIT 5
""")

        recent_tasks = cur.fetchall()

        cur.close()

        current_date = datetime.now().strftime("%d %B %Y")

        return render_template(
            'dashboard.html',
            total_employees=total_employees,
            total_departments=total_departments,
            completed_tasks=completed_tasks,
            pending_tasks=pending_tasks,
            overdue_tasks=overdue_tasks,
            completion_rate=completion_rate,
            current_date=current_date,
            recent_employees=recent_employees,
            recent_tasks=recent_tasks
            
        )

    return redirect('/')


# ADD EMPLOYEE
@app.route('/add_employee', methods=['GET', 'POST'])
def add_employee():

    if 'username' in session and session['role'] == 'admin':

        if request.method == 'POST':

            employee_id = request.form['employee_id']
            name = request.form['name']
            username = request.form['username']
            department = request.form['department']
            designation = request.form['designation']
            contact_number = request.form['contact_number']
            joining_date = request.form['joining_date']
            office_location = request.form['office_location']

            cur = mysql.connection.cursor()

            query = """
            INSERT INTO employees
            (employee_id, name, department, designation,
            contact_number, joining_date, office_location, username)

            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """

            values = (
                employee_id,
                name,
                department,
                designation,
                contact_number,
                joining_date,
                office_location,
                username
            )

            cur.execute(query, values)

            mysql.connection.commit()

            cur.close()

            return "Employee Added Successfully"

        return render_template('add_employee.html')

    return redirect('/')


# VIEW EMPLOYEES
@app.route('/view_employees')
def view_employees():

    if 'username' in session and session['role'] == 'admin':

        search = request.args.get('search')

        cur = mysql.connection.cursor()

        # SEARCH FUNCTIONALITY
        if search:

            query = """
            SELECT * FROM employees
            WHERE name LIKE %s
            OR employee_id LIKE %s
            """

            search_term = "%" + search + "%"

            cur.execute(query, (search_term, search_term))

        else:

            query = "SELECT * FROM employees"

            cur.execute(query)

        employees = cur.fetchall()
        print(employees)

        cur.close()

        return render_template(
            'view_employees.html',
            employees=employees
        )

    return redirect('/')


# EDIT EMPLOYEE
@app.route('/edit_employee/<int:id>', methods=['GET', 'POST'])
def edit_employee(id):

    if 'username' in session and session['role'] == 'admin':

        cur = mysql.connection.cursor()

        # UPDATE DATA
        if request.method == 'POST':

            employee_id = request.form['employee_id']
            name = request.form['name']
            department = request.form['department']
            designation = request.form['designation']
            contact_number = request.form['contact_number']
            joining_date = request.form['joining_date']
            office_location = request.form['office_location']

            query = """
            UPDATE employees
            SET employee_id=%s,
                name=%s,
                department=%s,
                designation=%s,
                contact_number=%s,
                joining_date=%s,
                office_location=%s
            WHERE id=%s
            """

            values = (
                employee_id,
                name,
                department,
                designation,
                contact_number,
                joining_date,
                office_location,
                id
            )

            cur.execute(query, values)

            mysql.connection.commit()

            cur.close()

            return redirect('/view_employees')

        # FETCH EXISTING DATA
        query = "SELECT * FROM employees WHERE id=%s"

        cur.execute(query, (id,))

        employee = cur.fetchone()

        cur.close()

        return render_template(
            'edit_employee.html',
            employee=employee
        )

    return redirect('/')


# DELETE EMPLOYEE
@app.route('/delete_employee/<int:id>')
def delete_employee(id):

    if 'username' in session and session['role'] == 'admin':

        cur = mysql.connection.cursor()

        query = "DELETE FROM employees WHERE id=%s"

        cur.execute(query, (id,))

        mysql.connection.commit()

        cur.close()

        return redirect('/view_employees')

    return redirect('/')


# ADD DEPARTMENT
@app.route('/add_department', methods=['GET', 'POST'])
def add_department():

    if 'username' in session and session['role'] == 'admin':

        if request.method == 'POST':

            department_name = request.form['department_name']

            cur = mysql.connection.cursor()

            query = """
            INSERT INTO departments (department_name)
            VALUES (%s)
            """

            cur.execute(query, (department_name,))

            mysql.connection.commit()

            cur.close()

            return redirect('/view_departments')

        return render_template('add_department.html')

    return redirect('/')


# VIEW DEPARTMENTS
@app.route('/view_departments')
def view_departments():

    if 'username' in session and session['role'] == 'admin':

        cur = mysql.connection.cursor()

        query = "SELECT * FROM departments"

        cur.execute(query)

        departments = cur.fetchall()

        cur.close()

        return render_template(
            'view_departments.html',
            departments=departments
        )

    return redirect('/')

# ASSIGN TASK
@app.route('/assign_task', methods=['GET', 'POST'])
def assign_task():

    if 'username' in session and session['role'] == 'admin':

        if request.method == 'POST':

            employee_id = request.form['employee_id']
            cur = mysql.connection.cursor()

            cur.execute("""
SELECT employee_id,
       username,
       name
FROM employees
WHERE employee_id=%s
""", (employee_id,))

            employee = cur.fetchone()

            cur.close()

            employee_id = employee[0]
            username = employee[1]
            employee_name = employee[2]
            task_title = request.form['task_title']
            description = request.form['description']
            assigned_date = request.form['assigned_date']
            due_date = request.form['due_date']
            status = request.form['status']
            priority = request.form['priority']

            cur = mysql.connection.cursor()

            query = """
INSERT INTO tasks
(employee_id,
 username,
 employee_name,
 task_title,
 description,
 assigned_date,
 due_date,
 status,
 priority)

VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

            values = (
                employee_id,
                username,
                employee_name,
                task_title,
                description,
                assigned_date,
                due_date,
                status,
                priority
            )

            cur.execute(query, values)

            mysql.connection.commit()

            cur.close()

            return redirect('/view_tasks')

        cur = mysql.connection.cursor()

        cur.execute("""
SELECT employee_id,
       username,
       name
FROM employees
""")

        employees = cur.fetchall()

        cur.close()

        return render_template(
    'assign_task.html',
    employees=employees
)

    return redirect('/')


# VIEW TASKS
@app.route('/view_tasks')
def view_tasks():

    filter_status = request.args.get('status')

    cur = mysql.connection.cursor()

    if filter_status and filter_status != "All":

        query = """
        SELECT * FROM tasks
        WHERE status=%s
        """

        cur.execute(query, (filter_status,))

    else:

        query = "SELECT * FROM tasks"

        cur.execute(query)

    tasks = cur.fetchall()

    cur.close()

    print(tasks[0])

    return render_template(
        'view_tasks.html',
        tasks=tasks
        )

    return redirect('/')

# EDIT TASK
@app.route('/edit_task/<int:id>', methods=['GET', 'POST'])
def edit_task(id):

    if 'username' in session and session['role'] == 'admin':

        cur = mysql.connection.cursor()

        if request.method == 'POST':

            task_title = request.form['task_title']
            description = request.form['description']
            due_date = request.form['due_date']
            status = request.form['status']

            query = """
            UPDATE tasks
            SET task_title=%s,
                description=%s,
                due_date=%s,
                status=%s
            WHERE id=%s
            """

            cur.execute(
                query,
                (
                    task_title,
                    description,
                    due_date,
                    status,
                    id
                )
            )

            mysql.connection.commit()

            cur.close()

            return redirect('/view_tasks')

        cur.execute(
            "SELECT * FROM tasks WHERE id=%s",
            (id,)
        )

        task = cur.fetchone()

        cur.close()

        return render_template(
            'edit_task.html',
            task=task
        )

    return redirect('/')

# DELETE TASK
@app.route('/delete_task/<int:id>')
def delete_task(id):

    if 'username' in session and session['role'] == 'admin':

        cur = mysql.connection.cursor()

        cur.execute(
            "DELETE FROM tasks WHERE id=%s",
            (id,)
        )

        mysql.connection.commit()

        cur.close()

        return redirect('/view_tasks')

    return redirect('/')

@app.route('/view_leave_requests')
def view_leave_requests():

    if 'username' not in session:
        return redirect('/')

    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT *
        FROM leaves
        ORDER BY id DESC
    """)

    leaves = cur.fetchall()

    cur.close()

    return render_template(
        'view_leave_requests.html',
        leaves=leaves
    )

@app.route('/approve_leave/<int:id>')
def approve_leave(id):

    cur = mysql.connection.cursor()

    cur.execute("""
        UPDATE leaves
        SET status='Approved'
        WHERE id=%s
    """, (id,))

    mysql.connection.commit()

    cur.close()

    return redirect('/view_leave_requests')

@app.route('/reject_leave/<int:id>')
def reject_leave(id):

    cur = mysql.connection.cursor()

    cur.execute("""
        UPDATE leaves
        SET status='Rejected'
        WHERE id=%s
    """, (id,))

    mysql.connection.commit()

    cur.close()

    return redirect('/view_leave_requests')

# EMPLOYEE DASHBOARD
@app.route('/employee_dashboard')
def employee_dashboard():

    if 'username' in session and session['role'] == 'employee':

        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        username = session['username']

        # EMPLOYEE DETAILS
        cur.execute("""
            SELECT * FROM employees
            WHERE username=%s
        """, (username,))

        employee = cur.fetchone()

        # Employee Tasks
        cur.execute("""
            SELECT * FROM tasks
            WHERE username=%s
        """, (username,))

        tasks = cur.fetchall()

        total_tasks = len(tasks)

        # Completed Tasks
        cur.execute("""
            SELECT COUNT(*) AS completed
            FROM tasks
            WHERE username=%s
            AND status='Completed'
        """, (username,))

        completed = cur.fetchone()['completed']

        # Pending Tasks
        cur.execute("""
            SELECT COUNT(*) AS pending
            FROM tasks
            WHERE username=%s
            AND status='Pending'
        """, (username,))

        pending = cur.fetchone()['pending']

        cur.close()

        current_hour = datetime.now().hour

        if current_hour < 12:
          greeting = "Good Morning ☀️"

        elif current_hour < 18:
          greeting = "Good Afternoon 🌤️"

        else:
         greeting = "Good Evening 🌙"

         print(employee)

        return render_template(
            'employee_dashboard.html',
            tasks=tasks,
            completed=completed,
            greeting=greeting,
            pending=pending,
            total_tasks=total_tasks,
            username=username,
            employee=employee
        )

    return redirect('/')

@app.route('/update_task_status/<int:id>')
def update_task_status(id):

    if 'username' in session and session['role'] == 'employee':

        cur = mysql.connection.cursor()

        query = """
        UPDATE tasks
        SET status='Completed'
        WHERE id=%s
        """

        cur.execute(query, (id,))

        mysql.connection.commit()

        cur.close()

        return redirect('/employee_dashboard')

    return redirect('/')

# MY PROFILE
@app.route('/my_profile')
def my_profile():

    if 'username' in session and session['role'] == 'employee':

        username = session['username']

        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cur.execute("""
            SELECT * FROM employees
            WHERE username=%s
        """, (username,))

        employee = cur.fetchone()

        print("Employee Data:", employee)

        cur.close()

        return render_template(
            'my_profile.html',
            employee=employee
        )

    return redirect('/')

# EDIT PROFILE
@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():

    if 'username' in session and session['role'] == 'employee':

        username = session['username']

        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        if request.method == 'POST':

            contact_number = request.form['contact_number']
            office_location = request.form['office_location']

            cur.execute("""
                UPDATE employees
                SET contact_number=%s,
                    office_location=%s
                WHERE username=%s
            """,
            (
                contact_number,
                office_location,
                username
            ))

            mysql.connection.commit()

            return redirect('/my_profile')

        cur.execute("""
            SELECT * FROM employees
            WHERE username=%s
        """, (username,))

        employee = cur.fetchone()

        cur.close()

        return render_template(
            'edit_profile.html',
            employee=employee
        )

    return redirect('/')

@app.route('/upload_profile_photo', methods=['POST'])
def upload_profile_photo():

    if 'username' not in session:
        return redirect('/')

    photo = request.files['profile_photo']

    if photo and photo.filename != '':

        filename = secure_filename(photo.filename)

        photo.save(
            os.path.join(
                app.config['UPLOAD_FOLDER'],
                filename
            )
        )

        cur = mysql.connection.cursor()

        cur.execute("""
            UPDATE employees
            SET profile_photo=%s
            WHERE username=%s
        """, (filename, session['username']))

        mysql.connection.commit()

        cur.close()

    return redirect('/my_profile')

@app.route('/my_tasks')
def my_tasks():

    if 'username' not in session:
        return redirect('/')

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cur.execute("""
    SELECT *
    FROM tasks
    WHERE username=%s
""", (session['username'],))

    tasks = cur.fetchall()

    cur.close()

    return render_template(
    'my_tasks.html',
    tasks=tasks,
    total_tasks=len(tasks)
)

@app.route('/employee_complete_task/<int:id>')
def employee_complete_task(id):

    if 'username' not in session:
        return redirect('/')

    cur = mysql.connection.cursor()

    cur.execute("""
        UPDATE tasks
        SET status='Completed'
        WHERE id=%s
    """, (id,))

    mysql.connection.commit()

    cur.close()

    return redirect('/my_tasks')

@app.route('/my_department')
def my_department():

    if 'username' not in session:
        return redirect('/')

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cur.execute("""
        SELECT *
        FROM employees
        WHERE username=%s
    """, (session['username'],))

    employee = cur.fetchone()

    cur.execute("""
        SELECT name, designation
        FROM employees
        WHERE department=%s
    """, (employee['department'],))

    members = cur.fetchall()

    cur.close()

    return render_template(
        'my_department.html',
        employee=employee,
        members=members
    )

@app.route('/apply_leave', methods=['GET', 'POST'])
def apply_leave():

    if 'username' not in session:
        return redirect('/')

    if request.method == 'POST':

        leave_type = request.form['leave_type']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        reason = request.form['reason']

        cur = mysql.connection.cursor()

        cur.execute("""
            INSERT INTO leaves
            (username, leave_type, start_date,
             end_date, reason)

            VALUES (%s,%s,%s,%s,%s)
        """, (

            session['username'],
            leave_type,
            start_date,
            end_date,
            reason

        ))

        mysql.connection.commit()

        cur.close()

        return redirect('/apply_leave')

    return render_template('apply_leave.html')

@app.route('/my_leaves')
def my_leaves():

    if 'username' not in session:
        return redirect('/')

    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT *
        FROM leaves
        WHERE username=%s
        ORDER BY id DESC
    """, (session['username'],))

    leaves = cur.fetchall()

    cur.close()

    return render_template(
        'my_leaves.html',
        leaves=leaves
    )

# LOGOUT
@app.route('/logout')
def logout():

    session.clear()

    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)