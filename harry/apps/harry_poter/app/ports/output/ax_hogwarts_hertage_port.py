from abc import ABC, abstractmethod

from harry_poter.app.dtos.ax_hogwarts_hertage_dto import HogwartsHeritageQuery, HogwartsHeritageResponse


class HogwartsHeritagePort(ABC):
    """호그와트 헤리티지의 챔피언 명단 관리 저장소."""

    @abstractmethod
    async def get_train_set(self) -> "pd.DataFrame":
        ''' Survived 컬럼이 있는 데이터 전체를 데이터 프레임으로 반환하는 메소드 '''
        pass

    @abstractmethod
    async def get_test_set(self) -> "pd.DataFrame":
        ''' Survived 컬럼이 없는 데이터 전체를 데이터 프레임으로 반환하는 메소드 '''
        pass

    @abstractmethod
    def introduce_myself(self, query: HogwartsHeritageQuery) -> HogwartsHeritageResponse:
        '''호그와트 헤리티지의 자기 소개 레포지토리 추상 메소드'''
        pass
