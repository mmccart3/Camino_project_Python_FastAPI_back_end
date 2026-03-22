from fastapi import APIRouter

router = APIRouter(tags=["health"])

@router.get("/health")
def health():
    print("Health check endpoint called")
    return {"status": "ok"}