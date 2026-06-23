from dataclasses import dataclass


@dataclass(frozen=True)
class SphinxQuizQuery:

    id: int
    name: str


@dataclass(frozen=True)
class SphinxQuizResponse:

    id: int
    name: str


@dataclass(frozen=True)
class HeritageQuizItem:

    id: int
    heritage_name: str
    question: str
    answer: str
    choices: tuple[str, ...]


@dataclass(frozen=True)
class QuizListItem:

    quiz: HeritageQuizItem
    is_correct: bool


@dataclass(frozen=True)
class SubmitAnswerQuery:

    user_id: int
    quiz_id: int
    answer: str


@dataclass(frozen=True)
class SubmitAnswerResponse:

    is_correct: bool
    correct_answer: str
    message: str
