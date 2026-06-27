# User Management API

A RESTful User Management API built using **FastAPI**, **SQLAlchemy**, and **MySQL**. The project provides user authentication using JWT, user management, dashboard statistics, audit logging, refresh tokens, profile image upload, and other essential backend features.

---

# Features

## Authentication

* User Registration
* User Login
* JWT Authentication
* Refresh Token
* User Profile

## User Management

* Get All Users (Pagination & Search)
* Get User by ID
* Update User
* Change Password
* Soft Delete User

## Dashboard

* Total Users
* Active Users
* Inactive Users
* Recently Registered Users (Last 7 Days)

## Audit Logs

* Track User Registration
* Track User Updates
* Track Password Changes
* Track User Deletion

## Additional Features

* Profile Image Upload
* Password Hashing using bcrypt
* Last Login Tracking
* Input Validation
* RESTful API Design

---

# Tech Stack

* Python 3
* FastAPI
* SQLAlchemy
* MySQL
* PyMySQL
* Pydantic
* Python-JOSE (JWT)
* Passlib (bcrypt)
* Python-Multipart
* Uvicorn
* Python-Dotenv

---

# Project Structure

```text
userManagementSystem/
│
├── app/
│   ├── api/
│   │   ├── auth.py
│   │   ├── users.py
│   │   ├── dashboard.py
│   │   └── audit.py
│   │
│   ├── database/
│   │   └── database.py
│   │
│   ├── models/
│   │   ├── user.py
│   │   └── audit_log.py
│   │
│   ├── schemas/
│   │   ├── update_user.py
│   │   ├── change_password.py
│   │   └── refresh_token.py
│   │
│   ├── utils/
│   │   ├── security.py
│   │   └── token.py
│   │
│   └── main.py
│
├── uploads/
├── database.sql
├── requirements.txt
├── README.md
└── .env.example
```

---

# Installation

## 1. Clone the Repository

```bash
git clone <repository-url>
cd userManagementSystem
```

---

## 2. Create Virtual Environment

```bash
python -m venv venv
```

### Activate

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

Create a `.env` file in the project root.

```env
DATABASE_URL=mysql+pymysql://root:password@localhost/user_management
```

---

## 5. Create Database

Import the provided `database.sql` file into MySQL.

---

## 6. Run the Application

```bash
uvicorn app.main:app --reload
```

---

# API Documentation

Swagger UI

```text
http://127.0.0.1:8000/docs
```

ReDoc

```text
http://127.0.0.1:8000/redoc
```

---

# API Endpoints

## Authentication

| Method | Endpoint                  | Description                 |
| ------ | ------------------------- | --------------------------- |
| POST   | `/api/auth/register`      | Register a new user         |
| POST   | `/api/auth/login`         | Login user                  |
| POST   | `/api/auth/refresh-token` | Generate a new access token |
| GET    | `/api/auth/profile`       | Get logged-in user profile  |

---

## Users

| Method | Endpoint                     | Description                            |
| ------ | ---------------------------- | -------------------------------------- |
| GET    | `/api/users`                 | Get all users with pagination & search |
| GET    | `/api/users/{id}`            | Get user by ID                         |
| PUT    | `/api/users/{id}`            | Update user                            |
| PUT    | `/api/users/change-password` | Change current user's password         |
| DELETE | `/api/users/{id}`            | Soft delete user                       |

---

## Dashboard

| Method | Endpoint         | Description          |
| ------ | ---------------- | -------------------- |
| GET    | `/api/dashboard` | Dashboard statistics |

---

## Audit Logs

| Method | Endpoint     | Description     |
| ------ | ------------ | --------------- |
| GET    | `/api/audit` | View audit logs |

---

# Bonus Features Implemented

* Refresh Token Authentication
* Last Login Tracking
* Audit Logging
* Soft Delete
* Profile Image Upload
* Pagination
* Search Functionality

---

# Security Features

* Password Hashing using bcrypt
* JWT Authentication
* Refresh Token
* Password Change Verification
* Unique Email Validation
* Unique Mobile Number Validation
* Input Validation
* Protected Endpoints

---

# Testing

The project includes a Postman Collection for testing all API endpoints.

---

# Author

**Sabah Muhamd**

B.Tech Computer Science & Engineering

Python Developer | Backend Developer | Cybersecurity Enthusiast
