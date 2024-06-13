import asyncio
import asyncpg
from core.logger import get_logger
from db.postgres import DATABASE_DNS
from core.settings import settings

_logger = get_logger(__name__)


DB_CONF = {
    "user": settings.DB_USER,
    "password": settings.DB_PASSWORD,
    "host": settings.DB_HOST,
    "port": settings.DB_PORT,
    "database": settings.DB_NAME,
}


async def main():
    """Wait connect to db"""
    time_sleep = 5
    while True:
        try:
            connection = await asyncpg.connect(**DB_CONF)
            result = await connection.fetch("SELECT 1;")
            await connection.close()
            break
        except Exception as e:
            _logger.info(e)
            _logger.info("Wait connect to db")
            await asyncio.sleep(time_sleep)
            time_sleep += 3
    loop = asyncio.get_event_loop()
    loop.stop()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
