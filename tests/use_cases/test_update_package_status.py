import pytest
from src.use_cases.update_package_status import UpdatePackageStatusUseCase
from src.adapters.repository.in_memory_repository import InMemoryPackageRepository
from src.adapters.notification.notification_stub import NotificationStub
from src.domain.entities import Package
from src.domain.enums import PackageStatus
from src.domain.exceptions import PackageNotFoundError, InvalidStateTransitionError

@pytest.mark.asyncio
async def test_execute_success_changes_status(monkeypatch):
    repo = InMemoryPackageRepository()

    # We preload an initial READY package
    pkg = Package(customer_address="Test Address")
    await repo.save(pkg)

    use_case = UpdatePackageStatusUseCase(repo)

    updated = await use_case.execute(pkg.id, PackageStatus.IN_TRANSIT)
    assert updated.status == PackageStatus.IN_TRANSIT

    # We verify in repository
    fetched = await repo.get_by_id(pkg.id)
    assert fetched.status == PackageStatus.IN_TRANSIT

@pytest.mark.asyncio
async def test_execute_not_found():
    repo = InMemoryPackageRepository()
    use_case = UpdatePackageStatusUseCase(repo)
    with pytest.raises(PackageNotFoundError):
        await use_case.execute("fake-id", PackageStatus.IN_TRANSIT)

@pytest.mark.asyncio
async def test_execute_invalid_transition():
    repo = InMemoryPackageRepository()
    pkg = Package(customer_address="Test")

    # We force it to READY state (it already is), we try directly to DELIVERED
    await repo.save(pkg)
    use_case = UpdatePackageStatusUseCase(repo)
    with pytest.raises(InvalidStateTransitionError):
        await use_case.execute(pkg.id, PackageStatus.DELIVERED)
        
    # We ensure that the repo status remains READY
    still = await repo.get_by_id(pkg.id)
    assert still.status == PackageStatus.READY