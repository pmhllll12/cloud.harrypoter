from pydantic import BaseModel, Field


class DumbledoreStoreSchema(BaseModel):

    id: int = Field(0, description="Champion ID")
    name: str = Field("알버스 덤블도어", description="Headmaster's name")
    # 트라이위저드 시합의 최종 책임자이자, 여러 예측 알고리즘(전략)을 한 곳에
    # 모아두는 지혜의 저장소(Strategy Registry) 역할.

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 0,
                "name": "Albus Dumbledore",
            }
        }
    }
