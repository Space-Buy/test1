from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from auth.models import TodoModel

app=FastAPI()

from database import (
    fetch_all_todo,
    remove_todo,
    update_todo,
    create_todo
)

origins=["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins= origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

######################################################################################################################################################
"""

                                                            USERS

"""
######################################################################################################################################################
from auth.hashing import Hash
from auth.jwttoken import create_access_token, create_superuser_token
from auth.oauth import get_current_user,get_superuser
from auth.models import User
from fastapi.security import OAuth2PasswordRequestForm
from database import fetch_all_user

from pymongo import MongoClient
mongodb_uri = 'mongodb://127.0.0.1:27017'
port = 8000
client = MongoClient(mongodb_uri, port)
data_base=client["todo"]
user_collection = data_base["user"]



@app.post("/signup", tags=["users"])
async def create_user(request: User,current_user:User = Depends(get_superuser)):
    # user_detail=user_collection.find_one({"username":current_user})
    # if user_detail['is_employee'] and user_detail['is_staff']:
    usernames=await fetch_all_user()
    if(request.username not in usernames ):
        hashed_pass = Hash.bcrypt(request.password)
        user_object = dict(request)
        user_object["password"] = hashed_pass
        user_collection.insert_one(user_object)
        access_token = create_access_token(data={"sub": request.username })
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = 'This username is alredy register or Password Mismatch')
    return {"access_token":access_token}
    
@app.post('/login', tags=["users"])
def login(request:OAuth2PasswordRequestForm = Depends()):
    if request.username == 'superuser' and request.password == 'a':
        access_token = create_superuser_token(data={"sub": request.username })
        return {"access_token": access_token, "token_type": "superuser_token","login":"Login success"}
    else:
        user = user_collection.find_one({"username":request.username})
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f'No user found with this {request.username} username')
        if not Hash.verify(user["password"],request.password):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f'Wrong Username or password')
        access_token = create_access_token(data={"sub": user["username"] })
        return {"access_token": access_token, "token_type": "bearer","log_in":"Login success"}

######################################################################################################################################################
"""

                                                            Datas

"""
######################################################################################################################################################


@app.get("/todo/get", tags=["datas"])
async def get_todo(current_user:User = Depends(get_current_user)):
    user_detail=user_collection.find_one({"username":current_user})
    response = await fetch_all_todo()
    context={"response":response,"user":current_user,"is_staff":user_detail['is_staff'],"is_employee":user_detail['is_employee']}
    return context
    
@app.post("/todo/create", response_model=TodoModel, tags=["datas"])
async def post_todo(name: TodoModel,current_user:User = Depends(get_current_user)):
    user_detail=user_collection.find_one({"username":current_user})
    if user_detail['is_employee']:
        response = await create_todo(name.dict())
        if response:
            return response
    raise HTTPException(400, "something wrong")

@app.put("/todo/update/{id}", response_model=TodoModel, tags=["datas"])
async def put_todo(id:str,name: TodoModel,current_user:User = Depends(get_current_user)):
    user_detail=user_collection.find_one({"username":current_user})
    if user_detail['is_staff']:
        response = await update_todo(id,name)
        if response:
            return response
    raise HTTPException(404, "something wrong")

@app.delete("/todo/delete/{id}", tags=["datas"])
async def delete_todo(id: str,current_user:User = Depends(get_current_user)):
    user_detail=user_collection.find_one({"username":current_user})
    if user_detail['is_employee']:
        response = await remove_todo(id)
        if response:
            return response
    raise HTTPException(404, "something wrong")