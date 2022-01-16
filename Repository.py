import sqlite3


class Repository:
    def __init__(self):
        self.conn = sqlite3.connect("Output.db")

    def _close(self):
        self.conn.commit()
        self.conn.close()

    def create_tables(self):
        self.conn.executescript(
            "CREATE TABLE hats(id INTEGER PRIMARY KEY, topping STRING NOT NULL, supplier INTEGER REFERENCES supplier(id));"
            "CREATE TABLE suppliers(id INTEGER PRIMARY KEY, name STRING NOT NULL);"
            "CREATE TABLE orders(id INTEGER PRIMARY KEY,location STRING NOT NULL, hat INTEGER REFERENCES hats(id));"
            )