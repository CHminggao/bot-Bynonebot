'''
Author: GM
Date: 2021-11-23 20:22:45
LastEditors: GM
LastEditTime: 2021-11-23 21:44:39
Description: file content
'''
import sqlite3
import random
async def connectdb(uri):
    return sqlite3.connect(uri)
class data_source:
    async def create_table(uri):
        conn=await connectdb(uri)
        c=conn.cursor()
        c.execute('''
        CREATE TABLE tiangou
           (Content   TEXT  NOT NULL);
        ''')
        conn.commit()
        conn.close()
    
    async def insertContent(uri,text)->bool:
        conn=await connectdb(uri)
        c=conn.cursor()
        c.execute("INSERT INTO tiangou(Content) VALUES(:Content)",{"Content":text})
        conn.commit()
        conn.close()
        return True
    
    async def selectContent(uri)->str:
        conn=await connectdb(uri)
        c=conn.cursor()
        cursor = c.execute("SELECT * FROM tiangou ORDER BY RANDOM() limit 1")
        text=""
        
        for row in cursor:
            text = row[0]
        conn.close()
        return text
    
    async def cleals_table(uri)->bool:
        conn=await connectdb(uri)
        c=conn.cursor()
        state=True
        try:
            c.execute("DELETE FROM tiangou")
            conn.commit()
        except:
            state=False
            print("sql error")
        conn.close()
        return state