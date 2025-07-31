import os
import questionary


class Command_Line_Interface:
    def __init__(self, user):
        self.user = user

    def clear_screen(self) -> None:
        os.system('cls' if os.name == 'nt' else 'clear')

    def sign_in(self) -> bool:
        """
        Contacts User instance to sign user in.

        Returns True for a sign in attempt.

        Returns False for a program exit.
        """
        self.clear_screen()

        sign_in_type = questionary.select(
            "Sign in as staff or customer?",
            choices=["Staff", "Customer", "Exit"]
        ).ask()

        if sign_in_type is None or sign_in_type == "Exit":
            return False

        username = questionary.text("Username: ").ask()
        password = questionary.password("Password: ").ask()

        sign_in_method = {
            "Staff": self.user.sign_in_staff,
            "Customer": self.user.sign_in_customer
        }.get(sign_in_type)

        if not sign_in_method:
            print("Invalid sign in selected.")
            return True

        if sign_in_method(username, password):
            print(f'Hello, {self.user.name}!')
            return True
        else:
            print("Invalid username / password.")
            questionary.press_any_key_to_continue(
                "Press any key to try again...").ask()
            return True

    def sign_out(self) -> None:
        answer = questionary.confirm(
            "Are you sure you want to sign out?").ask()

        if answer:
            self.user.sign_out()

        self.clear_screen()

    def show_user_options(self) -> None:
        """
        Show appropriate main menu options for signed in user depending on role.
        """
        self.clear_screen()

        options = {
            "Staff": ["View Products", "Sign Out"],
            "Customer": ["View Products", "Add Card", "Sign Out"],
        }

        answer = questionary.select(
            "Select an option",
            choices=options[self.user.role]
        ).ask()

        action = {
            "View Products": self.view_products,
            "Add card": self.add_card,
            "Sign Out": self.sign_out,
        }.get(answer)

        action()

    def view_products(self) -> None:
        pass

    def add_product(self) -> None:
        pass

    def edit_product(self) -> None:
        pass

    def delete_product(self) -> None:
        pass

    def make_purchase(self) -> None:
        pass

    def add_card(self) -> None:
        pass

    def loop(self) -> None:
        """
        Main loop for CLI interactions. Breaks when "Exit Program" is selected in the outermost loop.
        """
        while True:
            if not self.sign_in():
                break

            while self.user.signed_in:
                self.show_user_options()
