import MySQLdb
import sys
import redis 
from datetime import datetime
import time
import cPickle
import hashlib

startTime = datetime.now()
R_SERVER = redis.Redis("redis")

db = MySQLdb.connect("mysql","root","password")
cursor = db.cursor()
CURSOR = db.cursor()
cursor.execute("DROP DATABASE IF EXISTS USERDB")
cursor.execute("CREATE DATABASE USERDB")
cursor.execute("USE USERDB")
sql = """CREATE TABLE users (
	 ID int,
	 USER char(30)
 )"""
cursor.execute(sql)
cursor.execute("""INSERT into users values(1,'Jon Doe')""")
db.commit()
cursor.execute("""INSERT into users values(2,'Jane Doe')""") 
db.commit()
cursor.execute("""INSERT into users values(3,'Carolyn Brown')""") 
db.commit()
cursor.execute("""INSERT into users values(4,'Amelia Anderson')""") 
db.commit()


id=4

def cache_redis(id, TTL = 36):
    hash = hashlib.sha224(str(id)).hexdigest()
    key = "sql_cache:" + hash
    
    if (R_SERVER.get(key)):
        print "[C] " + R_SERVER.get(key) 
    else:
    
        CURSOR.execute("select user from users where id=" + str(id))
        data = CURSOR.fetchone()[0]

        R_SERVER.set(key,data)
        R_SERVER.expire(key, TTL);
 		
       	print R_SERVER.get(key)

if __name__ == '__main__':
    cache_redis(id)