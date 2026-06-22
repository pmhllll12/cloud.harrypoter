# Harry Poter 피처 & 캐릭터 매핑

`minho/apps/titanic`의 ML 파이프라인 구조를 그대로 가져와 도메인만 바꾼 데모다.
이 문서는 그 매핑을 **추론한 근거**까지 남겨, 나중에 코드만 보고는 알 수 없는 의도를 보존한다.

## 도메인 치환

| Titanic | Harry Poter | 비고 |
|---------|-------------|------|
| 승객(Passenger) 생존 예측 | 트라이위저드 시합 챔피언 생존 예측 | `Survived` 컬럼명 그대로 유지 (시합 과제는 실제로 생명을 위협함 — 원작 설정과 부합) |
| Pclass (1/2/3등석) | School (1=Hogwarts, 2=Beauxbatons, 3=Durmstrang) | 3개 학교 = 3개 등급, ordinal 구조가 동일 |
| Sex (male/female) | gender (male/female) | 변경 없음 |
| Age | Age | 변경 없음 |
| Fare (탑승 요금) | Galleons (참가 등록 보증금) | 연속형 수치, qcut 4분위 밴드 로직 동일 |
| Embarked (S/C/Q, 승선항) | WandCore (P=불사조 깃털/D=용 심장 힘줄/U=유니콘 털) | 3개 nominal 카테고리 구조가 동일 |
| Cabin (객실) | Tower (기숙사 탑/동) | 동일 구조(`deck`→`block`) |
| PassengerId | ChampionId | — |
| Ticket | WandPermit | — |
| SibSp / Parch | AlliesCount / MentorsCount | 학습 직전 drop되는 컬럼이라 의미보다 구조 유지가 핵심 |

## 캐릭터 ↔ 기술 역할 매핑

titanic은 12명의 캐릭터 중 9명만 실제 로직을 갖고 있다(나머지 3명 — Isidor/Molly/Ruth — 는
`introduce_myself`만 있는 자리표시자). harry_poter의 use_cases도 정확히 9개만 스캐폴딩되어 있어,
**그 9개 active 역할에 1:1로 매핑**했다.

| harry_poter 유스케이스 | 매핑한 titanic 역할 | 매핑 근거 |
|------------------------|----------------------|-----------|
| `ax_hermione_route` | Andrews(설계자) — Kiwi NLU 의도분석 + 프로필 추출 | "route"=라우팅. 헤르미온느는 빠른 판단·정보 정리로 질문 의도를 분류하는 두뇌 역할에 어울림 |
| `ax_hogwarts_hertage` | Walter(명단 관리자) — DB에서 train/test set 조회 | "heritage"=역사적 기록보관소. 호그와트 자체가 챔피언 명단을 보관하는 저장소 비유로 자연스러움 |
| `ax_lovegood_course` | Lowe(항해사) — feature_engineering 파이프라인 | "course"=가공 경로. 루나는 남들이 못 보는 패턴을 찾는 캐릭터라 원본→피처 변환 여정에 어울림 |
| `dx_sphinx_quiz` | Cal(검증자) — 여러 모델을 점수화해 순위 매김(test_model) | "quiz"=시험. 스핑크스는 원작에서 실제로 미궁 과제의 정답을 채점하는 존재 |
| `dx_wizard_point` | Hartley(악단장) — 상관관계 분석 + 히트맵 플롯 | "point"=점수. 호그와트 기숙사 점수 집계 비유로 각 피처의 생존 상관계수를 "포인트"로 표현 |
| `po_harry_user` | Jack(트레이너) — feature 학습 + train/predict | "user"=개별 프로필 예측. 해리 본인이 시합의 주인공이자 예측 대상 |
| `po_professor_festival` | Smith(선장) — 전체를 오케스트레이션하는 채팅 엔드포인트 | "festival"=트라이위저드 시합(축제). 교수가 시합 진행을 총괄하듯 모든 유스케이스를 호출 |
| `sm_dumbledore_store` | Rose(모델) — Strategy 패턴으로 여러 ML 알고리즘 보관 | "store"=저장소. 덤블도어는 지혜(여러 알고리즘)를 모아두는 존재로 Strategy Registry에 적합 |
| `sm_weasley_booking` | James(감독) — CSV 업로드로 챔피언 명단 등록 | "booking"=등록. 위즐리 가족은 발이 넓어 명단 등록 창구 역할에 어울림 |

## 알고리즘 TOP 10 (`sm_dumbledore_store_strategies.py`)

titanic의 `passenger_rose_model_strategies.py`를 그대로 포팅했다 — XGBoost, RandomForest,
LightGBM, CatBoost, LogisticRegression, DecisionTree, SVM, KNN, NaiveBayes, PCA+KMeans.

## 알려진 한계

- 이 저장소(`cloud.harrypoter`)에는 워크스페이스 루트 `main.py`/`database.py`/`core/matrix/`가 없어
  ORM·Provider의 `from database import get_db`, `from matrix.grid_neo_theone_base import Base` import는
  아직 실행되지 않는다. titanic과 동일한 와이어링이 루트에 추가되면 그대로 동작하도록 맞춰뒀다.
- 테스트(`tests/`)는 titanic 원본도 전부 빈 placeholder라 harry_poter도 동일하게 비워뒀다.
