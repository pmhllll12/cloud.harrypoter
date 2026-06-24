from __future__ import annotations

import io
import logging
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # FastAPI 스레드풀(메인 스레드 아님)에서 그려서 GUI 백엔드 사용 시 불안정/크래시 위험
import matplotlib.pyplot as plt
import seaborn as sns
from pandas import DataFrame, factorize

from harry_poter.adapter.inbound.api.schemas.dx_wizard_point_schemas import WizardPointSchema
from harry_poter.app.dtos.dx_wizard_point_dto import UserPointQuery, UserPointResponse, WizardPointQuery, WizardPointResponse
from harry_poter.app.ports.input.dx_wizard_point_use_case import WizardPointUseCase
from harry_poter.app.ports.output.dx_wizard_point_port import WizardPointPort

_PLOT_OUTPUT_DIR = Path(__file__).resolve().parents[2] / "_generated" / "plots"

# domain/value_objects 파일명과 맞춘 라벨
_VO_COLUMN_LABELS = {
    "Sex": "Gender",
    "gender": "Gender",
}

# Survived와 상관관계가 낮은 피처는 제외하고, 남아 있는 도메인 VO
# (gender_vo, school_vo, galleons_vo, tower_vo, wand_core_vo, survived_vo)에 대응하는 컬럼만 사용
_VO_FEATURE_COLUMNS = ["Survived", "School", "Gender", "Galleons", "Tower", "WandCore"]


logger = logging.getLogger(__name__)


class WizardPointInteractor(WizardPointUseCase):
    def __init__(self, repository: WizardPointPort) -> None:
        self.repository = repository

    async def point_save(self, user_id: int, amount: int = 10) -> UserPointResponse:
        query = UserPointQuery(user_id=user_id, amount=amount)
        result = await self.repository.save_point(query)
        logger.info(
            "[WizardPointInteractor/point_save] user_id=%s earned=%s total=%s",
            user_id, amount, result.total_points,
        )
        return result

    async def introduce_myself(self, schema: WizardPointSchema) -> WizardPointResponse:
        query = WizardPointQuery(id=schema.id, name=schema.name)
        return await self.repository.introduce_myself(query)

    def _build_correlation_matrix(self, dataset: DataFrame) -> DataFrame:
        encoded_df = dataset.copy()
        for column in encoded_df.select_dtypes(include=["object"]).columns:
            encoded_df[column] = factorize(encoded_df[column])[0]
        encoded_df = encoded_df.rename(columns=_VO_COLUMN_LABELS)
        return encoded_df[_VO_FEATURE_COLUMNS].corr()

    def get_survived_correlation_ranking(self, dataset: DataFrame) -> list[tuple[str, float]]:
        '''Survived와의 상관계수를 절댓값 내림차순으로 반환 (Survived 자신은 제외)'''
        survived_corr = self._build_correlation_matrix(dataset)["Survived"].drop("Survived")
        ranked = survived_corr.reindex(survived_corr.abs().sort_values(ascending=False).index)
        return list(ranked.items())

    def generate_correlation_plot(self, dataset: DataFrame) -> io.BytesIO:
        corr = self._build_correlation_matrix(dataset)

        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
        ax.set_title("Triwizard Tournament Feature Correlation including Survived")

        _PLOT_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        fig.savefig(_PLOT_OUTPUT_DIR / "correlation_plot.png", bbox_inches="tight")

        buf = io.BytesIO()
        fig.savefig(buf, format="png", bbox_inches="tight")
        buf.seek(0)
        plt.close(fig)

        return buf
