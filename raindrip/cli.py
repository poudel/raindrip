import os
import sys
import time
import logging
import argparse

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from raindrip.exceptions import ConfigMissing
from raindrip.app import create_app
from raindrip.consumer import consume_messages
from raindrip.publisher import publish_messages


logger = logging.getLogger("raindrip")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Raindrip: stream OS metrics using Kafka and write them to a PostgreSQL database."
    )
    parser.add_argument("command", type=str, choices=["consumer", "publisher"])

    parser.add_argument(
        "-f",
        "--frequency",
        type=int,
        help="Streaming or Polling frequency in seconds. Applies to both commands.",
        default=3,
    )

    parser.add_argument(
        "-l",
        "--loglevel",
        type=str,
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Loglevel for verbosity. Default is INFO.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    command = args.command

    logging.basicConfig(level=args.loglevel)

    if args.command == "consumer":
        func = consume_messages
    elif args.command == "publisher":
        func = publish_messages
    else:
        logger.error(f"Unknown command: %s", command)
        return 1

    try:
        app = create_app()
    except ConfigMissing as err:
        logger.error("Failed to start. Reason: \n%s", err)
        return 1

    logger.info("Starting %s", command)
    exit_code = 0

    while True:
        try:
            func(app)
            time.sleep(args.frequency)
        except KeyboardInterrupt:
            logger.info("Gracefully stopping %s", command)
            break
        except Exception as err:
            logger.exception(err)
            logger.error("Abruptly stopping %s", command)
            exit_code = 1
            break

    # cleanup any open connection
    logger.info("Cleaning up..")
    app.cleanup()
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
