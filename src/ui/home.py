from flet import (
    Column,
    Row,
    UserControl,
    Text,
    FilledButton,
    MainAxisAlignment,
    DataTable,
    DataColumn,
    DataRow,
    DataCell,
    border,
    SnackBar,
    colors,
    TextAlign,
    CrossAxisAlignment
)


class Home(UserControl):
    def __init__(
            self,
            page,
            users_service,
            attendance_service
    ):
        super().__init__()
        self.no_attendance = None
        self.no_users = None
        self.sync_attendance_btn = None
        self.sync_user_btn = None
        self.build_attendance_btn = None
        self.build_user_btn = None
        self.attendance_table = None
        self.user_table = None
        self.page = page
        self.users_service = users_service
        self.attendance_service = attendance_service

    def build(self):

        self.no_users = Column(horizontal_alignment=CrossAxisAlignment.CENTER)
        self.no_attendance = Column(horizontal_alignment=CrossAxisAlignment.CENTER)

        self.build_user_btn = FilledButton(text="Re-Fetch", on_click=self.fetch_users, disabled=True)
        self.build_attendance_btn = FilledButton(text="Re-Fetch", on_click=self.fetch_attendance, disabled=True)

        self.sync_user_btn = FilledButton(text="Re-Sync", on_click=self.sync_users)
        self.sync_attendance_btn = FilledButton(text="Re-Sync", on_click=self.sync_attendances)

        self.build_user_table()
        self.build_attendance_table()

        if self.build_user_btn and self.build_attendance_btn:
            self.build_user_btn.disabled = False
            self.build_attendance_btn.disabled = False

        return Column(
            width=1000,
            horizontal_alignment=CrossAxisAlignment.CENTER,
            controls=[
                Row(
                    alignment=MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        Text('Users'),
                        Row(
                            controls=[
                                self.sync_user_btn,
                                self.build_user_btn
                            ])
                    ],
                ),
                self.user_table,
                self.no_users,
                Row(
                    alignment=MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        Text('Attendance'),
                        Row(
                            controls=[
                                self.sync_attendance_btn,
                                self.build_attendance_btn
                            ])
                    ],
                ),
                self.attendance_table,
                self.no_attendance
            ],
        )

    @staticmethod
    def resolve_status(status):
        if status == 0:
            return 'Check In'
        elif status == 1:
            return 'Check Out'

    def user_table_rows(self):
        users = self.users_service.get_device_users()
        data_rows = []
        if len(users) <= 0:
            self.no_users.controls.append(Text('No Users', text_align=TextAlign.CENTER))
        else:
            self.no_users.controls = []

        for i in range(len(users)):
            btn = FilledButton(text="Capture Finger", on_click=lambda event, user=users[i]: self.capture_finger(event, user))
            data_rows.append(DataRow(
                cells=[
                    DataCell(Text(users[i].user_id)),
                    DataCell(Text(users[i].name)),
                    DataCell(btn),
                ],
            ), )

        return data_rows

    def build_user_table(self):
        self.user_table = DataTable(
            width=1000,
            border=border.all(2),
            vertical_lines=border.BorderSide(1),
            horizontal_lines=border.BorderSide(1),
            columns=[
                DataColumn(Text("ID")),
                DataColumn(Text("Name")),
                DataColumn(Text("Actions")),
            ],
            rows=self.user_table_rows(),
        )

    def attendance_table_rows(self):
        attendance = self.attendance_service.get_device_attendance()
        data_rows = []
        if len(attendance) <= 0:
            self.no_attendance.controls.append(Text('No Attendances', text_align=TextAlign.CENTER))
        else:
            self.no_attendance.controls = []

        for i in range(len(attendance)):
            data_rows.append(DataRow(
                cells=[
                    DataCell(Text(attendance[i].user_id)),
                    DataCell(Text(Home.resolve_status(attendance[i].punch))),
                    DataCell(Text(str(attendance[i].timestamp))),
                ],
            ), )

        return data_rows

    def build_attendance_table(self):
        self.attendance_table = DataTable(
            width=1000,
            border=border.all(2),
            vertical_lines=border.BorderSide(1),
            horizontal_lines=border.BorderSide(1),
            columns=[
                DataColumn(Text("User Id")),
                DataColumn(Text("Punch")),
                DataColumn(Text("Timestamp")),
            ],
            rows=self.attendance_table_rows(),
        )

    def fetch_users(self, e):
        print(e)
        self.build_user_btn.disabled = True
        self.build_user_btn.Text = 'Fetching...'
        self.update()
        self.user_table.rows = self.user_table_rows()
        self.update()
        self.build_user_btn.disabled = False
        self.build_user_btn.Text = 'Re-Fetch'
        self.update()

    def fetch_attendance(self, e):
        self.build_attendance_btn.disabled = True
        self.build_attendance_btn.Text = 'Fetching...'
        self.update()
        self.attendance_table.rows = self.attendance_table_rows()
        self.update()
        self.build_attendance_btn.disabled = False
        self.build_attendance_btn.Text = 'Re-Fetch'
        self.update()

    def sync_users(self, e):
        try:
            self.sync_user_btn.disabled = True
            self.sync_user_btn.Text = 'Syncing...'
            self.update()
            self.users_service.sync_to_device()
            self.fetch_users(None)
            self.sync_user_btn.disabled = False
            self.sync_user_btn.Text = 'Re-Sync'
            self.update()
            self.page.snack_bar = SnackBar(Text("Users synced"), bgcolor=colors.GREEN_900,
                                           duration=1500)
            self.page.snack_bar.open = True
            self.page.update()

        except Exception as err:
            self.page.snack_bar = SnackBar(Text("Error: " + repr(err)), bgcolor=colors.RED_900)
            self.page.snack_bar.open = True
            self.page.update()

    def sync_attendances(self, e):
        try:
            self.sync_attendance_btn.disabled = True
            self.sync_attendance_btn.Text = 'Syncing...'
            self.update()
            self.attendance_service.sync_to_sparko()
            self.fetch_attendance(None)
            self.sync_attendance_btn.disabled = False
            self.sync_attendance_btn.Text = 'Re-Sync'
            self.update()
            self.page.snack_bar = SnackBar(Text("Attendance synced"), bgcolor=colors.GREEN_900,
                                           duration=1500)
            self.page.snack_bar.open = True
            self.page.update()

        except Exception as err:
            self.page.snack_bar = SnackBar(Text("Error: " + repr(err)), bgcolor=colors.RED_900)
            self.page.snack_bar.open = True
            self.page.update()

    def capture_finger(self, e, user):
        print('delete user')
        print(user)
        print(user.uid)
        try:
            self.users_service.capture_finger(user)
        except Exception as ex:
            print(ex)