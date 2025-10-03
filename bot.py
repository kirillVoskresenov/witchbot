import asyncio
import logging
from telegram import Bot
from apscheduler.schedulers.blocking import BlockingScheduler
import pytz
import random
from facts import WITCH_FACTS

# === НАСТРОЙКИ ===
TELEGRAM_TOKEN = '8220586207:AAEAdbE-CquQFZomVacikZI9MWeKvfP-IHM'  # замените!
CHAT_ID = 622753203  # замените на ваш числовой chat_id


# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


def get_random_witch_fact():
    return random.choice(WITCH_FACTS)


def send_witch_fact():
    logging.info("Подготавливаю отправку факта о ведьмах...")
    fact = get_random_witch_fact()
    logging.info(f"Факт: {fact}")

    async def _send():
        bot = Bot(token=TELEGRAM_TOKEN)
        await bot.send_message(
            chat_id=CHAT_ID,
            text=f"🧙‍♀️ *Забавный факт о ведьмах:* \n\n{fact}",
            parse_mode='Markdown'
        )

    try:
        asyncio.run(_send())
        logging.info("✅ Факт отправлен!")
    except Exception as e:
        logging.error(f"❌ Ошибка: {e}")


if __name__ == '__main__':
    scheduler = BlockingScheduler(timezone=pytz.timezone('Europe/Moscow'))
    scheduler.add_job(send_witch_fact, 'cron', hour=14, minute=45)  # каждый день в 10:00
    logging.info("🧙‍♀️ Бот запущен. Факты о ведьмах — ежедневно в 10:00 по Москве.")

    try:
        scheduler.start()
    except KeyboardInterrupt:
        logging.info("Бот остановлен.")