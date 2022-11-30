import sqlite3

from config import *

conn = sqlite3.connect(AMB_DB, check_same_thread=False)
c = conn.cursor()

class Amb:
    def __init__(self):
        self.l = []

        self.create_table(True)

    def create_table(self, true):
        self.true = true
        if self.true:
            c.execute("CREATE TABLE IF NOT EXISTS amb(name TEXT, code TEXT, secret TEXT)")
            conn.commit()
        else:
            pass


    def data_entry(self, name, code, secret):
        c.execute("INSERT INTO amb(name, code, secret) VALUES (?, ?, ?)",
            (name, code, secret))
        conn.commit()


    def read_all(self):
        c.execute("SELECT * FROM amb")
        self.l = []
        for row in c.fetchall():
            self.l.append(row)
            print(row)
        return self.l


    def delete_entry(self, secret):
        self.pid = secret
        c.execute("DELETE from amb where secret = ?", (self.pid,))
        conn.commit()
  