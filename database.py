from bson.objectid import ObjectId
import motor.motor_asyncio
import asyncio

client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017')
database = client.todo
collection = database.sample
user_collection = database.user

async def fetch_one_todo(id):
    document = await collection.find_one({"_id": ObjectId(id)})
    return document

def Todo_helper(todos) -> dict:
    return {
        "id": str(todos["_id"]),
        "name": todos["name"],
        "age": todos["age"]
    }

async def fetch_all_todo():
    todos = []
    cursor = collection.find({})
    async for i in cursor:
        todos.append(Todo_helper(i))
    return todos

async def create_todo(todo):
    document = todo
    await collection.insert_one(document)
    return document

async def update_todo(id,name):
    await collection.find_one_and_update({"_id": ObjectId(id)},{"$set":{"name":name.name,"age":name.age}})
    document = await collection.find_one({"_id": ObjectId(id)})
    return document

async def remove_todo(id):
    await collection.delete_one({"_id": ObjectId(id)})
    return True

async def fetch_all_user():
    usernames = []
    cursor = user_collection.find({})
    async for i in cursor:
        usernames.append(i['username'])
    return usernames
