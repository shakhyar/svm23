import sqlite3

from config import *

conn = sqlite3.connect(CONTACTS_DB, check_same_thread=False)
c = conn.cursor()

class Contacts:
    def __init__(self):
        self.l = []

        self.create_table(True)

    def create_table(self, true):
        self.true = true
        if self.true:
            c.execute("CREATE TABLE IF NOT EXISTS contacts(emailed INT, name TEXT, email TEXT, ph1 INT, ph2 INT, secret TEXT)")
            conn.commit()
        else:
            pass


    def data_entry(self, emailed, name, email, ph1, ph2, secret):
        c.execute("INSERT INTO contacts(emailed, name, email, ph1, ph2, secret) VALUES (?, ?, ?, ?, ?, ?)",
            (emailed, name, email, ph1, ph2, secret))
        conn.commit()


    def read_all(self):
        c.execute("SELECT * FROM contacts")
        self.l = []
        for row in c.fetchall():
            self.l.append(row)
            print(row)
        return self.l

    def update_entry(self, secret):
        self.secret = secret
        c.execute("UPDATE contacts SET emailed = 1 WHERE secret = ?",(self.secret,))
        conn.commit()

    def delete_entry(self, secret):
        self.pid = secret
        c.execute("DELETE from contacts where secret = ?", (self.pid,))
        conn.commit()
  