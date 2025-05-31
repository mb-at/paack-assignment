class InvalidStateTransitionError(Exception):
    """
    Domain Exception: Thrown when an attempt is made to invalidly change the state of a package.
    """
    pass

class PackageNotFoundError(Exception):
    """
    Domain Exception: Thrown when a package cannot be found by its ID.
    """
    pass