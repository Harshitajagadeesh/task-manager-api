# **Task Management REST API**

A professional, secure Task Management API built with **FastAPI**, **PostgreSQL**, and **SQLAlchemy**.

## **Features**

  * **Authentication:** JWT-based login and registration.
  * **CRUD Operations:** Create, Read, Update status, and Soft Delete tasks.
  * **Pagination:** Efficient data retrieval using `skip` and `limit`.
  * **Validation:** Strict input validation using Pydantic v2.
  * **Error Handling:** Standardized JSON error responses for all scenarios.
  * **Database:** PostgreSQL with automatic table synchronization.


## **Project Structure**

The project follows the **Repository-Service-Controller** pattern for clean separation of concerns:

```text
task-manager-api/
├── app/
│   ├── config/
│   │   └── database.py        # SQLAlchemy engine & session setup
│   ├── controllers/
│   │   ├── task_controller.py # Task API routes
│   │   └── user_controller.py # Auth API routes
│   ├── core/
│   │   ├── config.py          # Environment settings
│   │   └── security.py        # JWT & Password logic
│   ├── middlewares/
│   │   ├── auth_middleware.py  # JWT dependency
│   │   └── exception.py       # Global error handlers
│   ├── models/
│   │   ├── task.py            # Task SQLAlchemy model
│   │   └── user.py            # User SQLAlchemy model
│   ├── repositories/
│   │   ├── task_repository.py # Direct DB queries
│   │   └── user_repository.py # Direct DB queries
│   ├── schemas/
│   │   ├── response_schema.py # Generic API response
│   │   ├── task_schema.py     # Task Pydantic models
│   │   └── user_schema.py     # User Pydantic models
│   ├── services/
│   │   ├── task_service.py    # Task business logic
│   │   └── user_service.py    # User business logic
│   └── main.py                # App entry point
├── .env                       # Environment variables (Hidden)
├── .gitignore                 # Files to exclude from Git
├── requirements.txt           # Python dependencies
└── README.md                  # Project documentation
```


## **Setup Instructions**

### **1. Prerequisites**

  * **Python 3.10+**
  * **PostgreSQL** (Ensure a database named `task_db` is created)

### **2. Installation**

```bash
# Clone the repository
git clone <your-repo-url>
cd task-manager-api

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### **3. Environment Configuration**

Create a `.env` file in the root directory:

```bash
DATABASE_URL=postgresql://<username>:<password>@localhost:5432/task_db
SECRET_KEY=your_random_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

### **4. Running the API**

```bash
uvicorn app.main:app --reload
```

*The API will automatically create the required database tables on startup.*

-----

## **API Documentation**

Once the server is running, you can access the interactive docs at:

  * **Swagger UI:** [http://127.0.0.1:8000/docs](https://www.google.com/search?q=http://127.0.0.1:8000/docs)

-----

## **Testing with Curl**

### **1. Authentication**

**Register a User:**

```bash
curl -X POST http://127.0.0.1:8000/auth/register \
     -H "Content-Type: application/json" \
     -d '{"email": "user@example.com", "password": "password123"}'
```

**Login (Get Token):**

```bash
curl -X POST http://127.0.0.1:8000/auth/login \
     -H "Content-Type: application/json" \
     -d '{"email": "user@example.com", "password": "password123"}'
```

### **2. Tasks (Requires Token)**

**Create Task:**

```bash
curl -X POST http://127.0.0.1:8000/tasks/ \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"title": "My Task", "description": "This is a test task"}'
```

**Get All Tasks (with Pagination):**

```bash
curl -X GET "http://127.0.0.1:8000/tasks/?skip=0&limit=10" \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Update Task Status:**

```bash
curl -X PATCH http://127.0.0.1:8000/tasks/1 \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"status": "completed"}'
```

**Delete Task:**

```bash
curl -X DELETE http://127.0.0.1:8000/tasks/1 \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```


## **Database Schema**

The following schema is managed by SQLAlchemy:

  * **Users:** `id` (PK), `email` (Unique), `password`.
  * **Tasks:** `id` (PK), `title`, `description`, `status`, `user_id` (FK), `created_at`, `updated_at`, `deleted_at`.
