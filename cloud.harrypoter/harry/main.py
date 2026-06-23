import logging
import os
import sys
from contextlib import asynccontextmanager
from pathlib import Path

# `harry/` 에서 실행: `main` 모듈은 이 파일, `harry_poter` 는 `apps/` 에, `matrix` 는 `core/` 에 있음
_BACKEND_ROOT = Path(__file__).resolve().parent
_APPS_ROOT = _BACKEND_ROOT / "apps"
_CORE_ROOT = _BACKEND_ROOT / "core"
for _p in (_BACKEND_ROOT, _APPS_ROOT, _CORE_ROOT):
    _p_str = str(_p)
    if _p_str not in sys.path:
        sys.path.append(_p_str)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import create_all_tables, dispose_engine
from harry_poter.adapter.inbound.api import harry_poter_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_PORT = int(os.getenv("API_PORT", "8000"))
API_HOST = os.getenv("API_HOST", "127.0.0.1").strip() or "127.0.0.1"


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_all_tables()
    logger.info(
        "API 준비 port=%s — docs http://127.0.0.1:%s/docs | ping http://127.0.0.1:%s/ping",
        API_PORT, API_PORT, API_PORT,
    )
    try:
        yield
    finally:
        await dispose_engine()


app = FastAPI(title="Harry Poter Demo", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(harry_poter_router)


@app.get("/ping")
def ping() -> dict[str, bool]:
    return {"ok": True}


@app.get("/")
def read_root():
    return {"message": "Harry Poter API", "docs": "/docs"}


if __name__ == "__main__":
    import uvicorn

    # 주의: `python main.py` 는 반드시 `harry/` 디렉터리에서 실행하세요.
    uvicorn.run(app, host=API_HOST, port=API_PORT, log_level="info")
