import flet
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
)


class Home(UserControl):
    def __init__(
            self,
            page,
            users_service,
            attendance_service
    ):
        super().__init__()
        self.build_attendance_btn = None
        self.build_user_btn = None
        self.attendance_table = None
        self.user_table = None
        self.page = page
        self.users_service = users_service
        self.attendance_service = attendance_service

    def build(self):

        self.build_user_btn = FilledButton(text="Re-Sync", on_click=self.fetch_users, disabled=True)
        self.build_attendance_btn = FilledButton(text="Re-Sync", on_click=self.fetch_attendance, disabled=True)

        self.build_user_table()
        self.build_attendance_table()

        if self.build_user_btn and self.build_attendance_btn:
            self.build_user_btn.disabled = False
            self.build_attendance_btn.disabled = False

        return Column(
            width=1000,
            controls=[Row(
                alignment=MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    Text('Users'),
                    self.build_user_btn
                ],
            ), self.user_table, Row(
                alignment=MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    Text('Attendance'),
                    self.build_attendance_btn
                ],
            ), self.attendance_table],
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

        for i in range(len(users)):
            data_rows.append(DataRow(
                cells=[
                    DataCell(Text(users[i].name)),
                    DataCell(Text(users[i].user_id)),
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
            ],
            rows=self.user_table_rows(),
        )

    def attendance_table_rows(self):
        attendance = self.attendance_service.get_device_attendance()
        data_rows = []

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
        self.build_user_btn.disabled = True
        self.build_user_btn.Text = 'Fetching...'
        self.update()
        self.user_table.rows = self.user_table_rows()
        self.update()
        self.build_user_btn.disabled = False
        self.build_user_btn.Text = 'Re-Sync'
        self.update()

    def fetch_attendance(self, e):
        self.build_attendance_btn.disabled = True
        self.build_attendance_btn.Text = 'Fetching...'
        self.update()
        self.attendance_table.rows = self.attendance_table_rows()
        self.update()
        self.build_attendance_btn.disabled = False
        self.build_attendance_btn.Text = 'Re-Sync'
        self.update()
