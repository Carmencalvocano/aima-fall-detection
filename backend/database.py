import sqlite3

connection = sqlite3.connect("falls.db")

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS falls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_type TEXT,
    timestamp TEXT,
    confidence REAL,
    source TEXT
)
""")

connection.commit()

print("Base de datos creada correctamente")

connection.close()