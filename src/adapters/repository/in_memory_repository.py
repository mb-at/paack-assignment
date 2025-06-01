import asyncio
from typing import Dict, List

from src.domain.entities import Package
from src.domain.exceptions import PackageNotFoundError
from src.ports.repository import PackageRepository

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
                raise PackageNotFoundError(f"Package with id {package_id} not found.")
            return package
        
    async def save(self, package: Package) -> None:
        """
        Persists or updates the Package object in in-memory storage.
        """
        async with self._lock:
            self._storage[package.id] = package

    async def preload_packages(self, packages: List[Package]) -> None:
        """
        Helper method for preloading a list of Packages into memory.
        Useful for initializing sample data when the app starts.
        """
        async with self._lock:
            for package in packages:
                self._storage[package.id] = package

    async def list_all(self) -> List[Package]:
        """
        Returns a list of all Packages currently in memory.
        """
        async with self._lock:
            return list(self._storage.values())