import flet
from flet import (
    Page,
    colors,
    AppBar,
    Text,
    View
)

from src.ui import Connector


def app(page: Page):
    page.title = "ZZ Bridge Device Connection"
    page.horizontal_alignment = "center"

    appbar = AppBar(
        title=Text("ZZ Bridge"),
        center_title=True,
        bgcolor=colors.SURFACE_VARIANT,
    )

    connector = Connector(page)

    view = View("/", [appbar, connector])
    view.horizontal_alignment = "center"

    page.views.clear()
    page.views.append(view)

    page.update()


def main():
    flet.app(target=app)


if __name__ == '__main__':
    main()
