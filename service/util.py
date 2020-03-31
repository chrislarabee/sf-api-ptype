
class Config:
    """
    A simply object for holding and passing around various constants
    used by the API service.
    """
    def __init__(self, **kwargs):
        """

        Args:
            kwargs: Using this approach allows an arbitrarily large
                number of attributes to be stored in Config with
                minimal effort. If a kwarg becomes important enough to
                be declared during each init, then it should be added
                below.
        """
        self.username = None
        self.password = None
        self.security_token = None
        # tables will be used by the Codex to limit the scope of tables
        # it collects from the linked Salesforce instance. Useful if
        # you know exactly what tables you need and want to run the
        # Codex as efficiently as possible.
        self.tables = tuple()
        for k, v in kwargs.items():
            setattr(self, k, v)
