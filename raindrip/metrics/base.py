class MetricCollector:
    """
    Base metric collector class.

    All metric classes should subclass this class and implement the
    `collect` method. The `collect` should contain the actual logic
    that gets the metric from the OS.

    The module that contain your subclasses should be registered in
    the config file so that it can be discovered.

    ```
    metrics_modules = [
        ...,
        "path.to.your.metrics_module",
    ]
    ```

    """

    key: str

    def collect(self):
        """
        Should be implemented in your metric subclass.

        The return value should be a valid JSON-serializable object.
        """
        raise NotImplementedError
