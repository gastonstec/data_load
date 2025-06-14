
# FastAPI imports
from fastapi import FastAPI
from contextlib import asynccontextmanager
# Config imports
from app import routers
from core import config
# Dabase imports
from psycopg_pool import ConnectionPool
from db import Database
#from routers import admin


# FastAPI lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Connect database on startup
    try:
        db = Database()
        app.conn_pool = db.connect_pool(min_size=config.DBSettings.min_size, \
                                     max_size=config.DBSettings.max_size, timeout=config.DBSettings.timeout)
    except Exception as e:
        app.logger.error(f"Error connecting to database: {e}")
        quit()
    yield
    # Disconnect from database on shutdown
    try:
        app.conn_pool.close()
    except Exception as e:
        raise ValueError(e)
    return

    
app = FastAPI(host=config.AppSettings.host, port=config.AppSettings.port, title=config.AppSettings.name, \
              description=config.AppSettings.description, \
              version=config.AppSettings.version, lifespan=lifespan)

# Set routers
app.include_router(routers.admin)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("hello:app", reload=True)
    print("uvicorn started")

