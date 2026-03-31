from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app import models, schemas, crud, auth
from app.database import engine, get_db
from app.auth import get_current_active_user, require_admin
from fastapi.security import OAuth2PasswordRequestForm
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Microservice API")

# Auth endpoints
@app.post("/auth/register", response_model=schemas.UserOut, status_code=201)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)

@app.post("/auth/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# Items CRUD
@app.post("/items/", response_model=schemas.ItemOut, status_code=201)
def create_item(
    item: schemas.ItemCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    return crud.create_item(db=db, item=item, owner_id=current_user.id)

@app.get("/items/", response_model=List[schemas.ItemOut])
def read_items(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    # For regular users, show only their own items; admin sees all
    owner_id = None if current_user.role == "admin" else current_user.id
    items = crud.get_items(db, skip=skip, limit=limit, owner_id=owner_id)
    return items

@app.get("/items/{item_id}", response_model=schemas.ItemOut)
def read_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    item = crud.get_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    # Admin can see any item; regular users only their own
    if current_user.role != "admin" and item.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    return item

@app.put("/items/{item_id}", response_model=schemas.ItemOut)
def update_item(
    item_id: int,
    item: schemas.ItemCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    db_item = crud.get_item(db, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    if current_user.role != "admin" and db_item.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    return crud.update_item(db, item_id, item)

@app.delete("/items/{item_id}", status_code=204)
def delete_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    db_item = crud.get_item(db, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    if current_user.role != "admin" and db_item.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    crud.delete_item(db, item_id)
    return

# Admin endpoint
@app.get("/admin/users", response_model=List[schemas.UserOut])
def get_all_users(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin)
):
    users = db.query(models.User).all()
    return users