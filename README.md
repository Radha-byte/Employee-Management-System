# 👨‍💼 Employee Management System

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Flask](https://img.shields.io/badge/Flask-Framework-black)
![MySQL](https://img.shields.io/badge/MySQL-Database-orange)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-purple)
![Render](https://img.shields.io/badge/Deployed%20on-Render-success)

> A full-stack **Employee Management System** developed using **Python Flask** and **MySQL** during my internship. The system streamlines employee management, task allocation, leave management, and profile management through dedicated **Admin** and **Employee** portals.

---

## 📌 Project Overview

The Employee Management System (EMS) is a web-based application designed to simplify and digitize day-to-day employee management activities within an organization.

The application provides separate dashboards for **Administrators** and **Employees**, enabling efficient management of employee records, departments, task assignments, leave requests, and profile information.

The project focuses on improving organizational workflow while reducing manual record-keeping and administrative effort.

---

## 🌐 Live Demo

The Employee Management System is successfully deployed and can be accessed online.

🔗 **Live Application:**  
https://employee-management-system-frg0.onrender.com/

> **Demo Credentials**
>
> **Admin**
> - Username: admin
> - Password: admin123
>
> **Employee**
> - Username: employee1
> - Password: employee123

---

# ✨ Key Features

## 🔐 Secure Login System

- Separate login for **Admin** and **Employee**
- Session-based authentication
- Role-based access control

---

## 👨‍💼 Admin Module

### Dashboard
- Total Employees
- Total Departments
- Pending Tasks
- Completed Tasks
- Overdue Tasks
- Task Completion Rate
- Recent Employees
- Recent Task Activity

### Employee Management
- Add Employee
- Edit Employee
- Delete Employee
- Search Employee
- View Employee Records
- Employee Profile Photo Support

### Department Management
- Add Department
- View Departments

### Task Management
- Assign Tasks
- Task Priority (High / Medium / Low)
- Edit Tasks
- Delete Tasks
- Filter Tasks by Status

### Leave Management
- View Leave Requests
- Approve Leave
- Reject Leave

---

## 👨‍💻 Employee Module

### Dashboard
- Personalized Welcome Message
- Assigned Tasks
- Pending Task Count
- Completed Task Count
- Total Tasks

### Profile Management
- View Profile
- Edit Contact Information
- Update Office Location
- Upload Profile Picture

### Task Management
- View Assigned Tasks
- Mark Task as Completed

### Department
- View Department Details
- View Team Members

### Leave Module
- Apply Leave
- View Leave Status

---

# 🛠 Technology Stack

| Category | Technology |
|----------|------------|
| Backend | Python Flask |
| Frontend | HTML5 |
| Styling | CSS3 |
| Framework | Bootstrap 5 |
| Database | MySQL |
| Database Connector | Flask-MySQLdb |
| Authentication | Flask Sessions |
| Icons | Bootstrap Icons |
| Version Control | Git & GitHub |

---

# 🗄 Database

The project uses **MySQL** as the backend database.

### Main Tables

- users
- employees
- departments
- tasks
- leaves

The SQL dump is available inside:

```
database/ems_db.sql
```

---

# 📂 Project Structure

```
Employee-Management-System-Flask
│
├── app.py
├── requirements.txt
├── config_example.py
├── README.md
├── .gitignore
│
├── database/
│     └── ems_db.sql
│
├── screenshots/
│
├── static/
│     └── uploads/
│
└── templates/
```

---

# 📸 Project Screenshots

The project screenshots are available inside the **screenshots** folder.

Included Screens:

- Login Page
  <img width="1919" height="952" alt="login" src="https://github.com/user-attachments/assets/da29b67d-f543-48d3-b111-85f938d8a9cc" />

- Admin Dashboard
  <img width="1919" height="947" alt="admin_dashboard1" src="https://github.com/user-attachments/assets/f2507da6-ddde-4f7f-805a-7a1c3b423dea" />  <img width="1919" height="947" alt="admin_dashboard1" src="https://github.com/user-attachments/assets/0b104c02-e17c-46b3-b411-da724466612b" />  <img width="1919" height="942" alt="admin_dashboard3" src="https://github.com/user-attachments/assets/abad62ba-6b98-48c3-8a1a-f00e0044993b" />



- Employee Dashboard
  <img width="1919" height="946" alt="employee_dashboard1" src="https://github.com/user-attachments/assets/b34b6f0c-57e3-4ebc-a5b0-009d878e1d84" />  <img width="1919" height="948" alt="employee_dashboard2" src="https://github.com/user-attachments/assets/d100581f-0c5f-4c98-b90f-63beff266650" />


- Add Employee
  <img width="1919" height="829" alt="add_employee" src="https://github.com/user-attachments/assets/f8dc432b-f8df-4b29-a057-870a7b29d564" />

- Employee Records
  <img width="1919" height="542" alt="employee_records" src="https://github.com/user-attachments/assets/7ecaf3cb-34e0-49cf-8908-ba25d8a0ad68" />

- Assign Task
  <img width="1919" height="834" alt="assign_task" src="https://github.com/user-attachments/assets/38eac63e-fa96-4e34-8279-a6f8f4c9b7e7" />

- Task Records
  <img width="1919" height="538" alt="task_records" src="https://github.com/user-attachments/assets/b437a6d5-6b3a-427b-9053-a49f4c90da8e" />

- Leave Management
  <img width="1919" height="781" alt="employee_apply_leave" src="https://github.com/user-attachments/assets/e2874eb8-c994-4780-bb78-792ddf6a26bf" />  <img width="1919" height="502" alt="Admin_leave_approval" src="https://github.com/user-attachments/assets/87c45d53-2f0d-4a86-879f-553e8165f670" />  <img width="1769" height="459" alt="leave_status_check" src="https://github.com/user-attachments/assets/86a4058e-8100-4c85-8f70-e8a837456f60" />



- My Profile
  <img width="1917" height="819" alt="my_profile" src="https://github.com/user-attachments/assets/501a659e-63cd-48cf-86c8-e7c97450dbcb" />

- My Tasks
  <img width="1919" height="477" alt="my_tasks" src="https://github.com/user-attachments/assets/b044a833-bba8-4bad-b567-1521f2c52c53" />


---

# ⚙ Installation Guide

### 1 Clone Repository

```bash
git clone https://github.com/Radha-byte/Employee-Management-System.git
```

---

### 2 Navigate to Project

```bash
cd Employee-Management-System-Flask
```

---

### 3 Create Virtual Environment

```bash
python -m venv venv
```

---

### 4 Activate Virtual Environment

Windows

```bash
venv\Scripts\activate
```

Linux / Mac

```bash
source venv/bin/activate
```

---

### 5 Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 6 Configure Database

Create a file named

```
config.py
```

using

```
config_example.py
```

and update your MySQL credentials.

---

### 7 Import Database

Import

```
database/ems_db.sql
```

into your MySQL server.

---

### 8 Run Application

```bash
python app.py
```

---


# 👨‍💻 User Roles

## Admin

- Manage Employees
- Manage Departments
- Assign Tasks
- View Tasks
- Manage Leave Requests
- Dashboard Analytics

---

## Employee

- View Dashboard
- Manage Profile
- Upload Profile Photo
- View Assigned Tasks
- Complete Tasks
- Apply Leave
- Track Leave Status
- View Department Members

---

# 🚀 Future Enhancements

- Email Notification System
- Password Encryption
- Attendance Management
- Payroll Management
- Performance Evaluation Module
- QR Code Attendance
- PDF Report Generation
- Employee Document Management
- REST API Integration
- Responsive Mobile Version

---

# 🎯 Learning Outcomes

Through this internship project, I gained practical experience in:

- Full Stack Web Development
- Flask Framework
- MySQL Database Design
- CRUD Operations
- Session Management
- Authentication & Authorization
- Bootstrap UI Development
- File Upload Handling
- Git & GitHub
- Software Development Lifecycle

---

# 🏢 Internship

**Internship Domain**

Python Full Stack Development

**Project**

Employee Management System

---

# 👨‍💻 Developed By

**Radha Rani**

Python Full Stack Developer | Web Developer

GitHub: https://github.com/Radha-byte

LinkedIn: https://linkedin.com/in/radha-rani-04351329a

---

# 📄 License

This project is developed for **educational and internship purposes**.

Feel free to use and modify it for learning purposes.
