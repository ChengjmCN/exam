from fastapi import FastAPI, Request
from aioredis import create_redis_pool, Redis
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from config import *
from routers.paper import paperRouter

app = FastAPI()


# async def get_redis_pool() -> Redis:
#     redis = await create_redis_pool(f"redis://:@" + redishost + ":" + redisport + "/" + redisdb + "?encoding=utf-8")
#     return redis
#
#
# @app.on_event("startup")
# async def startup_event():
#     app.state.redis = await get_redis_pool()
#
#
# @app.on_event("shutdown")
# async def shutdown_event():
#     app.state.redis.close()
#     await app.state.redis.wait_closed()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        content=jsonable_encoder({"message": exc.errors(), "code": 421}),
    )


app.include_router(paperRouter, prefix="/exam", tags=['exams'])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app='main:app', host="127.0.0.1", port=8000, reload=True, debug=True)
