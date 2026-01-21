# *Task Management Dashboard (CRUD Application)*.
This is a full stack Management application based on CRUD. It features a modern "Dashboard" interface, a *Recycle Bin* for safely restoring deleted items, and a "Soft Delete" system.

## Key Features
- *Create & Edit:* Add new tasks or update existing ones (change status to Pending, In Progress, or Completed).
- *Soft Delete:* Clicking "Delete" moves items to the Recycle Bin instead of erasing them immediately.
- *Recycle Bin:* View deleted items and choose to *Restore* them or *Permanently Delete* them.
- *Persistent Database:* Uses SQLite for zero-configuration data storage.
- *Modern UI:* Built with React & Vite, featuring a clean, centered dashboard layout.

## Tech Stack
- *Backend* - Python 3.12, FastApi, Pydantic, SQLAlchemy.
- *Frontend* - React.js, Vite, Axios, CSS Module.
- *Database* - SQLite (Auto-generated file sql_app.db - no server installation required).

## How to execute the project
Since this is a full-stack application, you need to run this on two terminals one for running the frontend while the other for running the backend of the full-stack simultaneously.

### Step 1: Start the Backend(Python)

  1. Open terminal and navigate to the basic_crud_app folder
  
  2. create and activate the virtual environment (Recommended):  
  **Linux/MacOS**
   ```bash
    python3 -m venv venv
    source venv/bin/activate
  ```
  **Windows**
  ```bash
    python -m venv venv
    venv\Scripts\activate
   ```
 
 3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

 4. Start the server:
   ```bash
   uvicorn main:app --reload
   ```
  You should see: Uvicorn running on http://127.0.0.1:8000

 <!--list break-->
   ---
   
   ### Step 2: Start the Frontend (React)

1.  Open a *new* terminal window and navigate to the frontend folder:
    ```bash
    cd frontend
    ```

2.  Install the node modules:
    ```bash
    npm install
    ```

3.  Run the development server:
    ```bash
    npm run dev
    ```

4.  Open your browser and visit the link shown (usually *http://localhost:5173*).

---
