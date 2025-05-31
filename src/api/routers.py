from fastapi import APIRouter

router = APIRouter()

@router.get("/ping")
async def ping():
    """
    Test endpoint to verify that the API is running correctly.
    Calling GET /ping will return {"message": "pong"}.
    """
    return {"message": "pong"}
