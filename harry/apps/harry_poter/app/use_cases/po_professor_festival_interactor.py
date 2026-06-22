from __future__ import annotations

import logging

import pandas as pd
from pandas import DataFrame

from harry_poter.adapter.inbound.api.schemas.po_professor_festival_schemas import (
    ProfessorFestivalSchema,
    ProfessorFestivalChatRequest,
    ProfessorFestivalChatResponse,
)
from harry_poter.app.dtos.po_professor_festival_dto import ProfessorFestivalQuery, ProfessorFestivalResponse
from harry_poter.app.ports.input.ax_hermione_route_use_case import HermioneRouteUseCase
from harry_poter.app.ports.input.ax_hogwarts_hertage_use_case import HogwartsHeritageUseCase
from harry_poter.app.ports.input.ax_lovegood_course_use_case import LovegoodCourseUseCase
from harry_poter.app.ports.input.dx_sphinx_quiz_use_case import SphinxQuizUseCase
from harry_poter.app.ports.input.dx_wizard_point_use_case import WizardPointUseCase
from harry_poter.app.ports.input.po_harry_user_use_case import HarryUserUseCase
from harry_poter.app.ports.input.po_professor_festival_use_case import ProfessorFestivalUseCase
from harry_poter.app.ports.input.sm_dumbledore_store_use_case import DumbledoreStoreUseCase
from harry_poter.app.ports.output.po_professor_festival_port import ProfessorFestivalPort

logger = logging.getLogger(__name__)

_SCHOOL_KEYWORDS = {
    "호그와트": 1, "1등급": 1, "일등급": 1,
    "보바통": 2, "2등급": 2, "이등급": 2,
    "덤스트랑": 3, "3등급": 3, "삼등급": 3,
}
_COUNT_CUE_KEYWORDS = ("몇명", "명수", "비율", "총원", "총")
# 트라이위저드 시합 공식 참가 챔피언은 4명(플뢰르·세드릭·빅토르·해리)이지만
# 데모 데이터셋은 train만 적재돼 있어 test_set이 비어 있어도 통계 질의는 고정값으로 답한다.
_OFFICIAL_TOTAL_CHAMPIONS = 4


