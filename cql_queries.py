create_table_1 = """CREATE TABLE IF NOT EXISTS songs_by_sessionID (
        sessionID INT,
        artist TEXT,
        song TEXT,
        length FLOAT,
        PRIMARY KEY (sessionID)
    );"""


