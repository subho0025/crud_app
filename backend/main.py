from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

from backend import database
from backend import models
from backend import schema

def get_db():
    db=database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

@app.get("/")
def get_root():
    return {"message": "Welcome to main page"}

@app.post("/tasks", response_model=schema.Responser)
def create_task(task: schema.Creater,db: Session = Depends(get_db)):
    db_task = models.Task(title=task.title,description=task.description,status=task.status)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    return db_task

print("This is corrct")

@app.get("/tasks", response_model=list[schema.ResponseList])
def get_all_tasks(db: Session=Depends(get_db)):
    task = (db.query(models.Task).filter(models.Task.deleted.is_(False)).all())
    return task

@app.get("/tasks/{task_id}", response_model=schema.Responser)
def get_task(task_id: int,db: Session=Depends(get_db)):
    task = (db.query(models.Task).filter(models.Task.deleted.is_(False)).filter(models.Task.id==task_id).first())
    
    if not task:
        raise HTTPException(status_code=404, detail= f"task with id {task_id} not found")
    
    return task

@app.patch("/tasks/{task_id}", response_model= schema.Responser)
def update_task(task_id : int,task_update: schema.Updater, db: Session=Depends(get_db)):
    task = (db.query(models.Task).filter(models.Task.id==task_id).filter(models.Task.deleted.is_(False)).first())
    
    if not task:
        raise HTTPException(status_code = 404, detail = f"task with {task_id} not found")
    
    if task_update.title is not None:
        task.title = task_update.title

    if task_update.description is not None:
        task.description = task_update.description

    if task_update.title is not None:
        task.status = task_update.status

    db.commit()
    db.refresh(task)
    return task

# @app.delete("/tasks/{task_id}")
# def tempDelete_task(task_id : int):
#     for index, t in enumerate(tasks):
#         if t.id == task_id and not t.deleted:
#             t.deleted = True
#             return {"message" : f"task {task_id} moved to recycle bin"}
            
#     raise HTTPException(status_code=404, detail= f"task with id {task_id} not found")

# @app.get("/recycle-bin", response_model=List[Task])
# def get_deleted_tasks():
#     return [t for t in tasks if t.deleted]

# @app.put("/recycle-bin/{task_id}")
# def restore_task(task_id : int):
#     for t in tasks:
#         if t.id == task_id and t.deleted:
#             t.deleted = False
#             return {"message" : f"task {task_id} restored successfully"}
        
#     raise HTTPException(status_code=404, detail = f"task with id {task_id} not found")

# @app.delete("/recycle-bin/{task_id}")
# def permntDelete(task_id : int):
#     for index, t in enumerate(tasks):
#         if t.id == task_id and t.deleted:
#             tasks.pop(index)
#             return {"message": f"task {task_id} permanently deleted"}
        
#     raise HTTPException(status_code= 404, detail = f"task with id {task_id} not found")