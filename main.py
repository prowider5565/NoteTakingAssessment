from fastapi.responses import JSONResponse
from fastapi import FastAPI


app = FastAPI()
WEBHOOK_PATH = f"/webhook/{bot.token}"
WEBHOOK_URL = f"{settings.DOMAIN}{WEBHOOK_PATH}"


@app.get("/")
async def welcome_handler():
    return JSONResponse(
        content={"msg": "Welcome to the Note taking Assessment Service"}
    )


@app.on_event("startup")
async def on_startup():
    routers = [message_router]
    dp.include_routers(*routers)
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
