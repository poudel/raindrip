import json
import time
from raindrop.kafka_utils import kafka


class MessageHandler:

    def __init__(self, config):
        self.config = config

    def on_message(self):
        pass


def read_message(message):
    try:
        print(json.loads(message.value.decode("utf-8")))
    except json.JSONDecodeError as err:
        print(f"Could not decode: {message.value}\n {err}")


if __name__ == "__main__":
    print("Polling...")

    while True:
        try:
            topic_messages = kafka.consumer.poll(timeout_ms=1000)
            for topic, messages in topic_messages.items():
                for message in messages:
                    read_message(message)

            time.sleep(3)
        except KeyboardInterrupt:
            print("Exiting raindrop consumer...")
            break
