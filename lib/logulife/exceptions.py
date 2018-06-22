class LogulifeException(Exception):

    pass


class NotFoundException(LogulifeException):

    pass


class NoCredentialsProvidedException(LogulifeException):

    msg = 'You need to provide either a token or a username with a password'

    def __init__(self):

        super().__init__(self.msg)


class BadHostnameException(LogulifeException):

    pass


class NetworkException(LogulifeException):

    pass


class WrongCredentialsException(LogulifeException):

    msg = 'Username or password is incorrect'

    def __init__(self):

        super().__init__(self.msg)


class BadUrlException(LogulifeException):

    msg = 'Wrong url passed. Rigth form: <app_name>:<url>'

    def __init__(self):

        super().__init__(self.msg)


class BadConfigPath(LogulifeException):

    pass

class PermissionDeniedException(LogulifeException):

    pass
