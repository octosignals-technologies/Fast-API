from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import mysql.connector
from mysql.connector import Error
from pydantic import BaseModel
from typing import List
from datetime import datetime

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
    id: int
    number: str
    message: str
    created_on: datetime

class MarkReadRequest(BaseModel):
    ids: List[int]

@app.get("/data", response_model=List[Message])
async def get_data():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)

        query = "SELECT id, number, message, created_on FROM Inbox WHERE is_read = 0"
        cursor.execute(query)
        results = cursor.fetchall()

        cursor.close()
        connection.close()
        return results

    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

@app.post("/mark-as-read")
async def mark_as_read(request: MarkReadRequest):
    if not request.ids:
        raise HTTPException(status_code=400, detail="No message IDs provided.")

    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Use parameterized query
        format_strings = ','.join(['%s'] * len(request.ids))
        query = f"UPDATE Inbox SET is_read = 1 WHERE id IN ({format_strings})"
        cursor.execute(query, tuple(request.ids))
        connection.commit()

        affected_rows = cursor.rowcount

        cursor.close()
        connection.close()

        return JSONResponse(content={"marked_as_read": affected_rows})

    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")
