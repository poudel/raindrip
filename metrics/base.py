class BaseMetric:
    """
    Base metric class

    All metric classes should subclass this class and implement the
    `collect` method. The `collect` should contain the actual logic
    that gets the metric from the OS.
    """

    key: str
    description: str

    def collect(self):
        """
        Should be implemented in your metric subclass.

        The return value should be a valid JSON-serializable object.
        """
        raise NotImplementedError
