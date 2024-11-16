"""
Weather Processing App
Student: Chi Kin Lee
DBCM class manage the database connections
"""
import sqlite3

class DBCM:
    """ DBCM is a database connections manager """
    def __init__(self, dbname):
        self.dbname = dbname
        try:
            self.conn = sqlite3.connect(self.dbname)
            print("Opened database successfully.")
        except Exception as e:
            print("Error in opening database:", e)

    def __enter__(self):
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_value, exc_trace):
        self.conn.commit()
        self.conn.close()