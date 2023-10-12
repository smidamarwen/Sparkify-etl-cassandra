import os

import numpy as np
import pandas as pd
from cassandra import ConsistencyLevel
from cassandra.cluster import Cluster
from cassandra.query import BatchStatement
from cql_queries import *
from functools import wraps


def cassandra_connection(ip):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cluster = Cluster([ip])
            session = cluster.connect()
            try:
                return func(session, *args, **kwargs)
            finally:
                session.shutdown()
                cluster.shutdown()

        return wrapper

    return decorator


def load_files_list(path):
    files_list = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".csv"):
                files_list.append(os.path.join(root, file))
    return files_list


def all_in_one(files_list):
    dfs = [pd.read_csv(
        file, usecols=['artist',
                       'firstName',
                       'gender',
                       'itemInSession',
                       'lastName',
                       'length',
                       'level',
                       'location',
                       'sessionId',
                       'song',
                       'userId']
    ) for file in files_list]
    concat_df = pd.concat(dfs).reset_index(drop=True)
    concat_df.to_csv("event_datafile_new.csv", index=False)


# TODO:  Load data from Snowflake

# Create cassandra keyspace
@cassandra_connection('localhost')
def create_keyspace(session, keysapce, strategy='SimpleStrategy', replication_factor=1):
    '''
    strategy = 'SimpleStrategy' | 'NetworkTopologyStrategy'
    '''
    session.execute(
        """CREATE KEYSPACE IF NOT EXISTS %s
         WITH replication = {'class': '%s', 
         'replication_factor': %s};""" % (keysapce, strategy, replication_factor))


@cassandra_connection('localhost')
def set_keyspace(session, keyspace):
    session.set_keyspace(keyspace)


def load_data(fields):
    df = pd.read_csv(
        'event_datafile_new.csv', usecols=fields
    )
    return df


@cassandra_connection('localhost')
def create_songs_by_sessionId(session, keyspace='my_keyspace_test'):
    set_keyspace(keyspace)
    # Create table songs_by_sessionID
    session.execute(create_table_1 % keyspace)
    print('Table created')
    # Prepare data to be loaded into the table
    df = load_data(fields=['sessionId', 'itemInSession', 'artist', 'song', 'length'])
    query = '''INSERT INTO %s.songs_by_sessionID(sessionID, itemInSession, artist, song, length) 
                VALUES (?,?,?,?,?)''' % keyspace
    preparedStatement = session.prepare(query)
    df['song'] = df['song'].fillna('Empty Song')
    df['length'] = df['length'].fillna(0)
    df['artist'] = df['artist'].fillna('Empty Artist')

    for item in df.iterrows():
        session.execute(preparedStatement, (item[1]["sessionId"],item[1]["itemInSession"], item[1]["artist"], item[1]["song"], item[1]["length"]))