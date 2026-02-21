# Full Stack CRUD App

A robust, secure, and interactive Task Management system featuring a Drag and Drop Kanban interface. This application allows users to register, log in, and manage their tasks with strict data isolation. It includes a comprehensive "Soft Delete" mechanism with a Recycle Bin for data recovery and permanent deletion.

## Key Features

### Authentication & Security
* **User Registration & Login:** Secure access control using JWT (JSON Web Tokens).
* **Data Isolation:** Enforces strict privacy where users can only view and manage their own tasks.
* **Password Security:** Utilizes Bcrypt hashing for secure password storage.

### Kanban Dashboard
* **Interactive Board:** Visual column-based layout categorizing tasks into Pending, In Progress, and Completed statuses.
* **Drag & Drop:** Utilizes `@hello-pangea/dnd` for efficient status updates via a drag-and-drop interface.
* **Responsive Cards:** Includes hover effects and quick access to View, Edit, and Delete actions.

### Data Management
* **CRUD Operations:** Complete Create, Read, Update, and Delete capabilities.
* **Soft Delete:** Implements a safety mechanism where deleted items are moved to a Recycle Bin rather than being immediately erased.
* **Recycle Bin:** Provides functionality to restore accidentally deleted items or permanently remove them from the database.

---

## Tech Stack

### Backend
* **Language:** Python 3.12+
* **Framework:** FastAPI
* **Database:** SQLite (SQLAlchemy ORM)
* **Authentication:** OAuth2 with Password Bearer, JWT (python-jose), Passlib (bcrypt)

### Frontend
* **Framework:** React.js (Vite)
* **HTTP Client:** Axios (configured with Interceptors for token management)
* **Drag & Drop:** @hello-pangea/dnd
* **Styling:** CSS Modules / Standard CSS

---

## Execution Instructions

To run this full-stack application, the Backend and Frontend services must be executed simultaneously in separate terminal instances.

### Step 1: Initialize the Backend (Python)

1.  Open a terminal and navigate to the project root directory.
2.  Create and activate a virtual environment:

    **Linux/MacOS:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

    **Windows:**
    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```

3.  Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4.  Start the FastAPI server:
    ```bash
    uvicorn backend.main:app --reload
    ```
    *The server will initialize at: `http://127.0.0.1:8000`*

### Step 2: Initialize the Frontend (React)

1.  Open a new terminal instance.
2.  Navigate to the frontend directory:
    ```bash
    cd frontend
    ```

3.  Install Node.js dependencies:
    ```bash
    npm install
    ```

4.  Run the development server:
    ```bash
    npm run dev
    ```

5.  Access the application via the browser at the provided URL (usually **http://localhost:5173**).

---
