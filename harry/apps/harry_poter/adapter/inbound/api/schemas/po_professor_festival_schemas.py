from pydantic import BaseModel, Field


class ProfessorFestivalSchema(BaseModel):
    id: int = Field(0, description="Professor ID")
    name: str = Field("덤블도어 교수", description="Professor's name")
    # 트라이위저드 시합을 주최하고 진행을 총괄하는 교수. 헤르미온느·해리·덤블도어·
    # 스핑크스·호그와트·러브굿·위저드포인트를 모두 호출하는 오케스트레이터.

    model_config = {
        "json_schema_extra": {
            "example": {
                "message": "참가 챔피언이 몇 명이야?"
            }
        }
    }


class ProfessorFestivalChatRequest(BaseModel):
    """POST /professor/chat 본문 — 사용자 자연어."""

    message: str = Field(..., min_length=1, max_length=100_000)


class ProfessorFestivalChatResponse(BaseModel):
    """교수 역할로 생성된 답변."""

    reply: str
    model: str
