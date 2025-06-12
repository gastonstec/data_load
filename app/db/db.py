# from functools import lru_cache
from psycopg_pool import ConnectionPool
from fastapi import FastAPI

# Constants
ERR_MSG_DB_EMPTY_PARAMS: str = "Some database connection parameters are empty"
ERR_MSG_DB_POOL_PARAMS: str = "Error on connection pool parameters"

            
class Database:

    # Class init
    def __init__(self, user: str, password: str, \
                 host: str, port: int, dbname: str, appname: str):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.dbname = dbname
        self.appname = appname
        self.conn = None
    
    def _check_db_parameters(self):
         # Check pool settings
        if self.user == "" or self.password == "" or self.host == "" \
            or self.port == "" or self.dbname == "" or self.appname == "":
           raise ValueError(ERR_MSG_DB_EMPTY_PARAMS) 
    
    # Create and returns a Connection Pool
    def connect_pool(self, min_size: int, max_size: int, timeout: float):

        # Check db parameters
        try:
            self._check_db_parameters()
        except Exception as e:
            raise ValueError(e)
        
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
        self.conn = ConnectionPool(conninfo=connstr, min_size=min_size, max_size=max_size, timeout=timeout)

        # Check connection
        try:
            with self.conn.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT version()")
                    result = cur.fetchone()
                    print(f"Pool connected to: {result}")

            # Commit changes (if any)
            conn.commit()
        except Exception as e:
            #logger.error(f"Error connecting pool to PostgreSQL: {e}")
            self.conn.rollback() # Rollback in case of error
            raise ValueError(e)
        
        # Return ConnectionPool
        return self.conn
    

    # Close pool
    def close_pool(self, pool: ConnectionPool):
        try:
            pool.close()
            pool.wait()
        except Exception as e:
            raise ValueError(e)
        return
