# Harry Poter 앱 (`harry/apps/harry_poter`) — LLM 코딩 지침

`minho/apps/titanic`(cloud.pmhllll12 저장소)을 참조 구현으로 삼아 만든 헥사고날 데모 앱.
같은 디렉터리 구조·DI 패턴을 쓰되 도메인은 "트라이위저드 시합 챔피언 생존 예측"이다.

```
harry/apps/harry_poter/
├── .cursorrules
├── _docs/CLAUDE.md
├── adapter/
├── app/
├── domain/
└── dependencies/
```

---

## 라우터 등록

[`adapter/inbound/api/__init__.py`](../adapter/inbound/api/__init__.py):

```python
harry_poter_router = APIRouter(prefix="/harry-poter", tags=["harry-poter"])
```

워크스페이스 루트에 `main.py`가 생기면 `app.include_router(harry_poter_router)` — **prefix 중복 금지**.
(이 저장소엔 아직 `main.py`/`database.py`/`core/matrix/`가 없다 — 루트 와이어링은 범위 밖.)

### 주요 엔드포인트

| 경로 | 설명 |
|------|------|
| `GET /harry-poter/` | API 인덱스 |
| `GET /harry-poter/weasley/myself` | 위즐리 가족 |
| `POST /harry-poter/weasley/upload` | 챔피언 CSV 업로드 |
| `GET /harry-poter/harry/myself` | 해리 포터 |
| `POST /harry-poter/professor/chat` | 덤블도어 교수 채팅 (오케스트레이터) |
| `GET /harry-poter/wizardpoint/correlation-plot` | 생존 상관관계 히트맵 |

---

## 캐릭터 모듈 (v1 라우터)

`adapter/inbound/v1/` — 파일명 패턴 `ax_*_router.py`, `dx_*_router.py`, `po_*_router.py`, `sm_*_router.py`.

각 라우터는 `APIRouter(prefix="/<캐릭터>", …)` 이고, 상위 `harry_poter_router`와 합쳐져
`/harry-poter/<캐릭터>/...` 가 된다.

---

## 유스케이스·의존성

- Provider: `dependencies/*_provider.py` — FastAPI `Depends(get_db)`.
- Interactor: `app/use_cases/*_interactor.py` — 포트(input/output) 구현.
- **덤블도어 교수**는 `HarryUserUseCase`, `DumbledoreStoreUseCase` 등 7개 유스케이스를
  생성자 주입으로 연결 (`po_professor_festival_interactor.py`).

스키마 이름은 라우터·포트·interactor에서 **동일**하게 유지:

- `ProfessorFestivalSchema`, `ProfessorFestivalChatRequest`, `ProfessorFestivalChatResponse`
  → `schemas/po_professor_festival_schemas.py`

---

## ORM·DB

| 테이블 | ORM | 비고 |
|--------|-----|------|
| 챔피언 명단 | `champions` | `HarryUserOrm` (PK: `champion_id`) |
| 시합 등록 정보 | `tournament_entries` | `DumbledoreStoreOrm` (FK → `champions.champion_id`) |

나머지 7개 캐릭터의 ORM은 `__abstract__ = True` 자리표시자다(titanic의 andrews/walter/lowe/hartley/cal/smith와 동일 패턴).

---

## async 규칙

| 메소드 성격 | 형태 | 근거 |
|------------|------|------|
| CPU-bound (Kiwi 형태소 분석 등) | `def` | `async`를 붙여도 이벤트 루프 블로킹은 동일 |
| I/O-bound (DB·LLM·네트워크) | `async def` | `await` 가능한 호출이 있을 때만 |

---

## 도메인 문서 연결

- 캐릭터 ↔ 기술 역할 매핑, 피처 정의: [[harry-features]]
