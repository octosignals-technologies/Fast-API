from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import mysql.connector
from mysql.connector import Error
from pydantic import BaseModel
from typing import List

app = FastAPI()

# MySQL configuration
db_config = {
    'host': 'mysql',  # Changed to 'mysql' for Docker compatibility
    'user': 'your_username',
    'password': 'your_password',
    'database': 'your_database'
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
        query = "SELECT number, message FROM messages WHERE status = 0"
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
