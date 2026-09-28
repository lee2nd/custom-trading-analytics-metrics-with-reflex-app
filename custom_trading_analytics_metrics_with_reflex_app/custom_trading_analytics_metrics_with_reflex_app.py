import reflex as rx

from .components.layout import layout
from .state import AppState


def index() -> rx.Component:
    return layout()


app = rx.App()
app.add_page(index, route="/", on_load=AppState.submit)
