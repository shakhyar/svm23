import sqlite3

from config import *

conn = sqlite3.connect(USER_DB, check_same_thread=False)
c = conn.cursor()

"""
'name'
'std'
'school'
'email'
'ph1'
'ph2'
'prc'
'prp'
'exp'
'fp'
'notes'
'paid'
'secret'
"""
class Paid:
    def __init__(self):
        self.l = []

        self.create_table(True)

    def create_table(self, true):
        self.true = true
        if self.true:
            c.execute("CREATE TABLE IF NOT EXISTS paid(name TEXT, secret TEXT)")
            conn.commit()
        else:
            pass


    def data_entry(self, n, secret):
        c.execute("INSERT INTO paid(name, secret) VALUES (?, ?)",
            (n, secret))
        conn.commit()


    def read_all(self):
        c.execute("SELECT * FROM paid")
        self.l = []
        for row in c.fetchall():
            self.l.append(row)
            print(row)
        return self.l


    def delete_entry(self, secret):
        self.pid = secret
        c.execute("DELETE from paid where secret = ?", (self.pid,))
        conn.commit()
  