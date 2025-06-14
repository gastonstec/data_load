# FastAPI imports
from fastapi import FastAPI


@app.get("/")
async def root():
    return {"message": "OK"}

# @app.get("/db")
# async def db_version():
#     try:
#         conn = pool.getconn()
#         with conn.cursor() as cur:
#             cur.execute("SELECT version()")
#             result = cur.fetchone()
#     except Exception as e:
#         logger.error(f"Error connecting to database: {e}")
#     pool.putconn(conn)
#     return result