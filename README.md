# Django Modular System

This project implements a Django-based modular application system where modules can be dynamically managed (install, upgrade, uninstall). The frontend is developed using MUI, providing a clean and responsive interface.


## 🧩 Features

### Backend (Django)
	•	Modular engine using dynamic imports (importlib)
	•	Admin interface to install, upgrade, or uninstall modules
	•	Role-based access control (RBAC): Manager, User, Public
	•	Module landing pages registered automatically
	•	User interface to CRUD products

```
project-root/
│
├── hashmicro/                # Django project settings
├── modular_engine/           # Core module engine
├── project01_module/         # Example module to demonstrate functionality
├── project02_module/         # Example module to demonstrate functionality
├── project03_module/         # Example module to demonstrate functionality
├── docs/                     # ERD & Flowchart
├── db.sqlite3                # SQLite database
├── manage.py
├── README.md
```



## 🚀 Getting Started

### Backend Setup
```
cd project-root
python -m venv venv
source venv/bin/activate
python manage.py migrate
python manage.py runserver
```


## 🌐 Project Preview

[🚀 Live Demo](https://wawansetiawan.pythonanywhere.com)


### 🔐 Role-Based Access
```
-------------|------------------------------|----------------|-----------|
| Role       | Permissions                  | Username       | Password  |
-------------|------------------------------|----------------|-----------|
| Admin      | Create, Read, Update, Delete | wawansetiawan	 | qwerty    |
| Manager  	 | Create, Read, Update, Delete | manager1    	 | admin123  |
| User   	 | Create, Read, Update         | user1          | user123   |
| Public 	 | Read Only                    | 				 |           |
-------------|------------------------------|----------------|-----------|
```

Roles/Group are assigned in the Django admin panel.



### 🧪 Example Modules

A sample module project01_module is provided with:
- A dedicated landing page
- A CRUD interface for products
- Metadata for dynamic registration



### 🖼️ ERD & Flowchart

See the /docs folder for the ERD and Flowchart.


### 🔒 Access Control Note

```
⚠️ Module Management Menu is only visible when:
	•	No user is logged in (public access)
	•	Or the logged-in user is an admin

🚫 It will not be displayed to users with manager or user roles when logged in, as it is intended to facilitate easier access.
```
