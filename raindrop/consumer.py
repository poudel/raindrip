import time
from config import config
from app import App
from message_handlers import MessageListener


def main():
    """
    Entry point for raindrop consumer app.

    This listens to kafka topic for operating system metrics and
    writes them to a PostgreSQL database.
    """
    app = App(config)
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
    main()
