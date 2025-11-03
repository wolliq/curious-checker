import sys
import types
from pathlib import Path
import importlib.util


def test_main_logs_and_sets_streamlit_title(monkeypatch):
    debug_messages: list[str] = []
    fake_logger = types.SimpleNamespace(debug=lambda message: debug_messages.append(message))
    fake_loguru = types.ModuleType("loguru")
    fake_loguru.logger = fake_logger
    monkeypatch.setitem(sys.modules, "loguru", fake_loguru)

    titles: list[str] = []
    fake_streamlit = types.ModuleType("streamlit")
    fake_streamlit.title = lambda message: titles.append(message)
    monkeypatch.setitem(sys.modules, "streamlit", fake_streamlit)
    monkeypatch.delitem(sys.modules, "main", raising=False)

    module_path = Path(__file__).resolve().parent.parent / "main.py"
    spec = importlib.util.spec_from_file_location("main", module_path)
    app = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    sys.modules["main"] = app
    spec.loader.exec_module(app)

    app.main()

    assert debug_messages == ["Hello from curious-checker!"]
    assert titles == ["Hello from curious checker!"]
