from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from fastapi.openapi.utils import get_openapi
from fastapi.requests import Request
from datetime import timedelta, datetime
import redis
import time
import os

from src.bot.config import bot, dp
from src.settings import settings
from src.api.router import router
from src.logger import logger


# Initialize Redis client
app = FastAPI(
    title="Note-taking Assessment Service",
    description="This API manages note-taking assessments and integrates a Telegram bot.",
    version="1.0.0",
    docs_url="/docs",  # Swagger UI accessible at /docs
    redoc_url=None,  # Disable ReDoc
    openapi_url="/openapi.json",  # OpenAPI schema URL
)

app.include_router(router)

WEBHOOK_PATH = f"/webhook/{bot.token}"
WEBHOOK_URL = f"{settings.DOMAIN}{WEBHOOK_PATH}"
redis_client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)


@app.middleware("http")
async def rate_limit_handler(request: Request, call_next):
    client_ip = request.client.host  # Use IP address as identifier
    request_key = f"rate_limit:{client_ip}:count"
    time_key = f"rate_limit:{client_ip}:time"
    block_key = f"rate_limit:{client_ip}:blocked_until"

    # Check if the client is currently blocked
    blocked_until = redis_client.get(block_key)
    if blocked_until and datetime.now() <= datetime.fromtimestamp(float(blocked_until)):
        logger.info("Client is currently blocked")
        return JSONResponse(
            content={"error": "Rate limit exceeded, try again later!"},
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        )

    # Retrieve request count and time from Redis
    request_count = redis_client.get(request_key)
    request_time = redis_client.get(time_key)

    # Convert Redis data to appropriate types
    if request_count is None:
        request_count = 0
    else:
        request_count = int(request_count)

    if request_time is None:
        request_time = time.time()
        redis_client.set(time_key, request_time)
    else:
        request_time = float(request_time)

    # Check if rate limit is exceeded
    if time.time() - request_time > settings.RATE_LIMIT_WINDOW:
        # Reset the count and time if the time window has passed
        redis_client.set(request_key, 1)
        redis_client.set(time_key, time.time())
    elif request_count >= settings.RATE_LIMIT_COUNT:
        # Block the client if the request count exceeds the limit
        logger.info("Rate limit exceeded")
        block_until_time = datetime.now() + timedelta(seconds=settings.BLOCK_DURATION)
        redis_client.set(
            block_key, block_until_time.timestamp(), ex=settings.BLOCK_DURATION
        )
        return JSONResponse(
            content={"error": "Rate limit exceeded, try again later!"},
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        )
    else:
        # Increment the request count within the time window
        redis_client.incr(request_key)

    response = await call_next(request)
    return response


@app.get("/")
async def welcome_handler():
    return JSONResponse(
        content={"msg": "Welcome to the Note-taking Assessment Service"}
    )


@app.on_event("startup")
async def on_startup():
    await bot.set_webhook(WEBHOOK_URL)


@app.on_event("shutdown")
async def on_shutdown():
    await bot.delete_webhook()
    await bot.session.close()


@app.post(WEBHOOK_PATH)
async def bot_webhook_handler(update: dict):
    telegram_update = types.Update(**update)
    await dp.feed_update(bot=bot, update=telegram_update)


@app.get("/hello")
async def get_hello():
    return JSONResponse({"msg": "Hello"})


# Customizing the OpenAPI schema
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Note-taking Assessment Service",
        version="1.0.0",
        description="This is a custom OpenAPI schema for the Note-taking Assessment Service.",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


# Assign the custom OpenAPI schema function
app.openapi = custom_openapi
