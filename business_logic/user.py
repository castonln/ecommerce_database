from typing import Optional, Tuple

class User:
    """
    Logic for the current user of the CLI.

    Attributes are None if signed out.
    """
    def __init__(self, mycursor):
        self.username = None
        self.password = None
        self.name = None
        self.role = None
        self.cards = []

        self.signed_in = False

        self.mycursor = mycursor

    def _sign_in(self, username: str, password: str, query: str, role: str) -> Optional[Tuple[str, str, str]]:
        """
        Signs in a customer or a staff member.

        Returns signed in user's data or None for a failed sign in.
        """
        self.mycursor.execute(query, (username, password))
        user_data = self.mycursor.fetchone()

        if user_data:
            self.role = role
            (self.username, self.password, self.name) = user_data
            self.signed_in = True
            return user_data

        return None

    def sign_in_customer(self, username, password) -> Optional[Tuple[str, str, str]]:
        if self._sign_in(
            username,
            password,
            f'SELECT * FROM customers WHERE customer_username= %s AND customer_password= %s',
            "Customer"
        ):
            self.mycursor.execute(f'SELECT * FROM creditcards WHERE customer_username= %s', (username,))
            cards = self.mycursor.fetchall()
            for card in cards:
                self.add_card(card)
            return True

    def sign_in_staff(self, username, password) -> Optional[Tuple[str, str, str]]:
        return self._sign_in(
            username,
            password,
            f'SELECT * FROM staff WHERE staff_username= %s AND staff_password= %s',
            "Staff"
        )

    def sign_out(self) -> None:
        self.username, self.password, self.name, self.role, self.cards = None, None, None, None, []
        self.signed_in = False

    def add_card(self, card) -> None:
        #[(4532756273945842, 'Logan Castonguay', datetime.date(2027, 5, 1), 123, 'logan')]
        self.cards.append(card)