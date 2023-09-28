class ConnectionClosed(Exception):
    pass


class ProtocolException(ConnectionClosed):
    pass


class InvalidStatusCode(ProtocolException):
    pass


class InvalidProtocolVersion(ProtocolException):
    pass


class StatusException(ProtocolException):
    pass
