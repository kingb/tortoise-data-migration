import logging

from app.models import Country
from tortoise import Tortoise, run_async

from tortoise_data_migration import upgrade

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

config = {
    "connections": {
        "default": "sqlite:///tmp/some-db.sqlite3",
        "non-default": "sqlite:///tmp/another-db.sqlite3",
    },
    "apps": {
        "models": {
            "models": ["app.models", "tortoise_data_migration.models"],
            "default_connection": "default",
        }
    },
}


async def init():
    logger.info("Starting app")
    await Tortoise.init(config=config)

    await Tortoise.generate_schemas()

    await upgrade(base_package="my_data_migrations", connection_name="non-default")

    logger.info("Available countries:")
    for country in await Country.all():
        logger.info(f" - {country.code} | {country.name}")


if __name__ == "__main__":
    run_async(init())
