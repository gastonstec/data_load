# from functools import lru_cache
from psycopg_pool import ConnectionPool
from core import DBSettings
import logging

# Constants
ERR_MSG_DB_EMPTY_PARAMS: str = "Some database connection parameters are empty"
ERR_MSG_DB_POOL_PARAMS: str = "Error on connection pool parameters"


            
class Database:

    # Class init
    def __init__(self):
        # Properties
        self.user:str = DBSettings.user
        self.password: str = DBSettings.password
        self.host: str = DBSettings.host
        self.port: int = DBSettings.port
        self.dbname: str = DBSettings.dbname
        self.appname: str = DBSettings.appname

        # Params validation
        # self.user = user if user=="" else DBSettings.user
        # self.password = password if password=="" else DBSettings.password
        # self.host = host if host=="" else DBSettings.host
        # self.port = port if port=="" else DBSettings.port
        # self.dbname = dbname if dbname=="" else DBSettings.dbname
        # self.appname = appname if appname=="" else DBSettings.appname
        # self.conn = None

    # Create and returns a Connection Pool
    def connect_pool(self, min_size: int, max_size: int, timeout: float):
        # Check db pool parameters
        if min_size < 1 or max_size < 1 or timeout < 0 or min_size > max_size \
            or min_size > 100 or max_size > 100 or timeout > 60:
            raise ValueError(ERR_MSG_DB_POOL_PARAMS)

        # Build connection string
        connstr =  f"user={self.user} " \
            f"password={self.password} " \
            f"host={self.host} " \
            f"port={self.port} " \
            f"dbname={self.dbname} " \
            f"application_name='{self.appname}'"  
        # Create pool 
        conn_pool = ConnectionPool(conninfo=connstr, min_size=min_size, max_size=max_size, timeout=timeout)

        # Check connection
        try:
            conn = conn_pool.getconn()
            with conn.cursor() as cur:
                cur.execute("SELECT version()")
                result = cur.fetchone()
                # logging.logger.info(f"Pool connected to: {result}")
            # Commit changes (if any)
            conn.commit()
            conn_pool.putconn(conn)
        except Exception as e:
            #logger.error(f"Error connecting pool to PostgreSQL: {e}")
            self.conn.rollback() # Rollback in case of error
            raise ValueError(e)
        
        # Return ConnectionPool
        return conn_pool
    

    # Close pool
    def close_pool(pool: ConnectionPool):
        try:
            pool.close()
        except Exception as e:
            raise ValueError(e)
        return
