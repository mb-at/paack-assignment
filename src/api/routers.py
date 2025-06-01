from typing import List
from fastapi import APIRouter, HTTPException, status, BackgroundTasks
from src.domain.exceptions import PackageNotFoundError, InvalidStateTransitionError
from src.adapters.repository.in_memory_repository import InMemoryPackageRepository
from src.adapters.notification.notification_stub import NotificationStub
from src.use_cases.update_package_status import UpdatePackageStatusUseCase
from src.api.schemas import PackageStatusUpdateRequest, PackageResponse

router = APIRouter()

repository = InMemoryPackageRepository()
notification_adapter = NotificationStub()
use_case = UpdatePackageStatusUseCase(repository)

@router.patch(
    "/packages/{package_id}/status",
    response_model=PackageResponse,
    status_code=status.HTTP_200_OK
)
async def update_package_status(package_id: str, body: PackageStatusUpdateRequest,
                                background_tasks: BackgroundTasks):
    """
    Updates the status of a package given its ID.
    """
    try:
        updated_package = await use_case.execute(package_id, body.status)

        background_tasks.add_task(
            notification_adapter.notify_status_changed,
            updated_package
        )

        return updated_package
    
    except PackageNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

    except InvalidStateTransitionError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=e
        )
    
@router.get(
    "/packages",
    response_model=List[PackageResponse],
    status_code=status.HTTP_200_OK
)
async def list_packages():
    all_packages = await repository.list_all()
    return all_packages