from fastapi import APIRouter

router = APIRouter(prefix='/chat')

@router.post('/query')
async def query():
    pass