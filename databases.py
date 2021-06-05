import sqlite3
from sqlite3 import Error

def sql_connection():

    try:

        con = sqlite3.connect('cpi-scrapper.db')

        return con

    except Error:

        print(Error)

def sql_table(con):

    cursorObj = con.cursor()

    cursorObj.execute("""CREATE TABLE IF NOT EXISTS basket_categories
    (id integer PRIMARY KEY AUTOINCREMENT ,
     product_name text,
      category_carrefour text,
      category_coto text,
      category_dia text,
      category_jumbo text)""")

    con.commit()

def insert(con):
    cursorObj = con.cursor()
    entities = []
    cursorObj.execute('''INSERT INTO employees(
    product_name,
     category_carrefour,
      category_dia,
       category_jumbo)
       VALUES(?, ?, ?, ?)''', entities)


    con.commit()

con = sql_connection()

sql_table(con)
insert(con)
