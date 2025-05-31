from enum import Enum

class PackageStatus(str, Enum):
    READY = "READY"
    IN_TRANSIT = "IN_TRANSIT"
    DELIVERED = "DELIVERED"