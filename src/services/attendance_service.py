class AttendanceService:
    def __init__(self, zk_api):
        self.zk_api = zk_api

    def get_device_attendance(self):
        return self.zk_api.get_attendance()

    def live_capture(self, func):
        for _ in self.zk_api.live_capture():
            func()

    @staticmethod
    def resolve_status(status):
        if status == 0:
            return 'Check In'
        elif status == 1:
            return 'Check Out'

# CTO
# DEV
# 44 45 56