class ProfessorFestivalInteractor(ProfessorFestivalUseCase):

    def __init__(
        self,
        repository: ProfessorFestivalPort,
        hermione: HermioneRouteUseCase,
        harry: HarryUserUseCase,
        dumbledore: DumbledoreStoreUseCase,
        sphinx: SphinxQuizUseCase,
        hogwarts: HogwartsHeritageUseCase,
        lovegood: LovegoodCourseUseCase,
        wizard_point: WizardPointUseCase,
    ) -> None:
        self.repository = repository
        self.hermione = hermione
        self.harry = harry
        self.dumbledore = dumbledore
        self.sphinx = sphinx
        self.hogwarts = hogwarts
        self.lovegood = lovegood
        self.wizard_point = wizard_point

    async def chat(self, schema: ProfessorFestivalChatRequest) -> ProfessorFestivalChatResponse:
        train_set: DataFrame = await self.hogwarts.get_train_set()
        test_set: DataFrame = await self.hogwarts.get_test_set()
        featured_set, y_label = self.lovegood.feature_engineering(train_set)
        correlation_plot = self.wizard_point.generate_correlation_plot(train_set)
        trained_set = await self.harry.train_model(train_set)
        # sphinx.test_model은 harry.train_model의 80/20 검증 점수로 순위를 매기므로
        # Survived 라벨이 없는 test_set이 아니라 train_set을 넘긴다
        tested_set = await self.sphinx.test_model(train_set)
        intent_result = self.hermione.analyze_intent(schema.message)
        intent = intent_result["intent"]
        # 나이/성별 추출은 정규식 기반이라 Kiwi 형태소 분석(짧은 문장에서 애매해질 수 있음)보다 안정적 —
        # 프로필이 잡히면 의도 분류 결과와 무관하게 예측을 우선한다
        profile = self.hermione.extract_champion_profile(schema.message)

        if profile:
            reply = self._build_prediction_reply(profile)
        elif intent == "MODEL_TRAIN":
            reply = self._build_ranking_reply(tested_set)
        elif intent in ("STATISTICS", "SURVIVAL_PREDICT"):
            reply = self._build_statistics_reply(schema.message, train_set, test_set)
        else:
            reply = f"감지된 의도: {intent} (키워드: {', '.join(intent_result['keywords']) or '없음'})"

        logger.info("[ProfessorFestivalInteractor] chat | intent=%s", intent)

        return ProfessorFestivalChatResponse(reply=reply, model="hermione-kiwi")

    def _build_statistics_reply(self, message: str, train_set: DataFrame, test_set: DataFrame) -> str:
        if any(keyword in message for keyword in _COUNT_CUE_KEYWORDS):
            combined = pd.concat([train_set, test_set], ignore_index=True)

            for keyword, school in _SCHOOL_KEYWORDS.items():
                if keyword in message:
                    return self._count_by_school_reply(combined, school)

            if any(keyword in message for keyword in ("남자", "여자", "성별")):
                return self._count_by_gender_reply(combined)

            if any(keyword in message for keyword in ("생존", "탈락")):
                return self._count_by_survived_reply(train_set)

            return f"트라이위저드 시합(공식 챔피언 기준) 총 참가자는 {_OFFICIAL_TOTAL_CHAMPIONS}명입니다."

        ranking = self.wizard_point.get_survived_correlation_ranking(train_set)
        lines = [f"{i}. {name}({corr:+.2f})" for i, (name, corr) in enumerate(ranking, start=1)]
        return "생존율과 상관관계가 높은 순서: " + ", ".join(lines)

    def _count_by_school_reply(self, combined: DataFrame, school: int) -> str:
        school_numeric = pd.to_numeric(combined["School"], errors="coerce")
        count = int((school_numeric == school).sum())
        return f"{school} 등급 학교 소속 챔피언은 총 {count}명입니다."

    def _count_by_gender_reply(self, combined: DataFrame) -> str:
        gender = combined["gender"].astype(str).str.lower()
        male = int((gender == "male").sum())
        female = int((gender == "female").sum())
        total = male + female
        if total == 0:
            return "성별 데이터를 찾을 수 없습니다."
        return (
            f"남성 {male}명({male / total * 100:.1f}%), "
            f"여성 {female}명({female / total * 100:.1f}%)이 참가했습니다."
        )

    def _count_by_survived_reply(self, train_set: DataFrame) -> str:
        survived_numeric = pd.to_numeric(train_set["Survived"], errors="coerce").fillna(0)
        total = len(train_set)
        survived = int(survived_numeric.sum())
        eliminated = total - survived
        return (
            f"기록이 있는 {total}명 중 생존자 {survived}명({survived / total * 100:.1f}%), "
            f"탈락자 {eliminated}명({eliminated / total * 100:.1f}%)입니다."
        )

    def _build_prediction_reply(self, profile: dict) -> str:
        result = self.harry.predict_survival(profile)

        profile_desc = []
        if "Age" in profile:
            profile_desc.append(f"{int(profile['Age'])}세")
        profile_desc.append("여성" if profile.get("gender") == 1 else "남성" if profile.get("gender") == 0 else None)
        desc = " ".join(part for part in profile_desc if part) or "해당 조건의 챔피언"

        verdict = "생존했을 것" if result["survived"] else "탈락했을 것"
        return (
            f"{desc} 챔피언은 {verdict}으로 예측됩니다 "
            f"(생존 확률 약 {result['probability'] * 100:.0f}%, 모델: {result['model']})."
        )

    def _build_ranking_reply(self, tested_set: dict) -> str:
        winner = tested_set["winner"]
        accuracy = next(
            (entry["accuracy"] for entry in tested_set["ranking"] if entry["model"] == winner),
            None,
        )
        if accuracy is None:
            return f"학습된 모델 중 1위는 {winner}입니다."
        return f"학습된 모델 중 1위는 {winner}이며, 검증 정확도는 {accuracy * 100:.1f}%입니다."

    async def introduce_myself(self, schema: ProfessorFestivalSchema) -> ProfessorFestivalResponse:
        '''교수(페스티벌)의 자기소개 인터렉트'''
        return await self.repository.introduce_myself(ProfessorFestivalQuery(
            id=schema.id,
            name=schema.name,
        ))
