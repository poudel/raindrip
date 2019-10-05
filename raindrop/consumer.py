from raindrop.config import config
from raindrop.app import App
from raindrop.message_handlers import MessageHandler


def consume_messages(app):
    handler = MessageHandler(app)
    handler.before()

    app.logger.info("Started continuous polling...")

    while True:
        try:
            handler.poll()
        except KeyboardInterrupt:
            app.logger.info("Exiting consumer...")
            break
        except Exception:
            app.logger.error(f"Exiting consumer because of error")
            raise

    handler.after()


if __name__ == "__main__":
    app = App(config)
    consume_messages(app)
