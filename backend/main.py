from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm

from backend import database
from backend import models
from backend import schema
from backend import auth

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)

models.Base.metadata.create_all(bind=database.engine)


#root
@app.get("/")
def get_root():
    return {"message": "Welcome to main page"}

@app.post("/register", response_model=schema.UserResponse)
def register_user(user: schema.UserCreate, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_pwd = auth.get_password_hash(user.password)
    new_user = models.User(username=user.username, hashed_password=hashed_pwd)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/login", response_model=schema.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

#create task
@app.post("/tasks", response_model=schema.Responser)
def create_task(task: schema.Creater,db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_task = models.Task(**task.dict(), owner_id=current_user.id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    return db_task

#get all valid tasks
@app.get("/tasks", response_model=list[schema.ResponseList])
def get_all_tasks(db: Session=Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    task = (db.query(models.Task).filter(models.Task.deleted.is_(False)).filter(models.Task.owner_id == current_user.id).all())
    return task

#get single task
@app.get("/tasks/{task_id}", response_model=schema.Responser)
def get_task(task_id: int,db: Session=Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    task = (db.query(models.Task).filter(models.Task.deleted.is_(False), models.Task.id == task_id, models.Task.owner_id == current_user.id).first())
    
    if not task:
        raise HTTPException(status_code=404, detail= f"task with id {task_id} not found")
    
    return task

#update task
@app.patch("/tasks/{task_id}", response_model= schema.Responser)
def update_task(task_id : int,task_update: schema.Updater, db: Session=Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    task = (db.query(models.Task).filter(models.Task.id==task_id, models.Task.deleted.is_(False), models.Task.owner_id == current_user.id).first())
    
    if not task:
        raise HTTPException(status_code = 404, detail = f"task with {task_id} not found")
    
    if task_update.title is not None:
        task.title = task_update.title

    if task_update.description is not None:
        task.description = task_update.description

    if task_update.status is not None:
        task.status = task_update.status

    db.commit()
    db.refresh(task)
    return task

#soft delete task
@app.delete("/tasks/{task_id}")
def tempDelete_task(task_id : int,db: Session=Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    task=(db.query(models.Task).filter(models.Task.deleted.is_(False), models.Task.owner_id == current_user.id, models.Task.id == task_id).first())
    
    if not task:
        raise HTTPException(status_code=404, detail= f"task with id {task_id} not found")
    
    task.deleted=True
    db.commit()

    return {"message": f"task {task_id} deleted"}
    
#get soft deleted tasks
@app.get("/recycle-bin", response_model=list[schema.ResponseList])
def get_trash(db: Session=Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    task = (db.query(models.Task).filter(models.Task.deleted.is_(True), models.Task.owner_id == current_user.id).all())
    return task

#restore soft deleted task
@app.put("/recycle-bin/{task_id}")
def restore_task(task_id : int,db:Session=Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    task=(db.query(models.Task).filter(models.Task.deleted.is_(True), models.Task.id == task_id, models.Task.owner_id == current_user.id).first())
    
    if not task:
        raise HTTPException(status_code=404, detail= f"task with id {task_id} not found")
    
    task.deleted=False
    db.commit()
    db.refresh(task)

    return {"message": f"task {task_id} restored"}

#hard delete
@app.delete("/recycle-bin/{task_id}")
def permntDelete(task_id : int,db:Session=Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    task=(db.query(models.Task).filter(models.Task.deleted.is_(True), models.Task.owner_id == current_user.id, models.Task.id==task_id).first())
    
    if not task:
        raise HTTPException(status_code= 404, detail = f"task with id {task_id} not found")
    db.delete(task)
    db.commit()

    return{ "message": f"task with id {task_id}Deleted permanently "}