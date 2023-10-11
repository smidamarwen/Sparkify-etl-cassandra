import os
import pandas as pd
from functools import wraps

from cassandra.cluster import Cluster


def cassandra_connection(ip, keyspace):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cluster = Cluster([ip])
            session = cluster.connect(keyspace)
            try:
                return func(session, cluster, *args, **kwargs)
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



