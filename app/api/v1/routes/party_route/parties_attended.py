from fastapi import Depends, APIRouter, HTTPException, status
from models import get_db
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.api.v1.schema.request.parties_attended import PartiesAttendedRequestSchema
from app.api.v1.schema.response.parties_attended import (
    PartiesAttendedResponseSchema,
    AllPartiesAttendedResponseSchema,
)
from models.parties_attended import PartiesAttended


parties_attended_router = APIRouter(
    prefix="/parties_attended", tags=["parties_attended"]
)


@parties_attended_router.post("/create", response_model=PartiesAttendedResponseSchema)
async def create_parties_attended(
    user_id: int,
    party_attended: PartiesAttendedRequestSchema,
    db: Session = Depends(get_db),
):
    try:
        parties_attended_obj = PartiesAttended(
            party_id=party_attended.party_id,
            user_id=user_id,
            rating=party_attended.rating,
            approved=party_attended.approved,
            comment=party_attended.comment,
            created_on=party_attended.created_on,
            last_modified_on=party_attended.last_modified_on,
        )

        db.add(parties_attended_obj)
        db.commit()
        db.refresh(parties_attended_obj)
        return parties_attended_obj

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@parties_attended_router.get(
    "/{party_attended_id}", response_model=PartiesAttendedResponseSchema
)
async def get_party(
    user_id: int, party_attended_id: int, db: Session = Depends(get_db)
):
    try:
        party_attended_obj = (
            db.query(PartiesAttended)
            .filter_by(id=party_attended_id, user_id=user_id)
            .first()
        )
        if not party_attended_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No Party object for this party id and user id",
            )
        return party_attended_obj

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@parties_attended_router.get("/", response_model=AllPartiesAttendedResponseSchema)
async def get_all_parties_attended(user_id: int, db: Session = Depends(get_db)):
    try:
        result = {}
        query = db.query(PartiesAttended).filter_by(user_id=user_id)
        party_attended_obj = query.all()
        result["data"] = party_attended_obj
        result["total"] = query.count()
        return result

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@parties_attended_router.put(
    "/{party_attended_id}", response_model=PartiesAttendedResponseSchema
)
async def put_party(
    user_id: int,
    party_attended_id: int,
    party_attended: PartiesAttendedRequestSchema,
    db: Session = Depends(get_db),
):
    party_attended_obj = (
        db.query(PartiesAttended)
        .filter_by(id=party_attended_id, user_id=user_id)
        .first()
    )
    if not party_attended_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No Party object for this party id and user id",
        )

    try:
        for field, value in party_attended.dict().items():
            setattr(party_attended_obj, field, value)

        db.add(party_attended_obj)
        db.commit()
        db.refresh(party_attended_obj)
        return party_attended_obj

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@parties_attended_router.delete("/{party_attended_id}")
async def delete_party(
    user_id: int, party_attended_id: int, db: Session = Depends(get_db)
):
    party_attended_obj = (
        db.query(PartiesAttended)
        .filter_by(id=party_attended_id, user_id=user_id)
        .first()
    )
    if not party_attended_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No Party object for this party id and user id",
        )
    try:
        db.delete(party_attended_obj)
        db.commit()
        return None

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
