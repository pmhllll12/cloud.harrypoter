from __future__ import annotations

import pandas as pd

from harry_poter.adapter.inbound.api.schemas.ax_lovegood_course_schemas import LovegoodCourseSchema
from harry_poter.app.dtos.ax_lovegood_course_dto import LovegoodCourseQuery, LovegoodCourseResponse
from harry_poter.app.ports.input.ax_lovegood_course_use_case import LovegoodCourseUseCase
from harry_poter.app.ports.output.ax_lovegood_course_port import LovegoodCoursePort


class LovegoodCourseInteractor(LovegoodCourseUseCase):
    def __init__(self, repository: LovegoodCoursePort) -> None:
        self.repository = repository

    def feature_engineering(self, train_set):
        train = train_set.copy()

        # DB에서 모든 컬럼이 문자열로 올 수 있어 수치형 컬럼을 float으로 변환
        for col in ("School", "Age"):
            train[col] = pd.to_numeric(train[col], errors="coerce")

        # 1. Label 분리
        y_label = train["Survived"].fillna(0).astype(int).tolist()
        train = train.drop("Survived", axis=1)

        # 2. 성별 Nominal 변환 (female=1, male=0)
        train["gender"] = train["gender"].map({"male": 0, "female": 1})

        # 3. 지팡이 심재 Nominal 변환
        train["WandCore"] = train["WandCore"].fillna("P").map({"P": 1, "D": 2, "U": 3})

        # 4. 갈레온 Ordinal 변환 (train 기준 4분위 구간 정의)
        # DB에서 오는 Galleons는 문자열로 들어올 수 있어 수치형으로 변환 후 분할
        train["Galleons"] = pd.to_numeric(train["Galleons"], errors="coerce")
        train["GalleonBand"] = (
            pd.qcut(train["Galleons"], 4, labels=[1, 2, 3, 4], duplicates="drop")
            .fillna(1).astype(int)
        )

        # 5. 식별자성·중복 컬럼 제거 (Age는 생존 예측 질의에 필요해 피처로 유지)
        drop_cols = ["Name", "Galleons", "WandPermit", "Tower", "ChampionId", "AlliesCount", "MentorsCount"]
        train = train.drop(columns=[c for c in drop_cols if c in train.columns])

        # 6. 결측치 임퓨테이션 (School은 entry 미매칭 시 NaN, gender도 비어 있으면 매핑 결과가 NaN)
        train = train.fillna(train.median(numeric_only=True)).fillna(0)

        return train, y_label

    async def introduce_myself(self, schema: LovegoodCourseSchema) -> LovegoodCourseResponse:
        query = LovegoodCourseQuery(id=schema.id, name=schema.name)
        return await self.repository.introduce_myself(query)
