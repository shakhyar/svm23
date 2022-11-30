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
class User:
    def __init__(self):
        self.l = []

        self.create_table(True)

    def create_table(self, true):
        self.true = true
        if self.true:
            c.execute("CREATE TABLE IF NOT EXISTS users(name TEXT, std TEXT, school TEXT, exp TEXT, fp TEXT, notes TEXT, paid INT, secret TEXT, acom TEXT)")
            conn.commit()
        else:
            pass

    def data_entry(self, n, std, school, exp, fp, notes, paid, secret, acom):
        c.execute("INSERT INTO users(name, std, school, exp, fp, notes, paid, secret, acom) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (n, std, school, exp, fp, notes, paid, secret, acom))
        conn.commit()


    def read_all(self):
        c.execute("SELECT * FROM users")
        self.l = []
        for row in c.fetchall():
            self.l.append(row)
        return self.l

    def delete_entry(self, secret):
        self.pid = secret
        c.execute("DELETE from users where secret = ?", (self.pid,))
        conn.commit()

    def update_entry(self, secret):
        self.secret = secret
        c.execute("UPDATE users SET paid = 1 WHERE secret = ?",(self.secret,))
        conn.commit()

    def read(self, name):
        self.name = name
        try:
            c.execute("SELECT * FROM users where name = ?", (self.name,))
            cs = c.fetchone()
            return [cs[0], cs[13], cs[7]]
        except IndexError:
            return [None, None]

    def read_sec(self, token):
        self.name = token
        try:
            c.execute("SELECT * FROM users where secret = ?", (self.name,))
            cs = c.fetchone()
            return cs[0]
        except TypeError:
            return None

    def paid_check(self):
        self.paid = []
        c.execute("SELECT * FROM users where paid = 1")
        rows = c.fetchall()
        for row in rows:
            self.paid.append(row)

        return self.paid


    def read_unpaid(self):
        c.execute("SELECT * FROM users WHERE paid=0")
        self.l = []
        for row in c.fetchall():
            self.l.append(row)
        return self.l



    def validate(self, ph1):
        try:
            self.ph1 = ph1
            c.execute("SELECT * FROM users where ph1 = ?", (self.ph1,))
            cs = c.fetchone()
            return [cs[0], cs[4], cs[13]]
        except IndexError:
            return [None, None]

    def update_prc(self, token, prc):
        self.token = token
        self.prc = prc
        c.execute("UPDATE users SET prc = ? WHERE secret = ?",(self.prc, self.token))
        conn.commit()

    def count_disec(self):
        c.execute("SELECT * FROM users where prc = ?", ('DISEC',))
        self.size = len(c.fetchall())
        return self.size

    def count_aippm(self):
        c.execute("SELECT * FROM users where prc = ?", ('AIPPM',))
        self.size = len(c.fetchall())
        return self.size

    def count_neppm(self):
        c.execute("SELECT * FROM users where prc = ?", ('NEPPM',))
        self.size = len(c.fetchall())
        return self.size

    def count_ipc(self):
        c.execute("SELECT * FROM users where prc = ?", ('IPC',))
        self.size = len(c.fetchall())
        return self.size

######################################################################
    def disec(self):
        c.execute("SELECT * FROM users where prc = ?", ('DISEC',))
        self.row = c.fetchall()
        self.l = []
        for i in self.row:
            self.l.append(i)
        return self.l

    def aippm(self):
        c.execute("SELECT * FROM users where prc = ?", ('AIPPM',))
        self.row = c.fetchall()
        self.l = []
        for i in self.row:
            self.l.append(i)
        return self.l

    def neppm(self):
        c.execute("SELECT * FROM users where prc = ?", ('NEPPM',))
        self.row = c.fetchall()
        self.l = []
        for i in self.row:
            self.l.append(i)
        return self.l
        
    def ipc(self):
        c.execute("SELECT * FROM users where prc = ?", ('IPC',))
        self.row = c.fetchall()
        self.l = []
        for i in self.row:
            self.l.append(i)
        return self.l
# MemoryUnit().read_all()