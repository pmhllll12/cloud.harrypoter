from __future__ import annotations

import logging
import random
from typing import Any

from harry_poter.adapter.inbound.api.schemas.dx_sphinx_quiz_schemas import SphinxQuizSchema
from harry_poter.app.dtos.dx_sphinx_quiz_dto import (
    QuizListItem,
    SphinxQuizQuery,
    SphinxQuizResponse,
    SubmitAnswerQuery,
    SubmitAnswerResponse,
)
from harry_poter.app.ports.input.dx_sphinx_quiz_use_case import SphinxQuizUseCase
from harry_poter.app.ports.input.dx_wizard_point_use_case import WizardPointUseCase
from harry_poter.app.ports.input.po_harry_user_use_case import HarryUserUseCase
from harry_poter.app.ports.output.dx_sphinx_quiz_port import SphinxQuizPort

logger = logging.getLogger(__name__)


class SphinxQuizInteractor(SphinxQuizUseCase):

    def __init__(self, repository: SphinxQuizPort, harry: HarryUserUseCase, wizard_point: WizardPointUseCase) -> None:
        self.repository = repository
        self.harry = harry
        self.wizard_point = wizard_point

    async def quiz_search(self, user_id: int, heritage_name: str) -> dict[str, Any]:
        all_quizzes = await self.repository.get_quizzes_by_heritage(heritage_name)
        correct_ids = await self.repository.get_user_progress(user_id, heritage_name)

        unanswered = [q for q in all_quizzes if q.id not in correct_ids]
        if not unanswered:
            logger.info("[SphinxQuizInteractor/quiz_search] user_id=%s 모든 퀴즈 완료", user_id)
            return {"message": "모든 퀴즈를 완료했습니다!", "quiz": None}

        quiz = random.choice(unanswered)
        logger.info("[SphinxQuizInteractor/quiz_search] user_id=%s quiz_id=%s", user_id, quiz.id)

        return {
            "quiz_id": quiz.id,
            "heritage_name": quiz.heritage_name,
            "question": quiz.question,
            "choices": list(quiz.choices),
        }

    async def get_quiz_list(self, user_id: int, heritage_name: str) -> list[QuizListItem]:
        all_quizzes = await self.repository.get_quizzes_by_heritage(heritage_name)
        correct_ids = await self.repository.get_user_progress(user_id, heritage_name)

        logger.info("[SphinxQuizInteractor/get_quiz_list] user_id=%s heritage=%s", user_id, heritage_name)

        return [QuizListItem(quiz=q, is_correct=q.id in correct_ids) for q in all_quizzes]

    async def submit_answer(self, query: SubmitAnswerQuery) -> SubmitAnswerResponse:
        quiz = await self.repository.get_quiz_by_id(query.quiz_id)
        is_correct = query.answer.strip() == quiz.answer.strip()

        if is_correct:
            await self.repository.save_quiz_result(query.user_id, query.quiz_id, is_correct=True)
            await self.wizard_point.point_save(user_id=query.user_id)
            message = "정답입니다!"
        else:
            message = f"오답입니다. 정답은 '{quiz.answer}'입니다."

        logger.info(
            "[SphinxQuizInteractor/submit_answer] user_id=%s quiz_id=%s is_correct=%s",
            query.user_id, query.quiz_id, is_correct,
        )

        return SubmitAnswerResponse(
            is_correct=is_correct,
            correct_answer=quiz.answer,
            message=message,
        )

    async def test_model(self, test_set) -> dict[str, Any]:
        """스핑크스가 덤블도어가 제안한 10개 모델의 트레이닝 정도를 점수화 해서 1등을 뽑는것"""

        train_result = await self.harry.train_model(test_set)
        scores = train_result["scores"]

        ranking = []
        for name in scores:
            ranking.append({"model": name, "accuracy": scores[name]})
        ranking.sort(key=lambda entry: entry["accuracy"], reverse=True)

        rank = 1
        for entry in ranking:
            entry["rank"] = rank
            rank = rank + 1

        winner = ranking[0]["model"]
        logger.info("[SphinxQuizInteractor/test_model] ranking=%s winner=%s", ranking, winner)

        return {"ranking": ranking, "winner": winner}

    async def introduce_myself(self, schema: SphinxQuizSchema) -> SphinxQuizResponse:
        query = SphinxQuizQuery(id=schema.id, name=schema.name)
        return await self.repository.introduce_myself(query)
