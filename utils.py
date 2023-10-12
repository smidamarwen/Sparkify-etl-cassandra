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

