class ErrorBin:
    def __init__(self, max_errors=100):
        """
        Create a new error bin.

        :param max_errors: The maximum number of errors to store for each field
        """
        self.max_errors = max_errors
        self.errors = {}

    def add(self, field: str, error: str):
        """
        Add an error to the error bin.

        :param field: The field the error is for
        :param error: The error message

        :return: None
        """
        if field not in self.errors:
            self.errors[field] = [error]
        elif len(self.errors[error]) < self.max_errors:
            self.errors[field].append(error)
        else:
            self.errors[field].append("...")

    def add_bin(self, field: str, error_bin):
        """
        Add a nested error bin to the error bin.

        :param error_bin: The error bin to add
        :
        """
        if error_bin.has_errors():
            self.errors[field] = error_bin.get()

    def has_errors(self):
        """
        Check if the error bin has any errors.

        :return: True if there are errors, False otherwise
        """
        return len(self.errors) > 0

    def get(self):
        """
        Get the errors in the error bin.

        :return: A dictionary of errors with the field as the key and a list of errors as the value
        """
        return self.errors
