import pathlib


REPO = pathlib.Path(__file__).parent.parent


def read(rel):
    return (REPO / rel).read_text(encoding="utf-8")


def test_auto_generate_titles_setting_exists():
    src = read("api/config.py")

    assert '"auto_generate_titles": True' in src
    assert '"auto_generate_titles"' in src
    assert "_SETTINGS_BOOL_KEYS" in src


def test_streaming_respects_auto_generate_titles_setting():
    src = read("api/streaming.py")

    assert "auto_generate_titles" in src
    assert "load_settings," in src
    assert "_should_bg_title" in src
    assert "load_settings" in src


def test_auto_title_control_is_in_settings_ui():
    html = read("static/index.html")
    panels = read("static/panels.js")

    assert 'id="settingsAutoGenerateTitles"' in html
    assert "auto_generate_titles" in panels
    assert "settingsAutoGenerateTitles" in panels
