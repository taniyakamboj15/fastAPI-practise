"""
app/db/session.py

This module simulates a database connection.
In a real production app, this is where you would configure SQLAlchemy or an async database driver.

Since we are restricted to no database, we use global dictionaries to store data in memory.
WARNING: All data is lost when the application restarts.
"""

from typing import List, Dict, Any

# Types for our in-memory data
UserDict = Dict[str, Any]
ItemDict = Dict[str, Any]

class FakeDB:
    """
    A simple class to hold our in-memory data.
    Acts as a singleton to simulate a persistent data store.
    """
    def __init__(self):
        # Users table: mapping ID -> User Data
        self.users: Dict[int, UserDict] = {}
        # Items table: mapping ID -> Item Data
        self.items: Dict[int, ItemDict] = {}
        
        # Auto-increment counters
        self.user_id_counter = 1
        self.item_id_counter = 1

    def get_users(self) -> List[UserDict]:
        return list(self.users.values())

    def get_user_by_email(self, email: str) ->  UserDict | None:
        for user in self.users.values():
            if user["email"] == email:
                return user
        return None
        
    def create_user(self, user_data: UserDict) -> UserDict:
        user_id = self.user_id_counter
        user_data["id"] = user_id
        self.users[user_id] = user_data
        self.user_id_counter += 1
        return user_data

    # ... other CRUD methods would go here, 
    # but we can also access .users directly for simplicity in this demo.

# Global instance
db = FakeDB()
