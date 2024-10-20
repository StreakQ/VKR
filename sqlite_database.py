import sqlite3
from database_interface import DatabaseInterface

class SQLiteDatabase(DatabaseInterface):
    def __init__(self, database):
        self.database = database

    def connect(self):
        self.conn = sqlite3.connect(self.database)

    def disconnect(self):
        self.conn.close()

    def execute_query(self, query):
        cursor = self.conn.cursor()
        cursor.execute(query)
        return cursor

    def fetch_all(self, cursor):
        return cursor.fetchall()