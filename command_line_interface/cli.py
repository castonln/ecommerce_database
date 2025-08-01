import os
import questionary
from product_service import ProductService
from staff_service import StaffService
from customer_service import CustomerService
from datetime import datetime


class Command_Line_Interface:
    def __init__(self, user, product_service: ProductService, staff_service: StaffService, customer_service: CustomerService):
        self.user = user
        self.product_service = product_service
        self.staff_service = staff_service
        self.customer_service = customer_service

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
            "Add Card": self.add_card,
            "Sign Out": self.sign_out,
        }.get(answer)

        action()

    def view_products(self) -> None:
        """
        Show all products in the database and allow a user to select one.
        """

        def view_product(product_id):
            pass

        products = self.product_service.get_all_products()

        if not products:
            print("No products available.")
            questionary.press_any_key_to_continue().ask()
            return

        name_width = 35
        stock_width = 8
        price_width = 10

        # Products
        choices = [
            questionary.Choice(
                title=(
                    f"{prod[2]:<{name_width}}"
                    f"{str(prod[1]):<{stock_width}}"
                    f"{'$' + format(prod[3], '.2f'):<{price_width}}"
                ),
                value=prod[0]  # product_id
            )
            for prod in products
        ]

        choices.append(questionary.Choice(
            title=[("fg:#009DFF bold", "<- Go back")],
            value="__back__",
        ))

        selected_id = questionary.select(
            "Select a product:",
            choices=choices
        ).ask()

        if selected_id == "__back__":
            return

        view_product(selected_id)

    def add_product(self) -> None:
        pass

    def edit_product(self) -> None:
        pass

    def delete_product(self) -> None:
        pass

    def make_purchase(self) -> None:
        pass

    def add_card(self) -> None:       
        def validate_exp_date(text):
            try:
                datetime.strptime(text, "%Y-%m")
                return True
            except ValueError:
                return False

        card_input = questionary.form(
            cc_number=questionary.text(
                "Card number: ",
                validate=lambda text: True if len(text) == 16 and text.isdigit() else "Please enter a valid card number"
            ),
            cc_name=questionary.text(
                "Name on card: ",
                validate=lambda text: True if len(text) < 255 else "Name must be under 255 chars"
            ),
            exp_date=questionary.text(
                "Expiration date (YYYY-MM): ",
                validate=lambda text: True if validate_exp_date(text) else "Enter a valid date (YYYY-MM)"
            ),
            csc=questionary.text(
                "CSC (3-digit security code): ",
                validate=lambda text: True if len(text) == 3 and text.isdigit() else "Enter a valid CSC"
            )
        ).ask()

        response = self.customer_service.add_card(
            card_input["cc_number"], 
            card_input["cc_name"], 
            card_input["exp_date"], 
            card_input["csc"]
        )

        if response:
            questionary.press_any_key_to_continue(f'Card added.\nPress any key to continue...').ask()
        else:
            questionary.press_any_key_to_continue(f'Error. Failed to add card.\nPress any key to continue...').ask()

    def loop(self) -> None:
        """
        Main loop for CLI interactions. Breaks when "Exit Program" is selected in the outermost loop.
        """

        while True:
            if not self.sign_in():
                break

            while self.user.signed_in:
                self.show_user_options()
