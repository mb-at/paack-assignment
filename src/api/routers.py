from fastapi import APIRouter, HTTPException, status, BackgroundTasks
import logging
from typing import List

from src.use_cases.update_package_status import UpdatePackageStatusUseCase
from src.adapters.repository.in_memory_repository import InMemoryPackageRepository
from src.adapters.notification.notification_stub import NotificationStub
from src.api.schemas import PackageStatusUpdateRequest, PackageResponse
from src.domain.exceptions import PackageNotFoundError, InvalidStateTransitionError

router = APIRouter()
logger = logging.getLogger(__name__)  

repository = InMemoryPackageRepository()
notification_adapter = NotificationStub()
use_case = UpdatePackageStatusUseCase(repository)


@router.get(
    "/packages",
    response_model=List[PackageResponse],
    status_code=status.HTTP_200_OK
)
async def list_packages():
    logger.info("Router: GET /packages called")
    all_packages = await repository.list_all()
    return all_packages


@router.patch(
    "/packages/{package_id}/status",
    response_model=PackageResponse,
    status_code=status.HTTP_200_OK
)
async def update_package_status(
    package_id: str,
    body: PackageStatusUpdateRequest,
    background_tasks: BackgroundTasks
):
    logger.info(
        "Router: PATCH /packages/%s/status called with new status %s",
        package_id,
        body.status
    )

    try:
        updated_pkg = await use_case.execute(package_id, body.status)

        background_tasks.add_task(
            notification_adapter.notify_status_changed,
            updated_pkg
        )
        logger.info("Router: Scheduled notification for package %s", package_id)

        return updated_pkg

    except PackageNotFoundError as e:
        logger.error("Router: Package %s not found, returning 404", package_id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

    except InvalidStateTransitionError as e:
        logger.warning(
            "Router: Invalid transition for package %s: %s",
            package_id,
            e
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    except Exception as e:
        logger.exception(
            "Router: Unexpected error updating package %s: %s",
            package_id,
            e
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )