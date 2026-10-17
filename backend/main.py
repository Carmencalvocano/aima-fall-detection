import sqlite3
from fastapi import FastAPI
from datetime import datetime
from pydantic import BaseModel # Para definir modelos de datos
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class FallEvent(BaseModel):
    event_type: str
    confidence: float
    source: str
falls = []


@app.get("/")
def root():
    return {
        "message": "AIMA Backend Running"
    }


@app.get("/falls")
def get_falls():

    connection = sqlite3.connect("falls.db")

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM falls
        """
    )

    rows = cursor.fetchall()

    connection.close()

    return rows


@app.post("/falls")
def create_fall(fall: FallEvent):

    connection = sqlite3.connect("falls.db")

    cursor = connection.cursor()

    timestamp = datetime.now().isoformat()

    cursor.execute(
        """
        INSERT INTO falls (
            event_type,
            timestamp,
            confidence,
            source
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            fall.event_type,
            timestamp,
            fall.confidence,
            fall.source
        )
    )

    connection.commit()

    connection.close()

    return {
        "message": "Event stored successfully"
    }