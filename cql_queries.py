create_table_1 = """CREATE TABLE IF NOT EXISTS %s.songs_by_sessionID (
        sessionID INT,
        itemInSession INT,
        artist TEXT,
        song TEXT,
        length FLOAT,
        PRIMARY KEY (sessionID, itemInSession)
    );"""

insert_table_1 = '''INSERT INTO %s.songs_by_sessionID(sessionID, itemInSession, artist, song, length) VALUES (?,?,?,?)'''


create_table_2 = """CREATE TABLE IF NOT EXISTS %s.info_by_userid (
        userId INT,
        sessionID INT,
        itemInSession INT,
        artist TEXT,
        song TEXT,
        firstName TEXT,
        lastName TEXT,
        PRIMARY KEY (userId, sessionID)
    );"""