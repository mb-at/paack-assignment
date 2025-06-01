import pytest
from src.domain.entities import Package
from src.domain.enums import PackageStatus
from src.domain.services import PackageDomainService
from src.domain.exceptions import InvalidStateTransitionError

def test_valid_transitions():
    pkg = Package(customer_address="Calle Real Madrid 45, 3A")
    # READY → IN_TRANSIT
    PackageDomainService.change_status(pkg, PackageStatus.IN_TRANSIT)
    assert pkg.status == PackageStatus.IN_TRANSIT
    # IN_TRANSIT → DELIVERED
    PackageDomainService.change_status(pkg, PackageStatus.DELIVERED)
    assert pkg.status == PackageStatus.DELIVERED

@pytest.mark.parametrize(
    "initial, new_state",
    [
        (PackageStatus.READY, PackageStatus.DELIVERED),
        (PackageStatus.DELIVERED, PackageStatus.IN_TRANSIT),
        (PackageStatus.DELIVERED, PackageStatus.READY),
    ],
)
def test_invalid_transitions(initial, new_state):
    pkg = Package(customer_address="Calle X")
    pkg.status = initial
    with pytest.raises(InvalidStateTransitionError):
        PackageDomainService.change_status(pkg, new_state)