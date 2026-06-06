import reflex as rx
from frontend_backend.frontend_backend import app

def test_app_initialization():
    assert isinstance(app, rx.App)
