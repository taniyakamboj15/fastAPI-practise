# FastAPI Production Backend Template

This project demonstrates an industry-standard backend architecture using FastAPI. It implements best practices for scalability, security, and maintainability.

## 📚 Key Concepts Implemented

### 1. Project Structure 🏗️
**File:** `app/` structure
- **Why:** To separate concerns (logic vs storage vs API).
- **Explanation:**
    - `api/`: Handles HTTP requests (Routes).
    - `core/`: Config and Security settings.
    - `schemas/`: Pydantic models (Data validation).
    - `db/`: Database logic (Simulated in-memory).

### 2. Pydantic Schemas (Data Validation) 🛡️
**Files:** `app/schemas/user.py`, `app/schemas/item.py`
- **Why:** Security & Validation. Prevents bad data from entering and sensitive data (like passwords) from leaking out.
- **Concept:**
    - `UserCreate`: Has password (Input).
    - `User`: No password (Output).
    - **Pass Keyword:** Used when a class inherits everything and adds nothing new (e.g., `ItemUpdate`).

### 3. Dependency Injection (DI) 💉
**File:** `app/api/deps.py`
- **Why:** Reusability and Testing.
- **Usage:**
    - `get_current_user`: Checks if a user is logged in before every request.
    - `get_db`: Provides database access to endpoints.
- **Benefit:** avoiding code duplication in every single endpoint.

### 4. Authentication (Cookie + JWT) 🍪
**Files:** `app/api/v1/endpoints/auth.py`, `app/core/security.py`
- **Why:** Secure user sessions.
- **Mechanism:**
    - **HttpOnly Cookie:** Token is stored in a browser cookie that JavaScript cannot access (Prevents XSS attacks).
    - **JWT (JSON Web Token):** Stateless authentication.

### 5. internal Service Authentication (API Keys) 🔑
**Files:** `app/api/v1/endpoints/utils.py`, `scripts/cron_email_sender.py`
- **Why:** For Scripts, Cron Jobs, or Robots that cannot "Login" like humans.
- **Mechanism:** Uses `X-API-Key` header.
    - **Difference:** Cookies are for browsers (Auto-attach). Headers must be sent manually by the script.

### 6. Router Versioning 🔄
**File:** `app/api/v1/api.py`
- **Why:** Future-proofing.
- **Concept:** All routes are under `/api/v1/`. If we break changes later, we create `/api/v2/` without crashing the old app.

### 7. Middleware & Custom Headers ⏱️
**File:** `app/main.py`
- **Why:** To intercept every request globally.
- **Example:** Added `X-Process-Time` header to track how long the server takes to respond.

### 8. Configuration Checking ⚙️
**File:** `app/core/config.py`
- **Why:** To manage secrets and environment variables safely using `Pydantic Settings`.
- **Typing:** Uses `List` and `Union` to strictly define allowed data types.

## 🚀 How to Run

1.  **Start Server:**
    ```bash
    uvicorn app.main:app --reload
    ```
2.  **Run Internal Script:**
    ```bash
    python scripts/cron_email_sender.py
    ```
3.  **View Docs:**
    - [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## 📝 Ignoring Unwanted Files
**File:** `.gitignore`
- Configured to ignore sensitive files (`.env`), compiled code (`__pycache__`), and local configs (`venv/`, `.vscode/`).
