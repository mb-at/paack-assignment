import asyncio
import logging
from typing import Dict, List

from src.domain.entities import Package
from src.domain.exceptions import PackageNotFoundError
from src.ports.repository import PackageRepository

logger = logging.getLogger(__name__)

class InMemoryPackageRepository(PackageRepository):
    """
    In-memory implementation of PackageRepository.
    Uses an internal dictionary and asyncio.Lock to ensure
    that operations are atomic in asynchronous environments.
    """
   
    def __init__(self):
        # Map package_id -> Package
        self._storage: Dict[str, Package] = {}
        # Lock to avoid race conditions in get/save
        self._lock = asyncio.Lock()

    async def get_by_id(self, package_id: str) -> Package:
        """
        Returns the Package whose id matches package_id.
        If it doesn't exist, throws PackageNotFoundError.
        """
        async with self._lock:
            package = self._storage.get(package_id)
            if package is None:
                logger.warning("get_by_id: Package %s not found", package_id)
                raise PackageNotFoundError(f"Package with id {package_id} not found.")
            logger.debug("get_by_id: returning package %s (status=%s)", package_id, package.status)
            return package
        
    async def save(self, package: Package) -> None:
        """
        Persists or updates the Package object in in-memory storage.
        """
        async with self._lock:
            self._storage[package.id] = package
            logger.info("save: Package %s saved/updated (status=%s)", package.id, package.status)

    async def preload_packages(self, packages: List[Package]) -> None:
        """
        Helper method for preloading a list of Packages into memory.
        Useful for initializing sample data when the app starts.
        """
        async with self._lock:
            for package in packages:
                self._storage[package.id] = package
                logger.info("preload_packages: Loaded package %s (address=%s)", package.id, package.customer_address)

    async def list_all(self) -> List[Package]:
        """
        Returns a list of all Packages currently in memory.
        """
        async with self._lock:
            logger.debug("list_all: returning %d packages", len(self._storage))
            return list(self._storage.values())