from user import User
from product_service import ProductService
from datetime import date, datetime

class CustomerService:
    def __init__(self, connector, user: User, product_service: ProductService):
        self.connector = connector
        self.user = user
        self.product_service = product_service

    def make_purchase(self, product_id, cc_number, amount):
        """
        Makes a purchase of a product_id with a cc_number from the current logged in user.

        Returns True if insertion successful.

        Returns False otherwise.
        """

        try:
            self.connector.cursor.execute(
                    "INSERT INTO purchases (customer_username, product_id, cc_number, amount) VALUES (%s, %s, %s, %s)", 
                    (self.user.username, product_id, cc_number, amount))
            self.product_service.update_product_stock_transaction(product_id, amount)
            # This transaction does NOT COMMIT until the product stock is updated afterwards.
            self.connector.db.commit()
            return True
        except Exception as e:
            return False

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
