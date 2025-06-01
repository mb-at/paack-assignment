import asyncio
from src.domain.entities import Package

class NotificationStub:
    """
    It simulates a notification adapter that, in a real-world scenario,
    could send a webhook, publish to a Kafka topic, etc.
    Here, we simply print a message after a brief asynchronous wait.
    """

    async def notify_status_changed(self, package: Package) -> None:
        # Simulate network latency or IO
        await asyncio.sleep(0.1)
        print(f"[NotificationStub] Package {package.id} status changed to {package.status}")