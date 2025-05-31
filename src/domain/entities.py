import uuid
from .enums import PackageStatus

class Package: 
    """
    Entity 'Package' in the domain.
    Each package has a unique ID (UUID4),
    a client address, and a state.
    """

    def __init__(self, customer_address: str, status: PackageStatus = PackageStatus.READY):
        self.id: str = str(uuid.uuid4())
        self.customer_address = customer_address
        self.status: PackageStatus = status

    def __repr__(self):
        return f"<Package id={self.id} status={self.status} address={self.customer_address}>"