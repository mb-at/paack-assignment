import logging

from src.ports.repository import PackageRepository
from src.domain.services import PackageDomainService
from src.domain.enums import PackageStatus
from src.domain.exceptions import PackageNotFoundError, InvalidStateTransitionError

logger = logging.getLogger(__name__) 

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

        logger.info("UseCase: Updating package %s to status %s", package_id, new_status)

        try:
            package = await self._repository.get_by_id(package_id)
        except PackageNotFoundError:
            logger.error("UseCase: Package %s not found", package_id)
            raise
    
        try:
            PackageDomainService.change_status(package, new_status)
            logger.info("UseCase: State changed for package %s (new status=%s)", package_id, new_status)
        except InvalidStateTransitionError as e:
            logger.warning("UseCase: Invalid state transition for package %s: %s", package_id, e)
            raise

        await self._repository.save(package)

        return package