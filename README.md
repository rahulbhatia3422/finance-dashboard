# 💰 Finance Dashboard Backend (FastAPI)

A production-ready backend system for managing personal financial records, including income, expenses, and analytics. Built using FastAPI with clean architecture, JWT authentication, and role-based access control (RBAC).

---

## 🚀 Features

### 🔐 Authentication & Authorization

* JWT-based authentication
* Role-Based Access Control (RBAC)

  * `admin` → full access
  * `analyst` → read + summary
  * `viewer` → read-only

---

### 📊 Records Management

* Create, Read, Update, Delete (CRUD)
* Partial Update (PATCH)
* Soft Delete (data is preserved)
* Filtering (type, category, date)
* Search (category + notes)
* Pagination support

---

### 📈 Dashboard Summary

* Total Income
* Total Expense
* Net Balance
* Category-wise breakdown
* Recent transactions

---

### ⚙️ Additional Enhancements

* Logging (create/update/delete tracking)
* Proper HTTP status codes
* Clean modular architecture (routes, services, schemas)
* Error handling with FastAPI exceptions

---

## 🏗️ Project Structure

```
finance-dashboard/
│── app/
│   ├── db/
│   │   ├── database.py
│   │   ├── models.py
│   ├── schemas/
│   │   ├── user_schema.py
│   │   ├── record_schema.py
│   ├── services/
│   │   ├── user_service.py
│   │   ├── record_service.py
│   ├── utils/
│   │   ├── auth.py
│   │   ├── role_checker.py
│   ├── routes/
│   │   ├── user_routes.py
│   │   ├── record_routes.py
│   │   ├── auth_routes.py
│── main.py
```

---

## 🛠️ Tech Stack

* FastAPI
* PostgreSQL
* SQLAlchemy ORM
* JWT (python-jose)
* Uvicorn

---

## ⚡ Setup Instructions

### 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/finance-dashboard.git
cd finance-dashboard
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run Server

```bash
uvicorn main:app --reload
```

---

## 🔑 Authentication Flow

### Login

```
POST /login
```

Response:

```
{
  "access_token": "...",
  "token_type": "bearer"
}
```

### Use Token

Click **Authorize** in Swagger UI and enter:

```
Bearer <your_token>
```

---

## 📌 API Endpoints

### 👤 Users

* POST `/users` → Create user
* GET `/users` → Get all users (admin only)
* PUT `/users/{id}` → Update user
* PATCH `/users/{id}` → Partial update
* DELETE `/users/{id}` → Delete user

---

### 💸 Records

* POST `/records` → Create record
* GET `/records` → Get records (filter + pagination)
* GET `/records/search` → Search records
* PUT `/records/{id}` → Update record
* PATCH `/records/{id}` → Partial update
* DELETE `/records/{id}` → Soft delete

---

### 📊 Dashboard

* GET `/summary` → Financial summary

---

## 🔍 Query Examples

### Filter

```
/records?type=expense&category=food
```

### Pagination

```
/records?skip=0&limit=5
```

### Search

```
/records/search?keyword=salary
```

---

## 🧠 Design Decisions

* Used **service layer** for clean separation of logic
* Implemented **soft delete** to preserve data history
* Added **RBAC** for secure access control
* Used **JWT tokens** for stateless authentication
* Pagination + search for scalability

---

## 📈 Future Improvements

* Rate limiting
* Unit tests
* Refresh tokens
* Docker support
* Deployment (AWS / Render)

---

## 👨‍💻 Author

Rahul Bhatia
Backend Developer | FastAPI | Python

---

## ⭐ Conclusion

This project demonstrates strong backend fundamentals including:

* Clean architecture
* Secure authentication
* Scalable API design
* Real-world business logic

---
