from typing import List
from beanie import Document


class User(Document):
    id        : str
    full_name : str
    user_name : str
    role      : List[str]

    class Settings:
        name = "users"