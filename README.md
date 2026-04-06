# 💰 Finance Dashboard Backend (FastAPI + PostgreSQL)

A backend system for managing financial data, built with clean architecture, secure authentication, and scalable API design.

This project demonstrates real-world backend engineering principles aligned with fintech requirements such as data integrity, access control, and performance.

---

## 🚀 Live Demo & API Docs

🔗 Swagger API Docs  
[https://finance-dashboard-zytj.onrender.com/docs  ](https://finance-dashboard-zytj.onrender.com/docs)

🔗 GitHub Repository  
https://github.com/rahulbhatia3422/finance-dashboard.git  

---

## 🎯 Project Objective

This project was built as part of a backend assessment focused on:

- API design & architecture  
- Data modeling & persistence  
- Role-based access control  
- Financial data processing  
- Clean and maintainable code  

It fulfills all core requirements including:

- User & role management  
- Financial records CRUD  
- Dashboard analytics  
- Access control (RBAC)  
- Validation & error handling  

---

## 🧠 Why FastAPI + PostgreSQL?

### ⚡ FastAPI

- High performance (similar to Node.js & Go)
- Built-in validation using Pydantic
- Automatic Swagger documentation
- Async support for handling multiple requests
- Ideal for real-time fintech systems

👉 FastAPI is well-suited for fintech applications requiring speed, scalability, and security.

---

### 🐘 PostgreSQL

- ACID compliance → ensures financial data integrity  
- Strong relational data modeling  
- Advanced querying for analytics  
- Widely used in banking & fintech systems  

---

### 🌐 Deployment (Render)

- Backend deployed on Render  
- PostgreSQL database hosted on Render  
- Public API available for testing  
- Simple CI/CD integration  

---

## 🔐 Authentication & Authorization

### JWT-Based Authentication

- Secure token-based login  
- Stateless authentication  
- Scalable for production systems  

---

### 🔑 Login Flow

1. User sends request to `/login`  
2. Server validates credentials  
3. JWT token is generated  
4. Token is used to access protected APIs  


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
│── main.py
```

---

## 🛠️ Tech Stack

* FastAPI
* PostgreSQL
* SQLAlchemy ORM
* JWT (python-jose)
* Uvicorn
* Render (Deployment)

---

## ⚡ Setup Instructions

### 1️⃣ Clone Repository

```bash
git clone https://github.com/rahulbhatia3422/finance-dashboard.git
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

### 4️⃣ Run APIs Locally 

```bash
uvicorn app.main:app --reload
```

---

## 🔑 Authentication Flow

### Login

POST `/login`

Example:
```

| Role    | Email                                         | Name          | Permissions                               |
| ------- | --------------------------------------------- | ------------- | ----------------------------------------- |
| Admin   | [rahul@admin.com](mailto:rahul@admin.com)     | Rahul Admin   | Full system access                        |
| Analyst | [bablu@analyst.com](mailto:bablu@analyst.com) | Bablu Analyst | Create/Update own records, View analytics |
| Viewer  | [raj@viewer.com](mailto:raj@viewer.com)       | Raj Viewer    | Read-only access                          |
 

```


### Response

```json
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


👉 Or create your own user using `/users`

---

## 🛡️ Role-Based Access Control (RBAC)

| Role     | Permissions |
|----------|------------|
| Admin    | Full access (CRUD + user management) |
| Analyst  | Read + analytics |
| Viewer   | Read-only |

✔ Implemented using dependency-based role validation  
✔ Ensures secure backend operations  

---

## 🗄️ Data Models Overview

### 👤 User

- id  
- name  
- email  
- role (admin / analyst / viewer)
- is_active

---

### 💸 Record

- id  
- amount  
- type (income / expense)  
- category  
- notes  
- is_deleted
- user_id

---

## ⚖️ Assumptions & Trade-offs

- Soft delete used instead of hard delete to preserve financial history  
- JWT authentication implemented without refresh tokens for simplicity  
- Role system kept minimal (admin, analyst, viewer)  
- No rate limiting added to keep implementation focused  
- Focused on backend logic over frontend/UI  

---

## 🧭 API Flow (High Level)

Client  
   ↓  
FastAPI Routes  
   ↓  
Services Layer  
   ↓  
Database (PostgreSQL)

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

## 🧪 Testing Strategy

- Manual testing performed using Swagger UI  
- All CRUD operations verified  
- Role-based access control tested  
- Error handling tested for invalid inputs and unauthorized access  

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