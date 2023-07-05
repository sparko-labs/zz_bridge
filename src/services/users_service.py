class UsersService:
    def __init__(self, zk_api):
        self.zk_api = zk_api

    def get_device_users(self):
        return self.zk_api.get_users()
