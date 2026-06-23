"""minho/test.py — Korean AI helpers 단위 테스트."""
import importlib.util
import sys
from pathlib import Path
from types import ModuleType
from unittest.mock import MagicMock

import pytest

# ---------------------------------------------------------------------------
# 외부 의존성(kiwipiepy, ollama)을 가짜로 교체한 뒤 모듈 임포트
# ---------------------------------------------------------------------------
# 이 파일 위치: <root>/apps/titanic/tests/test_korean_ai.py
# parents[3] = <root>/,  / "minho" = <root>/minho/
_MINHO_ROOT = Path(__file__).resolve().parents[3] / "minho"

_mock_kiwi_instance = MagicMock()
_mock_kiwi_module = MagicMock()
_mock_kiwi_module.Kiwi.return_value = _mock_kiwi_instance

_mock_ollama = MagicMock()


class FakeResponseError(Exception):
    def __init__(self, msg: str = "", status_code: int | None = None):
        super().__init__(msg)
        self.status_code = status_code


_mock_ollama.ResponseError = FakeResponseError

sys.modules.setdefault("kiwipiepy", _mock_kiwi_module)
sys.modules.setdefault("ollama", _mock_ollama)

_spec = importlib.util.spec_from_file_location("minho_korean_ai", _MINHO_ROOT / "test.py")
_mod: ModuleType = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)  # type: ignore[union-attr]

resolve_model = _mod._resolve_ollama_model
installed_names = _mod._installed_model_names
pick_model = _mod._pick_model
run_ai = _mod.run_korean_ai
DEFAULT = _mod.DEFAULT_OLLAMA_MODEL

pytestmark = pytest.mark.ollama


# ---------------------------------------------------------------------------
# 헬퍼
# ---------------------------------------------------------------------------

def _make_model_list(*names: str) -> MagicMock:
    models = [MagicMock(model=n) for n in names]
    fake = MagicMock()
    fake.models = models
    return fake


# ---------------------------------------------------------------------------
# _resolve_ollama_model
# ---------------------------------------------------------------------------

class TestResolveOllamaModel:
    def test_no_env_returns_default(self, monkeypatch):
        monkeypatch.delenv("OLLAMA_MODEL", raising=False)
        assert resolve_model() == DEFAULT

    def test_empty_string_returns_default(self, monkeypatch):
        monkeypatch.setenv("OLLAMA_MODEL", "   ")
        assert resolve_model() == DEFAULT

    @pytest.mark.parametrize("placeholder", [
        "설치한_모델_이름",
        "설치된_모델이름",
        "설치된_모델_이름",
    ])
    def test_placeholder_warns_and_returns_default(self, monkeypatch, capsys, placeholder):
        monkeypatch.setenv("OLLAMA_MODEL", placeholder)
        assert resolve_model() == DEFAULT
        assert "경고" in capsys.readouterr().out

    def test_korean_chars_warns_and_returns_default(self, monkeypatch, capsys):
        monkeypatch.setenv("OLLAMA_MODEL", "한글모델명")
        assert resolve_model() == DEFAULT
        assert "경고" in capsys.readouterr().out

    def test_valid_ascii_model_returned(self, monkeypatch):
        monkeypatch.setenv("OLLAMA_MODEL", "llama3.2")
        assert resolve_model() == "llama3.2"

    def test_valid_model_with_tag(self, monkeypatch):
        monkeypatch.setenv("OLLAMA_MODEL", "qwen2.5:7b")
        assert resolve_model() == "qwen2.5:7b"


# ---------------------------------------------------------------------------
# _installed_model_names
# ---------------------------------------------------------------------------

class TestInstalledModelNames:
    def test_returns_name_list(self):
        _mock_ollama.list.return_value = _make_model_list("llama3.2", "qwen2.5:3b")
        assert installed_names() == ["llama3.2", "qwen2.5:3b"]

    def test_empty_models_returns_empty(self):
        _mock_ollama.list.return_value = _make_model_list()
        assert installed_names() == []

    def test_skips_blank_name(self):
        models = [MagicMock(model=""), MagicMock(model="  "), MagicMock(model="llama3.2")]
        fake = MagicMock()
        fake.models = models
        _mock_ollama.list.return_value = fake
        assert installed_names() == ["llama3.2"]

    def test_ollama_unavailable_raises_systemexit(self):
        _mock_ollama.list.side_effect = ConnectionError("연결 실패")
        with pytest.raises(SystemExit, match="Ollama"):
            installed_names()
        _mock_ollama.list.side_effect = None


