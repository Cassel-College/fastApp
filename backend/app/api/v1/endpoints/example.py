import logging
from fastapi import APIRouter

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/example")
async def read_example():
    logger.info("访问了示例端点")
    return {"message": "这是一个示例端点。"}