# FastAPI Production-Ready Backend

This project demonstrates a production-grade FastAPI application structure, implementing advanced concepts including **Authentication**, **Database Migrations**, and **Distributed Background Tasks** with Celery & Redis.

## 📌 Topic Implementation Map

This section maps the learning requirements to the specific files in this codebase.

### 3.1 App Initialization & Path Operations
| Concept | Implementation File | Description |
| :--- | :--- | :--- |
| **App Initialization** | [`app/main.py`](app/main.py) | FastAPI app creation with title, version, and CORS settings. |
| **Path Operations** | [`app/api/v1/endpoints/users.py`](app/api/v1/endpoints/users.py) | Implements `GET`, `POST`, `PUT` HTTP methods. |

### 3.2 Request & Response Handling
| Concept | Implementation File | Description |
| :--- | :--- | :--- |
| **Request Parsing** | [`app/api/v1/endpoints/auth.py`](app/api/v1/endpoints/auth.py) | Parses JSON body for Login credentials. |
| **Status Codes** | [`app/api/v1/endpoints/users.py`](app/api/v1/endpoints/users.py) | Returns `404 Not Found` or `400 Bad Request` appropriately. |
| **HTTP Headers/Cookies** | [`app/api/v1/endpoints/auth.py`](app/api/v1/endpoints/auth.py) | Sets `HttpOnly` cookies for secure JWT storage. |

### 3.3 Pydantic (Data Validation)
| Concept | Implementation File | Description |
| :--- | :--- | :--- |
| **BaseModel & Schemas** | [`app/schemas/user.py`](app/schemas/user.py) | Defines `UserCreate`, `UserUpdate`, and `UserResponse` schemas. |
| **Validation** | [`app/schemas/item.py`](app/schemas/item.py) | Enforces data types and required fields automatically. |

### 3.4 Dependency Injection
| Concept | Implementation File | Description |
| :--- | :--- | :--- |
| **Depends() & DB Session** | [`app/api/deps.py`](app/api/deps.py) | `get_db()` yields a database session for each request. |
| **Auth Dependency** | [`app/api/deps.py`](app/api/deps.py) | `get_current_active_user()` validates JWT and injects user object. |

### 3.5 Authentication & Authorization
| Concept | Implementation File | Description |
| :--- | :--- | :--- |
| **JWT Config** | [`app/core/config.py`](app/core/config.py) | Configures `SECRET_KEY` and `ALGORITHM`. |
| **Password Hashing** | [`app/core/security.py`](app/core/security.py) | Uses `bcrypt` (via `passlib`) for secure password hashing. |
| **Login Flow** | [`app/api/v1/endpoints/auth.py`](app/api/v1/endpoints/auth.py) | Verifies credentials and issues Access Tokens. |

### 3.6 Middleware
| Concept | Implementation File | Description |
| :--- | :--- | :--- |
| **CORS** | [`app/main.py`](app/main.py) | Configures Cross-Origin Resource Sharing for frontend access. |
| **Custom Middleware** | [`app/core/middleware.py`](app/core/middleware.py) | `LogRequestMiddleware` logs every request for audit trails. |

### 3.7 Database Integration (SQLModel + Alembic)
| Concept | Implementation File | Description |
| :--- | :--- | :--- |
| **ORM Models** | [`app/models/user.py`](app/models/user.py) | Defines Database Tables using SQLModel. |
| **Session Management** | [`app/db/session.py`](app/db/session.py) | Configures SQLAlchemy Engine and Session factories. |
| **Migrations** | [`alembic/`](alembic/) | Manages schema changes (Generated via `alembic revision --autogenerate`). |

### 3.8 Background Tasks (Celery + Redis)
| Concept | Implementation File | Description |
| :--- | :--- | :--- |
| **Celery Setup** | [`app/core/celery_app.py`](app/core/celery_app.py) | Connects to Redis Broker and Configures Backend. |
| **Task Definitions** | [`app/worker.py`](app/worker.py) | Defines `@celery_app.task` for long-running jobs (e.g., video processing). |
| **Scheduled Tasks (Beat)**| [`app/core/celery_app.py`](app/core/celery_app.py) | Configures Cron-like schedules (e.g., Run every 30 seconds). |

---

## 🚀 How to Run

### 1. Requirements
*   Python 3.10+
*   PostgreSQL
*   Redis (for Celery)

### 2. Start Services
This project uses **4 separate terminals** to simulate a full microservices environment:

### Mac / Linux Users
First, make the scripts executable:
```bash
chmod +x run_worker.sh run_beat.sh run_flower.sh
```

Then run them in separate terminals:

**Terminal 2: Worker**
```bash
./run_worker.sh
```

**Terminal 3: Beat**
```bash
./run_beat.sh
```

**Terminal 4: Flower**
```bash
./run_flower.sh
```
