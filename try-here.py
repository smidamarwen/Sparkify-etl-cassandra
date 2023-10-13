from utils import *

#
# cluster = Cluster(['localhost'])
# session = cluster.connect()
# df = load_data(fields=['sessionId', 'artist', 'song', 'length'])
# query = '''INSERT INTO my_keyspace_test.songs_by_sessionID(sessionID, artist, song, length) VALUES (?,?,?,?)'''
# preparedStatement = session.prepare(query)
# df['song'] = df['song'].fillna('Empty Song')
# df['length'] = df['length'].fillna(0)
# df['artist'] = df['artist'].fillna('Empty Artist')

#
# for item in df.iterrows():
#     session.execute(preparedStatement, (item[1]["sessionId"], item[1]["artist"], item[1]["song"], item[1]["length"]))



# nan_counts = whole.isna().sum()
create_table_info_by_userid()
