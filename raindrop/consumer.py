class BaseConsumer:

    def __init__(self, config, *args, **kwargs):
        self.config = config

    def start(self):
        """
        Should basically ready the consumer to consume messages. Could
        be something like establishing connection to another service.
        """
        pass

    def stop(self):
        """
        To cleanup if there is anything to clean up before destroying.
        """
        pass

    def on_message(self, message):
        raise NotImplementedError


class WriteToPostgresConsumer(BaseConsumer):

    def on_message(self, message):
        # vaidate jsonschema
        # use the connection to write to the db
        pass
