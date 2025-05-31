from .entities import Package
from .enums import PackageStatus
from .exceptions import InvalidStateTransitionError

class PackageDomainService:
    """
    Domain Service: Contains the business logic that
    validates and enforces a Package's state transitions.
    """

    @staticmethod
    def change_status(package: Package, new_status: PackageStatus) -> None:
        """
        Validates and applies a status change.
        The rules are:
        READY -> IN_TRANSIT -> DELIVERED
        Any other combination should be considered invalid.
        """

        current = package.status

        if current == PackageStatus.READY and new_status == PackageStatus.IN_TRANSIT:
            package.status = new_status
            return

        if current == PackageStatus.IN_TRANSIT and new_status == PackageStatus.DELIVERED:
            package.status = new_status
            return

        raise InvalidStateTransitionError(
            f"Transición inválida de estado: {current} -> {new_status}"
        )