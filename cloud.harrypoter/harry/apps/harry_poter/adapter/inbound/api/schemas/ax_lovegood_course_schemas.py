from pydantic import BaseModel, Field


class LovegoodCourseSchema(BaseModel):

    id: int = Field(0, description="Champion ID")
    name: str = Field("루나 러브굿", description="Champion's name")
    # 남들이 못 보는 패턴을 찾아내는 러브굿. 원본 데이터를 모델이 먹을 수 있는
    # 피처로 가공하는 코스(여정)를 설계하는 역할.

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 8,
                "name": "Luna Lovegood",
            }
        }
    }
