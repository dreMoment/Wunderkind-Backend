import mysql.connector
from mysql.connector import Error

# change below depending on the password you set for your MySQL
mydb = mysql.connector.connect(
    #for local db:
    host="192.168.1.38",
    user="wunderkind_user",
    passwd="toor1234",
    port=3307
    )

my_cursor = mydb.cursor()
my_cursor.execute("DROP DATABASE IF EXISTS wunderkind")
my_cursor.execute("CREATE DATABASE wunderkind")

my_cursor.execute("SHOW DATABASES")
for db in my_cursor:
    print(db)

#Can only connect to the proper database on the official backend and not the local one
"""

mydb = mysql.connector.connect(
    host="mysql.inf.ethz.ch",
    user="grossm_virtual_teacher2",
    passwd="PnUzaZmnsZ2ir1gHpxVFneBl",
    database="grossm_virtual_teacher2"
)

my_cursor = mydb.cursor()
my_cursor.execute("SHOW DATABASES")
for db in my_cursor:
    print(db)
"""
