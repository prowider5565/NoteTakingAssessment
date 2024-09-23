from fastapi.responses import JSONResponse
from datetime import timedelta, datetime
from fastapi.requests import Request
from fastapi import FastAPI, status
import time

from src.bot.config import bot, dp
from src.settings import settings
from src.api.router import router
from src.logger import logger


app = FastAPI()
app.include_router(router)
WEBHOOK_PATH = f"/webhook/{bot.token}"
WEBHOOK_URL = f"{settings.DOMAIN}{WEBHOOK_PATH}"


@app.middleware("http")
async def rate_limit_handler(request: Request, call_next):
    if hasattr(app.state, "request_count"):
        logger.info(f"Request count exist, incrementing {app.state.request_count}")
        app.state.request_count += 1
    else:
        logger.info("Request count doesnt exist, setting one")
        app.state.request_count = 1
    request_count = app.state.request_count
    if hasattr(app.state, "request_time"):
        request_time = app.state.request_time
    else:
        request_time = app.state.request_time = time.time()

    if (time.time() - request_time > 3) and request_count > 3:
        logger.info("Rate limit exceeded")
        if not hasattr(app.state, "reload_time"):
            app.state.reload_time = None
        if app.state.reload_time is None:
            logger.info("Blocking requests")
            app.state.reload_time = datetime.now() + timedelta(seconds=10)
            return JSONResponse(
                content={"error": "Rate limit exceeded, try again later!"},
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            )
        elif datetime.now() <= app.state.reload_time:
            logger.info("Request in block, it is not time to allow")
            return JSONResponse(
                content={"error": "Rate limit exceeded, try again later!"},
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            )
        elif datetime.now() > app.state.reload_time:
            logger.info("Allowing requests")
            app.state.reload_time = None
            app.state.request_count = 0
            app.state.request_time = time.time()
    response = await call_next(request)
    return response


@app.get("/")
async def welcome_handler():
    return JSONResponse(
        content={"msg": "Welcome to the Note taking Assessment Service"}
    )


@app.on_event("startup")
async def on_startup():
    # routers = []
    # dp.include_routers(*routers)
    await bot.set_webhook(WEBHOOK_URL)


@app.on_event("shutdown")
async def on_shutdown():
    await bot.delete_webhook()
    await bot.session.close()


@app.post(WEBHOOK_PATH)
async def bot_webhook_handler(update: dict):
    telegram_update = types.Update(**update)
    await dp.feed_update(bot=bot, update=telegram_update)


@app.get("/")
async def get_hello():
    return JSONResponse({"msg": "Hello"})
