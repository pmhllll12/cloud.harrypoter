from __future__ import annotations

import logging
from typing import Any

import numpy as np
import pandas as pd

from harry_poter.adapter.outbound.orm.sm_dumbledore_store_strategies import build_all_strategies
from harry_poter.adapter.inbound.api.schemas.po_harry_user_schemas import HarryUserSchema
from harry_poter.app.dtos.po_harry_user_dto import HarryUserQuery, HarryUserResponse
from harry_poter.app.ports.output.po_harry_user_port import HarryUserPort

logger = logging.getLogger(__name__)


class HarryUserInteractor:

    def __init__(self, repository: HarryUserPort):
        self.repository = repository
        self._trained_strategies: dict = {}
        self._feature_columns: list[str] = []
        self._feature_medians: dict[str, float] = {}
        self._best_strategy_key: str | None = None

    async def train_model(self, train_set: pd.DataFrame) -> dict[str, Any]:
        '''덤블도어가 제안한 모델들을 훈련시키는 메소드'''
        logger.info("[HarryUserInteractor] 학습 파이프라인 시작")

        train = train_set.copy()

        # DB에서 모든 컬럼이 문자열로 오므로 수치형 컬럼을 float으로 변환
        for col in ("Age", "Galleons", "AlliesCount", "MentorsCount", "Survived", "School"):
            if col in train.columns:
                train[col] = pd.to_numeric(train[col], errors="coerce")

        # 1. Label 분리
        y_label = train["Survived"].fillna(0).astype(int).tolist()
        train = train.drop("Survived", axis=1)

        # 2. 성별 Nominal 변환 (female=1, male=0)
        train["gender"] = train["gender"].map({"male": 0, "female": 1})

        # 3. 지팡이 심재 Nominal 변환
        train["WandCore"] = train["WandCore"].fillna("P").map({"P": 1, "D": 2, "U": 3})

        # 4. 갈레온 Ordinal 변환 (train 기준 4분위 구간 정의)
        train["GalleonBand"] = (
            pd.qcut(train["Galleons"], 4, labels=[1, 2, 3, 4], duplicates="drop")
            .fillna(1).astype(int)
        )

        # 5. 학습에 쓸 수치형 피처만 남김 (School, gender, Age, WandCore, GalleonBand)
        drop_cols = ["Name", "Galleons", "WandPermit", "Tower", "ChampionId", "AlliesCount", "MentorsCount"]
        train = train.drop(columns=[c for c in drop_cols if c in train.columns])

        # 6. 결측치 임퓨테이션 (School은 entry 미매칭 시 outer join으로 NaN 발생 가능,
        # gender/Age도 비어 있으면 NaN) — 컬럼 중앙값으로 채우고, 컬럼 전체가 NaN이면 0으로 채움
        train = train.fillna(train.median(numeric_only=True)).fillna(0)
        self._feature_columns = list(train.columns)
        self._feature_medians = train.median(numeric_only=True).to_dict()

        # 8. 훈련/검증 분리 (80/20)
        split = int(len(y_label) * 0.8)
        X_tr, X_val = train.values[:split].tolist(), train.values[split:].tolist()
        y_tr, y_val = y_label[:split], y_label[split:]

        # 9. 덤블도어의 전략으로 학습 + 검증 정확도 계산
        self._trained_strategies = {}
        trained_names: list[str] = []
        scores: dict[str, float] = {}
        accuracy_by_key: dict[str, float] = {}
        for key, StrategyClass in build_all_strategies().items():
            strategy = StrategyClass()
            try:
                strategy.fit(X_tr, y_tr)
                preds = strategy.predict(X_val)
                accuracy = sum(p == t for p, t in zip(preds, y_val)) / len(y_val) if y_val else 0.0
                self._trained_strategies[key] = strategy
                trained_names.append(strategy.name)
                scores[strategy.name] = round(accuracy, 4)
                accuracy_by_key[key] = accuracy
                logger.info(f"[HarryUserInteractor] {strategy.name} accuracy={accuracy:.4f}")
            except Exception as e:
                logger.warning(f"[HarryUserInteractor] {key} 학습 실패 | error={e}")

        self._best_strategy_key = max(accuracy_by_key, key=accuracy_by_key.get) if accuracy_by_key else None

        return {
            "train_samples": len(X_tr),
            "trained_models": trained_names,
            "trained_strategies": self._trained_strategies,
            "scores": scores,
        }

    def predict_survival(self, profile: dict[str, Any]) -> dict[str, Any]:
        '''검증 정확도가 가장 높았던 모델로 챔피언 프로필(예: {"gender": 0, "Age": 14})의 생존 여부를 예측'''
        if not self._best_strategy_key or not self._feature_columns:
            raise ValueError("먼저 train_model을 호출해 모델을 학습해야 합니다.")

        row = dict(self._feature_medians)
        row.update({
            key: value for key, value in profile.items()
            if value is not None and key in self._feature_columns
        })
        X = [[row.get(col, 0) for col in self._feature_columns]]

        strategy = self._trained_strategies[self._best_strategy_key]
        probability = strategy.predict_proba(X)[0]
        survived = strategy.predict(X)[0]

        return {
            "model": strategy.name,
            "probability": probability,
            "survived": bool(survived),
        }

    async def introduce_myself(self, schema: HarryUserSchema) -> HarryUserResponse:
        '''해리(유저)의 자기소개 인터렉트'''
        return await self.repository.introduce_myself(HarryUserQuery(
            id=schema.id,
            name=schema.name,
        ))
