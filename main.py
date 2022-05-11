from fastapi import FastAPI
import aioredis

from routers.user import usersRouter
from routers.course import courseRouter
from config import *

app = FastAPI()

app.include_router(courseRouter,prefix='/course', tags=['course'])
app.include_router(usersRouter, prefix="/user", tags=['users'])


async def get_redis_pool() -> aioredis.Redis:
    redis = await aioredis.from_url(f"redis://:@"+redishost+":"+redisport+"/"+redisdb+"",
                                    encoding="utf-8",
                                    decode_responses=True)
    return redis


@app.on_event("startup")
async def startup_event():
    app.state.redis = await get_redis_pool()


@app.on_event("shutdown")
async def shutdown_event():
    app.state.redis.close()
    await app.state.redis.wait_closed()


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app='main:app', host="127.0.0.1", port=8000, reload=True, debug=True)