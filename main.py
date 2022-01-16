import sqlite3

from Repository import Repository

connection = sqlite3.connect('Output.db')
repo = Repository()
repo.create_tables()

class students:
    def __init__(self, conn):
        print("todo")
    def insert(self):

    def find(self):

