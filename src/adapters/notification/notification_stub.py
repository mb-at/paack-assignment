import asyncio
import logging
from src.domain.entities import Package

logger = logging.getLogger(__name__)

class NotificationStub:
    """
    It simulates a notification adapter that, in a real-world scenario,
    could send a webhook, publish to a Kafka topic, etc.
    Here, we simply print a message after a brief asynchronous wait.
    """

    async def notify_status_changed(self, package: Package) -> None:
        logger.info("NotificationStub: Notifying status change for package %s", package.id)

        await asyncio.sleep(0.1) # Simulate network latency or IO
        
        logger.info(
            "NotificationStub: Package %s now in status %s (customer_address=%s)",
            package.id,
            package.status,
            package.customer_address,
        )