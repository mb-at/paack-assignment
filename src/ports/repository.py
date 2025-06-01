from abc import ABC, abstractmethod
from typing import List
from src.domain.entities import Package

class PackageRepository(ABC):
    """
    Interface (port) for the package repository.
    Any implementation (in-memory, database-based, etc.)
    must inherit from this class and provide the methods declared here.
    """

    @abstractmethod
    async def get_by_id(self, package_id: str) -> Package:
        """
        Gets a Package from its ID.
        Must throw a PackageNotFoundError exception if it doesn't exist.
        """
        ...

    @abstractmethod
    async def save(self, package: Package) -> None:
        """
        Persists or updates a Package in storage.
        """
        ...

    @abstractmethod
    async def list_all(self) -> List[Package]:
        """
        Returns all stored packages.
        """