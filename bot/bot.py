"""
Minimal Telegram Bot (aiogram 3) + Static WebApp Host (aiohttp) for English -> Uzbek Word Cards.
- Serves static files from webapp/ on 0.0.0.0:$PORT (for Railway / cloud deployment).
- /start sends a short Uzbek welcome message with an inline WebApp button "So'zlarni o'rganish".
- Configures the bot's chat menu button to open the WebApp automatically.
"""

from __future__ import annotations

import asyncio
import logging
import os
import time
from pathlib import Path

from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    MenuButtonWebApp,
    Message,
    WebAppInfo,
)
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent
WEBAPP_DIR = ROOT_DIR / "webapp"
ENV_PATH = ROOT_DIR / ".env"
load_dotenv(dotenv_path=ENV_PATH)

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()


def resolve_webapp_url() -> str:
    explicit = os.getenv("WEBAPP_URL", "").strip()
    railway_domain = os.getenv("RAILWAY_PUBLIC_DOMAIN", "").strip()
    if railway_domain:
        return f"https://{railway_domain}"
    return explicit


dp = Dispatcher()


@dp.message(CommandStart())
async def cmd_start(message: Message) -> None:
    base_url = resolve_webapp_url()
    sep = "&" if "?" in base_url else "?"
    fresh_url = f"{base_url}{sep}t={int(time.time())}"
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="So'zlarni o'rganish",
                    web_app=WebAppInfo(url=fresh_url),
                )
            ]
        ]
    )
    await message.answer(
        "Assalomu alaykum! Inglizcha – oʻzbekcha soʻz kartochkalarini oʻrganish uchun quyidagi tugmani bosing:",
        reply_markup=keyboard,
    )


async def configure_menu_button(bot: Bot) -> None:
    base_url = resolve_webapp_url()
    if not base_url.startswith("https://"):
        logging.warning("Skipping MenuButton setup because WEBAPP_URL is not HTTPS yet: %s", base_url)
        return
    sep = "&" if "?" in base_url else "?"
    versioned_url = f"{base_url}{sep}v={int(time.time())}"
    await bot.set_chat_menu_button(
        menu_button=MenuButtonWebApp(
            text="So'zlarni o'rganish",
            web_app=WebAppInfo(url=versioned_url),
        )
    )
    logging.info("Configured Telegram MenuButton -> %s", versioned_url)


@web.middleware
async def nocache_middleware(request: web.Request, handler):
    response = await handler(request)
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


async def index_handler(request: web.Request) -> web.FileResponse:
    return web.FileResponse(WEBAPP_DIR / "index.html")


async def health_handler(request: web.Request) -> web.Response:
    return web.json_response({"status": "ok", "webapp_url": resolve_webapp_url()})


def create_web_app() -> web.Application:
    app = web.Application(middlewares=[nocache_middleware])
    app.router.add_get("/", index_handler)
    app.router.add_get("/index.html", index_handler)
    app.router.add_get("/health", health_handler)
    app.router.add_static("/", path=str(WEBAPP_DIR), show_index=False)
    return app


async def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

    port = int(os.getenv("PORT", "8080"))
    app = create_web_app()
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host="0.0.0.0", port=port)
    await site.start()
    logging.info("Serving static Mini App from %s on http://0.0.0.0:%d", WEBAPP_DIR, port)

    if not BOT_TOKEN:
        logging.warning("BOT_TOKEN is not set; running static web server only.")
        await asyncio.Event().wait()
        return

    bot = Bot(token=BOT_TOKEN)
    await bot.delete_webhook(drop_pending_updates=True)
    await configure_menu_button(bot)

    try:
        await dp.start_polling(bot, handle_signals=False)
    finally:
        await bot.session.close()
        await runner.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
