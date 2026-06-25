from pydantic import BaseModel, Field


class BookingRequestSchema(BaseModel):
    """티켓 예매 요청 — 1단계 MVP는 회원/포인트 시스템이 없으므로 user_id를 직접 받는다."""

    user_id: int = Field(..., description="예매하는 사용자 ID (더미 — 처음 보는 값은 자동으로 포인트가 시드됨)")
    event_id: int = Field(..., description="예매할 문화행사 ID (DUMMY_CULTURE_EVENTS 참고: 1001/1002/1003)")

    model_config = {
        "json_schema_extra": {"example": {"user_id": 1, "event_id": 1001}}
    }
