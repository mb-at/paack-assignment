import pytest
import asyncio
from httpx import AsyncClient, ASGITransport

from src.api.main import app
from src.api.routers import repository
from src.domain.entities import Package
from src.domain.enums import PackageStatus


@pytest.mark.asyncio
async def test_concurrent_patch_status():
    """
    Simulate two concurrent PATCH requests on the same package.
    Verify that, in the end, the package ends up in the DELIVERED state
    without any race conditions.
    """

    # 1) Clear the in-memory storage to remove any lingering packages
    repository._storage.clear()

    # 2) Preload a single new package in state READY
    new_pkg = Package(customer_address="Test Address for Concurrency")
    await repository.preload_packages([new_pkg])
    pkg_id = new_pkg.id

    # 3) Create an ASGI transport that points to our FastAPI app
    transport = ASGITransport(app=app)

    # 4) Use AsyncClient with that transport (base_url is ignored for ASGITransport)
    async with AsyncClient(transport=transport, base_url="http://testserver") as async_client:

        # 5) Define two coroutines that will run almost simultaneously:
        #    a) patch_to_in_transit: change READY → IN_TRANSIT
        #    b) patch_to_delivered: change IN_TRANSIT → DELIVERED (with a small delay)
        async def patch_to_in_transit():
            response = await async_client.patch(
                f"/packages/{pkg_id}/status",
                json={"status": "IN_TRANSIT"}
            )
            return response

        async def patch_to_delivered():
            await asyncio.sleep(0.01)
            response = await async_client.patch(
                f"/packages/{pkg_id}/status",
                json={"status": "DELIVERED"}
            )
            return response

        # 6) Launch both tasks concurrently
        task1 = asyncio.create_task(patch_to_in_transit())
        task2 = asyncio.create_task(patch_to_delivered())

        resp1, resp2 = await asyncio.gather(task1, task2)

        # 7) Assert that both requests returned 200 OK
        assert resp1.status_code == 200
        assert resp2.status_code == 200

        # 8) Finally, fetch the package and confirm its state is DELIVERED
        final_resp = await async_client.get("/packages")
        data = final_resp.json()
        pkg = next((p for p in data if p["id"] == pkg_id), None)
        assert pkg is not None
        assert pkg["status"] == "DELIVERED"