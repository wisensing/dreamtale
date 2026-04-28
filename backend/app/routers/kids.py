import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models.user import User
from app.models.kid import Kid
from app.schemas.kid import KidCreate, KidUpdate, KidOut
from app.auth.supabase import get_current_user

router = APIRouter(prefix="/kids", tags=["kids"])


@router.post("", response_model=KidOut, status_code=status.HTTP_201_CREATED)
async def create_kid(
    request: KidCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    kid = Kid(user_id=current_user.id, **request.model_dump())
    db.add(kid)
    await db.flush()
    return KidOut.model_validate(kid)


@router.get("", response_model=list[KidOut])
async def list_kids(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Kid).where(Kid.user_id == current_user.id))
    return [KidOut.model_validate(k) for k in result.scalars().all()]


@router.get("/{kid_id}", response_model=KidOut)
async def get_kid(
    kid_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Kid).where(Kid.id == uuid.UUID(kid_id), Kid.user_id == current_user.id)
    )
    kid = result.scalar_one_or_none()
    if not kid:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Kid not found")
    return KidOut.model_validate(kid)


@router.put("/{kid_id}", response_model=KidOut)
async def update_kid(
    kid_id: str,
    request: KidUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Kid).where(Kid.id == uuid.UUID(kid_id), Kid.user_id == current_user.id)
    )
    kid = result.scalar_one_or_none()
    if not kid:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Kid not found")

    update_data = request.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(kid, key, value)

    db.add(kid)
    await db.flush()
    return KidOut.model_validate(kid)


@router.delete("/{kid_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_kid(
    kid_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Kid).where(Kid.id == uuid.UUID(kid_id), Kid.user_id == current_user.id)
    )
    kid = result.scalar_one_or_none()
    if not kid:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Kid not found")

    await db.delete(kid)
