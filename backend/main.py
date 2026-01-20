from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Task (BaseModel):
    id : int
    title : str
    description : str
    status : str
    deleted : bool = False


tasks : List[Task] =[]


@app.get("/")
def get_root():
    return {"message": "Welcome to main page"}

@app.post("/tasks", response_model=Task)
def create_task(task : Task):
    for t in tasks:
        if t.id == task.id:
            raise HTTPException(status_code=400, detail= f"task with id {task.id} already exists")
    
    task.deleted = False
    tasks.append(task)
    return task

@app.get("/tasks", response_model=List[Task])
def get_all_tasks():
    return [t for t in tasks if not t.deleted]

@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id : int):
    for t in tasks:
        if t.id == task_id and not t.deleted:
            return t
        
    raise HTTPException(status_code=404, detail= f"task with id {task_id} not found")

@app.put("/tasks/{task_id}", response_model= Task)
def update_task(task_id : int, updated_task : Task):
    if updated_task.id != task_id:
        raise HTTPException(status_code=400, detail= "task id mismatch")
    
    for t in tasks:
        if t.id == task_id and not t.deleted:
            t.title = updated_task.title
            t.description = updated_task.description
            t.status = updated_task.status
            return t
        
    raise HTTPException(status_code = 404, detail = f"task with {task_id} not found")

@app.delete("/tasks/{task_id}")
def tempDelete_task(task_id : int):
    for index, t in enumerate(tasks):
        if t.id == task_id and not t.deleted:
            t.deleted = True
            return {"message" : f"task {task_id} moved to recycle bin"}
            
    raise HTTPException(status_code=404, detail= f"task with id {task_id} not found")

@app.get("/recycle-bin", response_model=List[Task])
def get_deleted_tasks():
    return [t for t in tasks if t.deleted]

@app.put("/recycle-bin/{task_id}")
def restore_task(task_id : int):
    for t in tasks:
        if t.id == task_id and t.deleted:
            t.deleted = False
            return {"message" : f"task {task_id} restored successfully"}
        
    raise HTTPException(status_code=404, detail = f"task with id {task_id} not found")

@app.delete("/recycle-bin/{task_id}")
def permntDelete(task_id : int):
    for index, t in enumerate(tasks):
        if t.id == task_id and t.deleted:
            tasks.pop(index)
            return {"message": f"task {task_id} permanently deleted"}
        
    raise HTTPException(status_code= 404, detail = f"task with id {task_id} not found")