from src.ports.repository import PackageRepository
from src.domain.services import PackageDomainService
from src.domain.enums import PackageStatus
from src.domain.exceptions import PackageNotFoundError, InvalidStateTransitionError

class UpdatePackageStatusUseCase:
    """
    Use case: Update the status of a package.
    Receives via dependency injection:
    - A repository that implements PackageRepository.
    - (Optional) A notification adapter that has a 'notify_status_changed' method.
    """

    def __init__(self, repository: PackageRepository, notification_adapter=None):
        self._repository = repository
        self._notification = notification_adapter

    async def execute(self, package_id: str, new_status: PackageStatus):
        """
        1. Gets the existing package from the repository.
        2. Validates and applies the state change using the domain service.
        3. Persists the updated package.
        4. (Optional) Calls the notification adapter if present.
        5. Returns the package with the new state.

        Throws:
        - PackageNotFoundError if the repository cannot find the package.
        - InvalidStateTransitionError if the state change is invalid.
        """

        package = await self._repository.get_by_id(package_id)

        PackageDomainService.change_status(package, new_status)

        await self._repository.save(package)

        if self._notification:
            #We expect the adapter to implement async def notify_status_changed(pkg)
            await self._notification.notify_status_changed(package)

        return package