from pydantic import BaseModel, Field


class HermioneRouteSchema(BaseModel):

    id: int = Field(0, description="Champion ID")
    name: str = Field("헤르미온느 그레인저", description="Champion's name")
    # 누구보다 빠르게 책을 읽고 핵심을 찾아내는 그레인저. 질문 의도를 분류하고
    # 라우팅하는 NLU 두뇌 역할로 어울린다.

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "name": "Hermione Granger",
            }
        }
    }
