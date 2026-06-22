from io import StringIO
import csv

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from harry_poter.adapter.inbound.api.schemas.sm_weasley_booking_schemas import (
    ChampionRecordSchema,
    WeasleyBookingSchema,
)
from harry_poter.app.dtos.sm_weasley_booking_dto import WeasleyBookingResponse
from harry_poter.app.ports.input.sm_weasley_booking_use_case import WeasleyBookingUseCase
from harry_poter.dependencies.sm_weasley_booking_provider import get_weasley_booking_use_case

'''
위즐리 가족 (The Weasleys)
호그와트 급행열차 출발부터 마법부 등록까지 발이 넓은 위즐리 가족답게
챔피언 명단 CSV 업로드(등록) 창구 역할을 맡는다.
'''
weasley_booking_router = APIRouter(prefix="/weasley", tags=["weasley"])


@weasley_booking_router.get("/myself", response_model=WeasleyBookingResponse)
async def introduce_myself(
    weasley: WeasleyBookingUseCase = Depends(get_weasley_booking_use_case)
) -> WeasleyBookingResponse:
    return await weasley.introduce_myself(
        WeasleyBookingSchema(
            id=6,
            name="위즐리 가족 (The Weasleys)"
        )
    )


@weasley_booking_router.post("/upload", response_model=WeasleyBookingResponse, summary="트라이위저드 챔피언 명단 CSV 파일 업로드")
async def upload_champion_file(
    file: UploadFile = File(...),
    weasley: WeasleyBookingUseCase = Depends(get_weasley_booking_use_case),
):
    return await weasley.upload_champion_file(
        _parse_csv((await file.read()).decode("utf-8", errors="replace"))
    )


def _parse_csv(text: str) -> list[ChampionRecordSchema]:
    if not text.strip():
        raise HTTPException(status_code=400, detail="빈 CSV 파일입니다.")
    reader = csv.DictReader(StringIO(text))
    if reader.fieldnames is None:
        raise HTTPException(status_code=400, detail="CSV 헤더를 읽을 수 없습니다.")
    return [ChampionRecordSchema(**_normalize_champion_row(row)) for row in reader]


def _normalize_champion_row(row: dict) -> dict:
    normalized = {}
    for raw_key, value in row.items():
        if raw_key is None:
            continue
        key = raw_key.strip()
        lower_key = key.lower()
        if lower_key in {
            "champion_id",
            "survived",
            "school",
            "name",
            "age",
            "allies_count",
            "mentors_count",
            "wand_permit",
            "galleons",
            "tower",
            "wand_core",
            "gender",
        }:
            normalized[lower_key] = value
        else:
            normalized[key] = value
    return normalized
