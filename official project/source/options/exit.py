class Exit(object):
    def __init__(self, exit_message):
        self.message = exit_message

    def __call__(self, *args, **kwargs):
        raise ExitError(message=self.message)

    @staticmethod
    def default_exit():
        return Exit("Thanks for using this program.")


class ExitError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return repr(self.message)
