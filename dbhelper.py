import os
from urllib import parse
import psycopg2

class DBhelper:
    
    def __init__(self):
        parse.uses_netloc.append("postgres")
        self.url = parse.urlparse(os.environ["DATABASE_URL"])
        self.conn = psycopg2.connect(
            database=self.url.path[1:],
            user=self.url.username,
            password=self.url.password,
            host=self.url.hostname,
            port=self.url.port
        )
    def setup(self):
        cur = self.conn.cursor()
        cur.execute('''CREATE TABLE register2
        (ID INT NOT NULL,
        NAME TEXT NOT NULL,
        SID TEXT NOT NULL);''')
        self.conn.commit()
    def add_item(self,item_list):
        cur = self.conn.cursor()
        cur.execute("""INSERT INTO register2 (ID,NAME,SID)
        VALUES (%s,%s,%s)""",(item_list[0],item_list[1],item_list[2]))
        self.conn.commit()
    def delete_item(self,ID):
        cur = self.conn.cursor()
        cur.execute("""DELETE from register2 where ID={};""".format(ID))
        self.conn.commit()
    def get_item(self):
        cur = self.conn.cursor()
        cur.execute("""SELECT NAME,SID from register2""")
        return(cur.fetchall())
