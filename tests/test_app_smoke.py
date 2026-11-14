from streamlit.testing.v1 import AppTest


def test_streamlit_app_renders_without_exceptions():
    app = AppTest.from_file("../app.py").run(timeout=20)
    assert not app.exception
    assert any("MoonSight" in title.value for title in app.title)
