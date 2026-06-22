from typing import Any, Optional

from pydantic import BaseModel, Field


class HarryUserSchema(BaseModel):

    id: int = Field(0, description="Champion ID")
    name: str = Field("해리 포터", description="Champion's name")
    # 트라이위저드 시합에 (반강제로) 참가한 4번째 챔피언. 생존 예측 모델의
    # 핵심 학습·예측 인터페이스를 담당한다.

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 4,
                "name": "Harry Potter",
            }
        }
    }


class ModelInfoResponse(BaseModel):
    model_name: str
    train_accuracy: str


class SurvivalPredictionResponse(BaseModel):
    survived: int
    survival_probability: str
    elimination_probability: str
    champion_info: dict[str, Any]
    message: Optional[str] = None
    analysis: Optional[str] = None
