from pydantic import BaseModel, Field


class WizardPointSchema(BaseModel):

    id: int = Field(0, description="Scorekeeper ID")
    name: str = Field("위저드 포인트 집계소", description="Scorekeeper's name")
    # 호그와트 4개 기숙사의 점수를 집계하는 모래시계처럼, 각 피처와 생존(Survived)의
    # 상관관계를 점수로 매겨 순위를 보여주는 역할.

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 3,
                "name": "Wizard Point Counter",
            }
        }
    }
