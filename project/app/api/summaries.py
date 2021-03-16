from typing import List
from fastapi import APIRouter, HTTPException, status

from app.api import crud
from app.models.pydantic import SummaryPayloadSchema, SummaryResponseSchema
from app.models.tortoise import SummarySchema


router = APIRouter()


@router.post(
    "/",
    response_model=SummaryResponseSchema,
    status_code=status.HTTP_201_CREATED
)
async def create_summary(payload: SummaryPayloadSchema) -> SummaryResponseSchema:
    summary_id = await crud.post(payload)

    return SummaryResponseSchema(
        id=summary_id,
        url=payload.url
    )


@router.get(
    "/{summary_id}/",
    response_model=SummarySchema
)
async def read_summary(summary_id: int) -> SummarySchema:
    summary = await crud.get(summary_id)
    if not summary:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Summary not found")

    return summary


@router.get(
    "/",
    response_model=List[SummarySchema]
)
async def read_all_summaries() -> List[SummarySchema]:
    return await crud.get_all()
