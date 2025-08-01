from typing import Optional, Tuple
from datetime import date


class User:
    """
    Logic for the current user of the CLI.

    Attributes are None if signed out.
    """

    def __init__(self, connector):
        self.username = None
        self.password = None
        self.name = None
        self.role = None
        self.cards = []

        self.signed_in = False

        self.connector = connector

    def _sign_in(self, username: str, password: str, query: str, role: str) -> Optional[Tuple[str, str, str]]:
        """
        Signs in a customer or a staff member.

        Returns signed in user's data or None for a failed sign in.
        """

        self.connector.cursor.execute(query, (username, password))
        user_data = self.connector.cursor.fetchone()

        if user_data:
            self.role = role
            (self.username, self.password, self.name) = user_data
            self.signed_in = True
            return user_data

        return None

    def sign_in_customer(self, username, password) -> Optional[Tuple[str, str, str]]:
        """
        Sends query to _sign_in to sign in a customer user.
        """

        if self._sign_in(
            username,
            password,
            f'SELECT * FROM customers WHERE customer_username= %s AND customer_password= %s',
            "Customer"
        ):
            self.connector.cursor.execute(
                f'SELECT * FROM creditcards WHERE customer_username= %s', (username,))
            cards = self.connector.cursor.fetchall()
            for card in cards:
                (cc_number, cc_name, exp_date, csc, customer_username) = card
                self.add_card(cc_number, cc_name, exp_date, csc, customer_username)
            return True

    def sign_in_staff(self, username, password) -> Optional[Tuple[str, str, str]]:
        """
        Sends query to _sign_in to sign in a staff user.
        """

        return self._sign_in(
            username,
            password,
            f'SELECT * FROM staff WHERE staff_username= %s AND staff_password= %s',
            "Staff"
        )

    def sign_out(self) -> None:
        """
        Signs out signed in user.
        """

        self.username, self.password, self.name, self.role, self.cards = None, None, None, None, []
        self.signed_in = False
