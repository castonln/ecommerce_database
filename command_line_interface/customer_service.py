from user import User

class CustomerService:
    def __init__(self, cursor, user: User):
        self.cursor = cursor
        self.user = user

    def make_purchase(self):
        pass
