"""
"""

import sqlite3


class Database:
    """"""

    def __init__(self, database) -> None:
        self.database = database

    def connect(self):
        self.connection = sqlite3.connect(self.database)
        self.cursor = self.connection.cursor()

    def disconnect(self):
        self.connection.commit()
        self.connection.close()
