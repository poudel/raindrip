import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from raindrip.app import create_app
from raindrip.consumer import consume_messages
from raindrip.publisher import publish_messages


def main():
    if len(sys.argv) < 2:
        print("Usage: `cli.py consumer` or `cli.py publisher`")
        sys.exit(1)

    app = create_app()
    command = sys.argv[1]

    if command == "consumer":
        func = consume_messages
    elif command == "publisher":
        func = publish_messages
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

    app.logger.info(f"Starting {command}")
    exit_code = 0

    while True:
        try:
            func(app)
            time.sleep(2)
        except KeyboardInterrupt:
            app.logger.info(f"Gracefully stopping {command}")
            break
        except Exception as err:
            app.logger.exception(err)
            app.logger.error("Abruptly stopping {command}")
            exit_code = 1

    # cleanup any open connection
    app.logger.info("Cleaning up..")
    app.cleanup()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
