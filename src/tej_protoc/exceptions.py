class ConnectionClosed(Exception):
    """ Raises when connection is closed. """

    pass


class ProtocolException(ConnectionClosed):
    """
    Extends `ConnectionClosed` exception class. This will raise when the protocol bytes are constructed
    improperly.
    """

    pass


class InvalidStatusCode(ProtocolException):
    """ This exception will be raised when the invalid status code is received in MSB. """

    pass


class InvalidProtocolVersion(ProtocolException):
    """ This exception will be raised when the invalid protocol version is read in the data frame. """

    pass

