from zk import const


class UsersService:
    def __init__(self, zk_api, sparko_api):
        self.zk_api = zk_api
        self.sparko_api = sparko_api

    def get_device_users(self):
        return self.zk_api.get_users()

    def sync_to_device(self):
        try:
            raw_employees = self.sparko_api.fetch_employees()
            device_users = self.zk_api.get_users()
            for x in raw_employees:
                if self.check_user_device(device_users, x['user_id']):
                    continue

                try:
                    self.zk_api.create_user(
                        user_id=x['user_id'],
                        name=x['name'],
                        privilege=const.USER_DEFAULT,
                    )
                except Exception as err:
                    raise Exception(err)

        except Exception as err:
            print(err)
            raise Exception(err)

    def capture_finger(self, user):
        try:
            return self.zk_api.capture_finger_index(user)
        except Exception as err:
            raise Exception(err)

    def get_finger(self, user):
        try:
            return self.zk_api.get_finger(user)
        except Exception as err:
            print(err)
            raise Exception(err)

    @staticmethod
    def check_user_device(users, user_id):
        for i in range(len(users)):
            if users[i].user_id == user_id:
                return True
        return False
