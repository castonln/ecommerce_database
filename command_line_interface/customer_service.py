from user import User
from datetime import date, datetime

class CustomerService:
    def __init__(self, connector, user: User):
        self.connector = connector
        self.user = user

    def make_purchase(self):
        pass

    def add_card(self, cc_number: str, cc_name: str, exp_date: str, csc: str) -> bool:
        """
        Adds a new card to the database.

        Returns True if insertion successful.

        Returns False otherwise.
        """

        card = (int(cc_number), str(cc_name), datetime.strptime(exp_date, "%Y-%m"), int(csc), str(self.user.username))
        print(card)
        try:
            self.connector.cursor.execute(
                "INSERT INTO creditcards (cc_number, cc_name, exp_date, csc, customer_username) VALUES (%s, %s, %s, %s, %s)", card)
            self.connector.db.commit()
            self.user.cards.append(card)
            return True
        except Exception as e:
            return False
