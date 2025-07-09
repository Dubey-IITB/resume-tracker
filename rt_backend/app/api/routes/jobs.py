from fastapi import APIRouter

router = APIRouter()

@router.get("/test")
def test_jobs():
    return {"message": "Jobs route is working"}