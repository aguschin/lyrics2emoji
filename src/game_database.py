from typing import TypedDict

from pymongo import MongoClient
from pymongo.collection import Collection
from streamlit import secrets

MAIN: str = "Main"
SCORE: str = "Score"


class Score(TypedDict):
    username: str
    score: int
    datetime: str


class GameDB:

    @staticmethod
    def get_db_uri() -> str:
        user_name: str = secrets["mongo"]["username"]
        user_pass: str = secrets["mongo"]["password"]

        uri: str = f"mongodb+srv://{user_name}:" \
                   f"{user_pass}@cluster0.ec67wlo.mongodb.net/?retryWrites" \
                   "=true&w=majority"

        return uri

    def __init__(self) -> None:
        self.client: MongoClient = MongoClient(GameDB.get_db_uri())
        assert self.is_connected(), "not connected to database"

    def is_connected(self) -> bool:
        try:
            self.client.admin.command('ping')
            print("You successfully connected to MongoDB!")
        except Exception as e:
            print(e)
            return False
        else:
            return True

    def score(self) -> Collection:
        return self.client[MAIN][SCORE]
