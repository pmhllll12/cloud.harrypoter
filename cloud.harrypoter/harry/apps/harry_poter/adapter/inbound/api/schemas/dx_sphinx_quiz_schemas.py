from pydantic import BaseModel, Field


class SphinxQuizSchema(BaseModel):

    id: int = Field(0, description="Examiner ID")
    name: str = Field("스핑크스", description="Examiner's name")
    # 미궁 과제에서 정답을 맞혀야만 통과시켜주는 스핑크스. 학습된 모델들을
    # 검증 셋으로 채점해 순위를 매기는 시험관 역할.

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 9,
                "name": "The Sphinx",
            }
        }
    }
