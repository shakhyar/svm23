import sqlite3

from config import *

conn = sqlite3.connect(COMMITTEE_DB, check_same_thread=False)
c = conn.cursor()


class Committee:
    def __init__(self):
        self.l = []

        self.create_table(True)

    def create_table(self, true):
        self.true = true
        if self.true:
            c.execute("CREATE TABLE IF NOT EXISTS committee(name TEXT, prc1 TEXT, prc2 TEXT, prc3 TEXT, prp1 TEXT, prp2 TEXT, prp3 TEXT, secret TEXT)")
            conn.commit()
        else:
            pass


    def data_entry(self,name, prc1, prc2, prc3, prp1, prp2, prp3, secret):
        c.execute("INSERT INTO committee(name, prc1, prc2, prc3, prp1, prp2, prp3, secret) VALUES (?,?,?,?,?,?,?,?)",
            (name, prc1, prc2, prc3, prp1, prp2, prp3, secret))
        conn.commit()


    def read_all(self):
        c.execute("SELECT * FROM committee")
        self.l = []
        for row in c.fetchall():
            self.l.append(row)
            print(row)
        return self.l


    def delete_entry(self, secret):
        self.pid = secret
        c.execute("DELETE from committee where secret = ?", (self.pid,))
        conn.commit()
  ####################################################################################################################
    def count_unsc(self):
        c.execute("SELECT * FROM committee where prc1 = ? OR prc2 = ? OR prc3 = ?", ('UNSC', 'UNSC', 'UNSC'))
        self.size = len(c.fetchall())
        return self.size

    def count_disec(self):
        c.execute("SELECT * FROM committee where prc1 = ? OR prc2 = ? OR prc3 = ?", ('UNGA-DISEC', 'UNGA-DISEC', 'UNGA-DISEC'))
        self.size = len(c.fetchall())
        return self.size

    def count_loksabha(self):
        c.execute("SELECT * FROM committee where prc1 = ? OR prc2 = ? OR prc3 = ?", ('Lok Sabha', 'Lok Sabha', 'Lok Sabha'))
        self.size = len(c.fetchall())
        return self.size

    def count_abs(self):
        c.execute("SELECT * FROM committee where prc1 = ? OR prc2 = ? OR prc3 = ?", ('Assam Vidhan Sabha', 'Assam Vidhan Sabha', 'Assam Vidhan Sabha'))
        self.size = len(c.fetchall())
        return self.size


    def count_ipc(self):
        c.execute("SELECT * FROM committee where prc1 = ? OR prc2 = ? OR prc3 = ?", ('IPC', 'IPC', 'IPC'))
        self.size = len(c.fetchall())
        return self.size

###############################################################################
    
    def unsc1(self):
        c.execute("SELECT * FROM committee where prc1 = ?", ('UNSC',))
        self.size = len(c.fetchall())
        return self.size

    def ds1(self):
        c.execute("SELECT * FROM committee where prc1 = ?", ('UNGA-DISEC',))
        self.size = len(c.fetchall())
        return self.size

    def lk1(self):
        c.execute("SELECT * FROM committee where prc1 = ?", ('Lok Sabha',))
        self.size = len(c.fetchall())
        return self.size

    def abs1(self):
        c.execute("SELECT * FROM committee where prc1 = ?", ('Assam Vidhan Sabha',))
        self.size = len(c.fetchall())
        return self.size


    def ipc1(self):
        c.execute("SELECT * FROM committee where prc1 = ?", ('IPC',))
        self.size = len(c.fetchall())
        return self.size

###########################################################################################################################
    
    def parse_download(self, flag, secret, coms):
        c.execute(f"SELECT name, {coms} FROM committee where {flag} = '{secret}'")
        self.l = c.fetchall()
        return self.l


    def gunsc(self, flag):
        c.execute("SELECT * FROM committee where ? = ?", (flag, 'UNSC'))
        self.size = c.fetchall()
        return self.size

    def gdisec(self, flag):
        c.execute("SELECT * FROM committee where ? = ?", (flag, 'UNGA-DISEC'))
        self.size = c.fetchall()
        return self.size

    def gloksabha(self, flag):
        c.execute("SELECT * FROM committee where ? = ?", (flag, 'Lok Sabha'))
        self.size = c.fetchall()
        return self.size

    def gabs(self, flag):
        c.execute("SELECT * FROM committee where prc1 = ? OR prc2 = ? OR prc3 = ?", ('Assam Vidhan Sabha', 'Assam Vidhan Sabha', 'Assam Vidhan Sabha'))
        self.size = c.fetchall()
        return self.size


    def gipc(self, flag):
        c.execute("SELECT * FROM committee where prc1 = ? OR prc2 = ? OR prc3 = ?", ('IPC', 'IPC', 'IPC'))
        self.size = c.fetchall()
        return self.size