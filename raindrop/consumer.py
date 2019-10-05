import time
from raindrop.config import config
from raindrop.app import App
from raindrop.message_handlers import MessageListener


def main(app):
    """
    Entry point for raindrop consumer app.

    This listens to kafka topic for operating system metrics and
    writes them to a PostgreSQL database.
    """
    handler = MessageListener(app)

    app.logger.info("Started continuous polling...")

    while True:
        try:
            handler.poll()
            time.sleep(2)
        except KeyboardInterrupt:
            app.logger.info("Exiting consumer...")
            break
        except Exception:
            app.logger.error(f"Exiting consumer because of error")
            raise


if __name__ == "__main__":
    app = App(config)
    main(app)
