from ..api import ZkAPI


class AttendanceService:
    def __init__(self, zk_api, sparko_api):
        self.zk_api = zk_api
        self.sparko_api = sparko_api

    def get_device_attendance(self):
        return self.zk_api.get_attendance()

    def live_capture(self, func):
        for _ in self.zk_api.live_capture():
            func()

    def sync_to_sparko(self):
        attendances = self.zk_api.get_attendance()

        for attendance in attendances:
            try:
                self.sparko_api.post_attendance({
                    'dateTime': attendance.timestamp,
                    'ssn': attendance.user_id,
                    'punch': attendance.punch,
                })
            except Exception as err:
                print(err)
        self.zk_api.clear_attendance()

    @staticmethod
    def resolve_status(status):
        if status == 0:
            return 'Check In'
        elif status == 1:
            return 'Check Out'

# CTO
# DEV
# 44 45 56