# ---------------------------------------------------------------------------
# _pick_model
# ---------------------------------------------------------------------------

class TestPickModel:
    def setup_method(self):
        _mock_ollama.list.side_effect = None

    def test_exact_match_returned(self):
        _mock_ollama.list.return_value = _make_model_list("qwen2.5:3b", "llama3.2")
        assert pick_model("qwen2.5:3b") == "qwen2.5:3b"

    def test_no_models_raises_systemexit(self):
        _mock_ollama.list.return_value = _make_model_list()
        with pytest.raises(SystemExit, match="설치된"):
            pick_model("any")

    def test_fallback_eeve_hint(self, capsys):
        _mock_ollama.list.return_value = _make_model_list("anpigon/eeve-korean-10.8b", "llama3.2")
        result = pick_model("missing-model")
        assert "eeve" in result.lower()
        assert "안내" in capsys.readouterr().out

    def test_fallback_korean_hint(self, capsys):
        _mock_ollama.list.return_value = _make_model_list("some-korean-7b", "llama3.2")
        result = pick_model("missing-model")
        assert result == "some-korean-7b"
        assert "안내" in capsys.readouterr().out

    def test_fallback_first_in_list(self, capsys):
        _mock_ollama.list.return_value = _make_model_list("llama3.2", "mistral")
        result = pick_model("missing-model")
        assert result == "llama3.2"
        assert "안내" in capsys.readouterr().out


# ---------------------------------------------------------------------------
# run_korean_ai
# ---------------------------------------------------------------------------

class TestRunKoreanAi:
    def setup_method(self):
        _mock_ollama.list.side_effect = None
        _mock_ollama.chat.side_effect = None
        _mock_kiwi_instance.reset_mock()
        _mod.kiwi = _mock_kiwi_instance

    def _setup(
        self,
        space_result: str,
        tokens: list,
        chat_content: str,
        model_names: list[str] | None = None,
    ):
        _mock_kiwi_instance.space = MagicMock(return_value=space_result)
        _mock_kiwi_instance.tokenize = MagicMock(return_value=tokens)

        fake_msg = MagicMock()
        fake_msg.content = chat_content
        fake_resp = MagicMock()
        fake_resp.message = fake_msg
        _mock_ollama.chat.return_value = fake_resp

        names = model_names or [DEFAULT]
        _mock_ollama.list.return_value = _make_model_list(*names)

    def test_returns_stripped_response(self, monkeypatch):
        monkeypatch.delenv("OLLAMA_MODEL", raising=False)
        tok = MagicMock()
        tok.form = "테스트"
        tok.tag = "NNG"
        self._setup("정제된 문장", [tok], "  답변 내용  ")

        assert run_ai("테스트 입력") == "답변 내용"

    def test_kiwi_space_called_with_original(self, monkeypatch):
        monkeypatch.delenv("OLLAMA_MODEL", raising=False)
        self._setup("cleaned", [], "ok")

        run_ai("원본 문장")
        _mock_kiwi_instance.space.assert_called_once_with("원본 문장")

    def test_ollama_chat_uses_cleaned_text(self, monkeypatch):
        monkeypatch.delenv("OLLAMA_MODEL", raising=False)
        self._setup("정제된 문장", [], "response")

        run_ai("입력")
        _, kwargs = _mock_ollama.chat.call_args
        messages = kwargs.get("messages", [])
        assert any(m.get("content") == "정제된 문장" for m in messages if isinstance(m, dict))

    def test_only_nouns_extracted(self, monkeypatch, capsys):
        monkeypatch.delenv("OLLAMA_MODEL", raising=False)
        noun = MagicMock(); noun.form = "명사"; noun.tag = "NNG"
        verb = MagicMock(); verb.form = "동사"; verb.tag = "VV"
        self._setup("text", [noun, verb], "ok")

        run_ai("입력")
        out = capsys.readouterr().out
        assert "명사" in out
        assert "동사" not in out

    def test_response_error_404_raises_systemexit(self, monkeypatch):
        monkeypatch.delenv("OLLAMA_MODEL", raising=False)
        self._setup("text", [], "")
        _mock_ollama.chat.side_effect = FakeResponseError("not found", status_code=404)

        with pytest.raises(SystemExit, match="모델을 찾을 수 없습니다"):
            run_ai("입력")
