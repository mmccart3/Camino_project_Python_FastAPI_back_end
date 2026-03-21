from mysql.connector import connect
from dotenv import load_dotenv
import os

def connect_to_db():
    # global mycursor, dbconnection
        
    load_dotenv()

    host = os.environ.get("HOST")
    user = os.environ.get("USER")
    password = os.environ.get("PASSWORD")
    port = os.environ.get("PORT")
    database = os.environ.get("DATABASE")
    print(f"{host}, {user}, {password}, {port}, {database}")

    dbconnection = connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    print(dbconnection, "line 24"  )
 
    return dbconnection

