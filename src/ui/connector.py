from flet import (
    Checkbox,
    Column,
    Row,
    TextField,
    UserControl,
    Text,
    FilledButton,
    MainAxisAlignment,
    SnackBar,
    colors,
    Container,
    Card,
    View,
    AppBar,
    ScrollMode
)
from ..api import ZkAPI, SparkoAPI
from .home import Home

from ..services import UsersService, AttendanceService


class Connector(UserControl):
    def __init__(
            self,
            page
    ):
        super().__init__()
        self.snack_bar = None
        self.btn = None
        self.check = None
        self.port = None
        self.ip = None
        self._state = {
            'timeout': 5,
            'verbose': False,
            'password': 0,
            'encoding': 'UTF-8',
            'ip': '192.168.1.29',
            'port': '4370'
        }
        self.page = page

    def build(self):

        self.ip = TextField(hint_text="Device IP", expand=True,
                            dense=True, value=self._state['ip'])
        self.port = TextField(hint_text="Device Port",
                              expand=True, dense=True, value=self._state['port'])
        self.check = Checkbox(label="Force UDP", value=False)
        self.btn = FilledButton(text="Connect", on_click=self.connect)

        form = Column(
            width=600,
            spacing=20,
            controls=[
                Text("Device Connection", size=40),
                Row(
                    controls=[
                        self.ip,
                    ],
                ),
                Row(
                    controls=[
                        self.port,
                    ],
                ),
                Row(
                    alignment=MainAxisAlignment.CENTER,
                    controls=[
                        self.btn
                    ],
                ),
            ],
        )

        container = Container(
            content=form,
            padding=15,
        )
        card = Card(
            content=container,
        )

        # application's root control (i.e. "view") containing all other controls
        return card

    def connect(self, e):
        try:
            self.btn.disabled = True
            self.btn.text = 'Connecting...'
            self.update()

            self._state['ip'] = self.ip.value
            self._state['port'] = int(self.port.value)

            zk_api = ZkAPI(**self._state)
            sparko_api = SparkoAPI()

            self.page.snack_bar = SnackBar(Text("Connected to " + self.ip.value), bgcolor=colors.GREEN_900,
                                           duration=1500)
            self.page.snack_bar.open = True
            self.page.update()

            self.dashboard(UsersService(zk_api, sparko_api), AttendanceService(zk_api, sparko_api))

        except Exception as ex:
            self.page.snack_bar = SnackBar(Text("Unable to connect: " + repr(ex)), bgcolor=colors.RED_900,
                                           duration=1500)
            self.page.snack_bar.open = True
            self.page.update()
            self.btn.disabled = False
            self.btn.text = 'Connect'
            self.update()

    def dashboard(self, users_service, attendance_service):
        try:
            home = Home(self.page, users_service, attendance_service)
            appbar = AppBar(
                title=Text("ZZ Bridge"),
                center_title=True,
                bgcolor=colors.SURFACE_VARIANT,
            )

            view = View("/", [appbar, home], scroll=ScrollMode.AUTO)
            view.horizontal_alignment = "center"

            self.page.views.clear()
            self.page.views.append(view)

            self.page.update()

        except Exception as ex:
            self.page.snack_bar = SnackBar(Text("Error: " + repr(ex)), bgcolor=colors.RED_900)
            self.page.snack_bar.open = True
            self.page.update()
