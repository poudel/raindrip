
class ConfigMissing(Exception):

    def __init__(self, missing):
        msg = f"Missing environment variables: {missing}"
        super().__init__(msg)
