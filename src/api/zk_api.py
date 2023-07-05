from zk import ZK, const

_client: ZK | None = None


class ZkAPI:
    def __init__(self, **kwargs):
        global _client
        if _client is None:
            _client = ZK(**kwargs)

        _client.connect()
        _client.read_sizes()

        self.client = _client

    def get_users(self):
        return self.client.get_users()

    def get_attendance(self):
        return self.client.get_attendance()

    def clear_attendance(self):
        return self.client.clear_attendance()

    def create_user(self, **kwargs):
        users = self.client.get_users()
        found = False
        for user in users:
            if user.user_id == kwargs['user_id']:
                found = True
                break

        if not found:
            self.client.set_user(**kwargs)

    def live_capture(self):
        for _ in self.client.live_capture():
            yield _

    def del_users(self):
        self.client.clear_data()
