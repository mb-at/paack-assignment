from src.ports.repository import PackageRepository
from src.domain.services import PackageDomainService
from src.domain.enums import PackageStatus
from src.domain.exceptions import PackageNotFoundError, InvalidStateTransitionError

class UpdatePackageStatusUseCase:
    """
    Use case: Update the status of a package.
    Receives via dependency injection:
    - A repository that implements PackageRepository.
    """

    def __init__(self, repository: PackageRepository):
        self._repository = repository

    async def execute(self, package_id: str, new_status: PackageStatus):
        """
        1. Gets the existing package from the repository.
        2. Validates and applies the state change using the domain service.
        3. Persists the updated package.
        4. Returns the package with the new state.

        Throws:
        - PackageNotFoundError if the repository cannot find the package.
        - InvalidStateTransitionError if the state change is invalid.
        """

        package = await self._repository.get_by_id(package_id)
        
        PackageDomainService.change_status(package, new_status)

        await self._repository.save(package)

        return package