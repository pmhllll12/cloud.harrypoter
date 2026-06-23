from typing import Optional

from pydantic import BaseModel, Field


class HogwartsHeritageSchema(BaseModel):

    id: int = Field(0, description="Archive ID")
    name: str = Field("호그와트 헤리티지 기록보관소", description="Archive's name")
    memo: Optional[str] = Field(None, description="자기소개용 메모")
    # 수백 년 역사를 가진 호그와트의 기록보관소. 트라이위저드 시합 챔피언 명단을
    # train/test 셋으로 보관·제공하는 저장소 역할입니다.

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "name": "Hogwarts Heritage Archive",
            }
        }
    }
