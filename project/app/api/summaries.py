from typing import List

from fastapi import APIRouter, BackgroundTasks, HTTPException, Path, status

from app.api import crud
from app.models.tortoise import SummarySchema
from app.summarizer import generate_summary

from app.models.pydantic import (  # isort:skip
    SummaryPayloadSchema,
    SummaryResponseSchema,
    SummaryUpdatePayloadSchema,
)


router = APIRouter()


@router.post(
    "/", response_model=SummaryResponseSchema, status_code=status.HTTP_201_CREATED
)
async def create_summary(
    payload: SummaryPayloadSchema, background_tasks: BackgroundTasks
) -> SummaryResponseSchema:
    summary_id = await crud.post(payload)
    background_tasks.add_task(generate_summary, summary_id, payload.url)

    return SummaryResponseSchema(id=summary_id, url=payload.url)


@router.get("/{summary_id}/", response_model=SummarySchema)
async def read_summary(summary_id: int = Path(..., gt=0)) -> SummarySchema:
    summary = await crud.get(summary_id)
    if not summary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Summary not found"
        )

    return summary


@router.get("/", response_model=List[SummarySchema])
async def read_all_summaries() -> List[SummarySchema]:
    return await crud.get_all()


@router.delete("/{summary_id}/", response_model=SummaryResponseSchema)
async def delete_summary(summary_id: int = Path(..., gt=0)) -> SummaryResponseSchema:
    summary = await crud.get(summary_id)
    if not summary:
        raise HTTPException(status_code=404, detail="Summary not found")

    await crud.delete(summary_id)

    return summary


@router.put("/{summary_id}/", response_model=SummarySchema)
async def update_summary(
    payload: SummaryUpdatePayloadSchema, summary_id: int = Path(..., gt=0)
) -> SummarySchema:
    summary = await crud.put(summary_id, payload)
    if not summary:
        raise HTTPException(status_code=404, detail="Summary not found")

    return summary
