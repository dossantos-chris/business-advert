from app.server.db import db

user_collection = db.users

def user_helper(user) -> dict:
    result = {
        "username": user["username"],
        "hashed_password": user["hashed_password"],
        "disabled": user["disabled"]
    }

    return result

async def get_user(username: str) -> dict:
    user = await user_collection.find_one({"username": username})
    if user:
        return user_helper(user)