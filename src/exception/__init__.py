class GrapherException(Exception):
    pass


class NoStartNodeFound(GrapherException):
    pass


class IdNotFound(GrapherException):
    pass


class StoredQueryException(GrapherException):
    pass


class StoredQueryAlreadyExists(StoredQueryException):
    pass
