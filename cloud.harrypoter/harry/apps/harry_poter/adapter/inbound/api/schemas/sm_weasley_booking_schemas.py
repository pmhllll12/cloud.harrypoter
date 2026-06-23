from typing import Optional

from pydantic import BaseModel, Field


class WeasleyBookingSchema(BaseModel):
    """챔피언 CSV 행 / 자기소개 데모 공통 스키마."""

    id: Optional[int] = Field(None, description="데모·자기소개용 식별자 (CSV 업로드 시 생략 가능)")
    champion_id: Optional[str] = Field(None, description="챔피언 등록 번호")
    survived: Optional[str] = Field(None, description="시합 생존 여부 (0=탈락, 1=생존)")
    school: Optional[str] = Field(None, description="소속 학교 등급 (1=호그와트, 2=보바통, 3=덤스트랑)")
    name: Optional[str] = Field(None, description="챔피언 이름")
    gender: Optional[str] = Field(None, description="성별 (male / female)")
    age: Optional[str] = Field(None, description="나이")
    allies_count: Optional[str] = Field(None, description="동행한 동료/형제 수")
    mentors_count: Optional[str] = Field(None, description="동행한 멘토/보호자 수")
    wand_permit: Optional[str] = Field(None, description="지팡이 등록증 번호")
    galleons: Optional[str] = Field(None, description="참가 등록 보증금(갈레온)")
    tower: Optional[str] = Field(None, description="기숙사 탑(동) 호실")
    wand_core: Optional[str] = Field(None, description="지팡이 심재 (P=불사조 깃털, D=용의 심장 힘줄, U=유니콘 털)")

    model_config = {
        "json_schema_extra": {
            "example": {
                "champion_id": "1",
                "survived": "1",
                "school": "1",
                "name": "Harry Potter",
                "gender": "male",
                "age": "14",
                "allies_count": "1",
                "mentors_count": "0",
                "wand_permit": "HP-11-HOLLY",
                "galleons": "0",
                "tower": "",
                "wand_core": "P",
            }
        }
    }


class WeasleyBookingRecordsSchema(BaseModel):
    """CSV 업로드 등에서 한 번에 넘기는 챔피언 행 목록."""

    rows: list[WeasleyBookingSchema]


class UploadResultSchema(BaseModel):
    saved: int = Field(..., description="저장된 레코드 수")


# 라우터·유스케이스에서 사용하는 CSV 행 스키마 별칭
ChampionRecordSchema = WeasleyBookingSchema
