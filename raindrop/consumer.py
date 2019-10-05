from raindrop.message_handlers import MessageHandler


def consume_messages(config):
    handler = MessageHandler(config)
    handler.before()

    while True:
        print("Polling...")
        try:
            handler.poll()
        except KeyboardInterrupt:
            print("Exiting consumer...")
            break
        except Exception:
            print(f"Exiting consumer because of error")
            raise

    handler.after()
