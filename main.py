import atexit
import os.path
import sqlite3
import io
import os
from Repository import Repository

if os.path.isfile("Output.db") is False:
    repo = Repository()
    repo.create_tables()
else:
    repo = Repository()


class Hats:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, hat):
        self._conn.execute("""
                       INSERT INTO hats(id, topping,supplier, quantity) VALUES (?, ?, ?, ?)
                   """, [hat.id, hat.topping, hat.supplier, hat.quantity])

    def find(self, hat_id):
        cur = self._conn.cursor()
        cur.execute("""
                   SELECT id, topping,supplier, quantity FROM hats WHERE id = ?
               """, [hat_id])
        return Hat(*cur.fetchone())

    def try_order(self, topping_name):
        cur = self._conn.cursor()
        cur.execute("""
                           SELECT id,topping,MIN(supplier), quantity FROM hats WHERE topping = ? AND (SELECT count(*) FROM hats WHERE topping = ?)>1
                       """, [topping_name, topping_name])
        return Hat(*cur.fetchone())

    def order_one(self, hat_id):
        self._conn.execute("""
                       UPDATE hats SET quantity=quantity-1 WHERE id=(?)
                   """, [hat_id])
        self._conn.execute("""
                               DELETE FROM hats WHERE id=(?) AND quantity=0
                           """, [hat_id])


class Hat:
    def __init__(self, id, topping, supplier, quantity):
        self.quantity = quantity
        self.supplier = supplier
        self.id = id
        self.topping = topping


class Suppliers:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, supplier):
        self._conn.execute("""
                          INSERT INTO suppliers(id, name) VALUES (?, ?)
                      """, [supplier.id, supplier.name])

    def find(self, supplier_id):
        cur = self._conn.cursor()
        cur.execute("""
                      SELECT id, name FROM suppliers WHERE id = ?
                  """, [supplier_id])

        return Supplier(*cur.fetchone())


class Supplier:
    def __init__(self, id, name):
        self.name = name
        self.id = id


class Orders:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, order):
        self._conn.execute("""
                          INSERT INTO orders(id, location,hat) VALUES (?, ?, ?)
                      """, [order.id, order.location, order.hat])

    def find(self, order_id):
        cur = self._conn.cursor()
        cur.execute("""
                      SELECT id, topping,supplier, quantity FROM orders WHERE id = ?
                  """, [order_id])

        return Hat(*cur.fetchone())


class Order:
    def __init__(self, id, location, hat):
        self.hat = hat
        self.location = location
        self.id = id


order_id_tracker = 1
Orders1 = Orders(repo.conn)
Hats1 = Hats(repo.conn)
Suppliers = Suppliers(repo.conn)
oparsedOrders = [["myHouse", "none"]]
summery = open("Summery.txt", "w+")
for order_req in oparsedOrders:
    hat = Hats1.try_order(order_req[1])
    if hat.id is not None:
        Hats1.order_one(hat.id)
        supplier = Suppliers.find(hat.supplier)
        order = Order(0, order_req[0], hat.topping)
        Orders1.insert(order)
        order_id_tracker = order_id_tracker + 1
        summery.write("{topping},{supplier},{location}\n".format(topping=hat.topping, supplier=supplier.name,
                                                                 location=order_req[0]))

repo._close()
