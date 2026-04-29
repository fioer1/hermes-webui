import pathlib

import pytest
import yaml


REPO = pathlib.Path(__file__).parent.parent


def read(rel):
    return (REPO / rel).read_text(encoding="utf-8")


def test_prompt_cache_status_reads_model_api_mode(tmp_path, monkeypatch):
    import api.config as cfg

    cfgfile = tmp_path / "config.yaml"
    cfgfile.write_text(
        yaml.safe_dump({"model": {"default": "gpt-5.4", "api_mode": "chat_completions"}}),
        encoding="utf-8",
    )
    monkeypatch.setattr(cfg, "_get_config_path", lambda: cfgfile)

    status = cfg.get_prompt_cache_status()

    assert status["enabled"] is True
    assert status["api_mode"] == "chat_completions"


def test_set_prompt_cache_enabled_persists_api_mode(tmp_path, monkeypatch):
    import api.config as cfg

    cfgfile = tmp_path / "config.yaml"
    cfgfile.write_text(
        yaml.safe_dump(
            {
                "model": {
                    "default": "gpt-5.4",
                    "provider": "lansekafei",
                    "base_url": "https://example.invalid/v1",
                    "api_mode": "codex_responses",
                }
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(cfg, "_get_config_path", lambda: cfgfile)

    on = cfg.set_prompt_cache_enabled(True)
    data = yaml.safe_load(cfgfile.read_text(encoding="utf-8"))
    assert on["enabled"] is True
    assert data["model"]["api_mode"] == "chat_completions"
    assert data["model"]["provider"] == "lansekafei"

    off = cfg.set_prompt_cache_enabled(False)
    data = yaml.safe_load(cfgfile.read_text(encoding="utf-8"))
    assert off["enabled"] is False
    assert data["model"]["api_mode"] == "codex_responses"


def test_set_prompt_cache_rejects_non_boolean():
    import api.config as cfg

    with pytest.raises(ValueError):
        cfg.set_prompt_cache_enabled("yes")


def test_prompt_cache_route_is_wired():
    src = read("api/routes.py")
    assert 'if parsed.path == "/api/prompt-cache"' in src
    assert "get_prompt_cache_status" in src
    assert "set_prompt_cache_enabled" in src


def test_prompt_cache_control_is_in_settings_ui():
    html = read("static/index.html")
    panels = read("static/panels.js")

    assert 'id="settingsPromptCacheEnabled"' in html
    assert "/api/prompt-cache" in panels
    assert "settingsPromptCacheEnabled" in panels
