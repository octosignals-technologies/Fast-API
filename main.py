from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import mysql.connector
from mysql.connector import Error
from pydantic import BaseModel
from typing import List

app = FastAPI()

# MySQL configuration
db_config = {
    'host': '38.242.140.179',
    'port': 3306,
    'user': 'twilioclouddb',
    'password': 'M!aPyC4ewi3!Ze5c',
    'database': 'twilioclouddb'
}

class Message(BaseModel):
    number: str
    message: str

@app.get("/data", response_model=List[Message])
async def get_data():
    try:
        # Connect to MySQL
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)

        # Query records where status = 0
        query = "SELECT number, message FROM Inbox WHERE is_read = 1"
        cursor.execute(query)
        results = cursor.fetchall()

        # Close database connection
        cursor.close()
        connection.close()

        return results

    except Error as e:
        raise HTTPException(
            status_code=500,
            detail=f"Database error: {str(e)}"
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Server error: {str(e)}"
        )
