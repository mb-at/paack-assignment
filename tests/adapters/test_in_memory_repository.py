import pytest
from src.adapters.repository.in_memory_repository import InMemoryPackageRepository
from src.domain.entities import Package
from src.domain.exceptions import PackageNotFoundError

@pytest.mark.asyncio
async def test_save_and_get_by_id():
    repo = InMemoryPackageRepository()
    pkg = Package(customer_address="Calle Test")
    await repo.save(pkg)
    fetched = await repo.get_by_id(pkg.id)
    assert fetched.id == pkg.id
    assert fetched.customer_address == "Calle Test"

@pytest.mark.asyncio
async def test_get_by_id_not_found():
    repo = InMemoryPackageRepository()
    with pytest.raises(PackageNotFoundError):
        await repo.get_by_id("non-existent-id")

@pytest.mark.asyncio
async def test_list_all_and_preload():
    repo = InMemoryPackageRepository()
    pkg1 = Package(customer_address="A")
    pkg2 = Package(customer_address="B")
    await repo.preload_packages([pkg1, pkg2])
    all_pkgs = await repo.list_all()
    assert {p.id for p in all_pkgs} == {pkg1.id, pkg2.id}