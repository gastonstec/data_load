
# FastAPI imports
from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
# Config imports
from core import config
# Logging imports
import logging
# Dabase imports
from psycopg_pool import ConnectionPool
import db
# Routers
import routers


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create a connection pool with a minimum of 2 connections and
#a maximum of 3 connections
pool = ConnectionPool(conninfo="user='postgres' password='c4rec4'  host='localhost' \
                      port='5432' dbname='gtim_services' application_name='fastapi'")

# Get a connection from the pool
connection1 = pool.getconn()

# Use the connection to execute a query
cursor = connection1.cursor()
cursor.execute("SELECT version()")
results = cursor.fetchall()
for data in results:
    print(data)
    print()
cursor.close()
pool.putconn(connection1)


# try: 
#     database = db.Database(config.DBSettings.user, config.DBSettings.password, config.DBSettings.host, \
#                            config.DBSettings.port, config.DBSettings.dbname, config.DBSettings.appname)
#     conn = database.connect_pool(config.DBSettings.min_size, config.DBSettings.max_size, config.DBSettings.timeout)
#     logger.info("Connected to Database")
# except Exception as e:
#         logger.error(f"Error connecting to database: {e}")
#         quit()


# FastAPI lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Start startup")
    yield
    print("Start shutdown")
    # Disconnect from database on shutdown
    pool.close()
    logger.info("Disconnect from database")
    return

    
app = FastAPI(host=config.AppSettings.host, port=config.AppSettings.port, title=config.AppSettings.name, \
              description=config.AppSettings.description, \
              version=config.AppSettings.version, lifespan=lifespan)

