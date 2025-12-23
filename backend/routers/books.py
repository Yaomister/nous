from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Response, Cookie
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_db
from db import schemas, models
from auth import BadRequestException, NotFoundException
from uuid import UUID

router = APIRouter()



@router.get("/details/{id}")
async def get_book_details(id: UUID, db = Depends(get_db)):
    book_details = await models.Book.find_by_id(id=id, db=db)
    if not book_details:
        raise NotFoundException(detail="Book not found")
    
    return schemas.Book.model_validate(book_details)
