class InvalidStatusCode(Exception):
    pass


class InvalidProtocolVersion(Exception):
    pass


class ConnectionClosed(Exception):
    pass


class ProtocolException(Exception):
    pass


class StatusException(ProtocolException):
    pass
