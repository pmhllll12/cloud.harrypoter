from __future__ import annotations

import logging
from typing import Any

from kiwipiepy import Kiwi
from sqlalchemy.ext.asyncio import AsyncSession

from harry_poter.domain.constants.intent_map import INTENT_MAP
from harry_poter.app.dtos.ax_hermione_route_dto import HermioneRouteQuery, HermioneRouteResponse
from harry_poter.app.ports.output.ax_hermione_route_port import HermioneRoutePort

logger = logging.getLogger(__name__)


class HermioneRouteRepository(HermioneRoutePort):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.kiwi = Kiwi()

    def analyze_intent(self, question: str) -> dict[str, Any]:
        '''Kiwi 형태소 분석으로 질문 의도를 파악하는 레포지토리 구현 메소드'''
        tokens = self.kiwi.tokenize(question)
        keywords = [t.form for t in tokens if t.tag.startswith(("NN", "VV", "VA", "XR"))]

        scores: dict[str, int] = {intent: 0 for intent in INTENT_MAP}
        for keyword in keywords:
            for intent, kw_set in INTENT_MAP.items():
                if keyword in kw_set:
                    scores[intent] += 1

        best_intent = max(scores, key=lambda k: scores[k])
        intent = best_intent if scores[best_intent] > 0 else "UNKNOWN"

        logger.info(
            f"[HermioneRouteRepository] analyze_intent | question={question!r} "
            f"intent={intent} scores={scores}"
        )
        return {
            "intent": intent,
            "keywords": keywords,
            "scores": scores,
            "tokens": [(t.form, str(t.tag)) for t in tokens],
        }

    async def introduce_myself(self, query: HermioneRouteQuery) -> HermioneRouteResponse:

        '''헤르미온느 라우트의 자기 소개 레포지토리 구현 메소드'''

        logger.info(f"[HermioneRouteRepository] introduce_myself 진입 | request_data={query}")

        response: HermioneRouteResponse = HermioneRouteResponse(
            id=query.id * 10000,
            name=query.name + "가 레포지토리에 다녀옴"
        )
        return response
