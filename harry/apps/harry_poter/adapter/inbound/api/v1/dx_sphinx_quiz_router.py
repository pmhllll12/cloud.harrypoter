from fastapi import APIRouter, Depends

from harry_poter.adapter.inbound.api.schemas.dx_sphinx_quiz_schemas import SphinxQuizSchema
from harry_poter.app.dtos.dx_sphinx_quiz_dto import SphinxQuizResponse
from harry_poter.app.ports.input.dx_sphinx_quiz_use_case import SphinxQuizUseCase
from harry_poter.dependencies.dx_sphinx_quiz_provider import get_sphinx_quiz_use_case

'''
스핑크스 (The Sphinx)
트라이위저드 시합 미궁 과제에서 정답을 맞혀야만 통과시켜주는 수호자.
학습된 모델들을 검증 셋으로 채점해 순위를 매기는 시험관 역할.
'''

sphinx_quiz_router = APIRouter(prefix="/sphinx", tags=["sphinx"])


@sphinx_quiz_router.get("/myself")
async def introduce_myself(
    sphinx: SphinxQuizUseCase = Depends(get_sphinx_quiz_use_case)
) -> SphinxQuizResponse:
    return await sphinx.introduce_myself(
        SphinxQuizSchema(
            id=9,
            name="스핑크스 (The Sphinx)"
        )
    )
