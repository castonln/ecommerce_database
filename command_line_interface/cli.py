import os
import questionary
from product_service import ProductService
from customer_service import CustomerService
from datetime import datetime
from typing import Optional, Tuple, Callable

class Command_Line_Interface:
    def __init__(self, user, product_service: ProductService, customer_service: CustomerService):
        self.user = user
        self.product_service = product_service
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
            choices=["Staff", "Customer",
                     questionary.Choice(
                         title=[("fg:#DB0000 bold", "Exit")],
                         value="Exit",
                     )]
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
            "Staff": ["View Products", "Add Product", questionary.Choice(
                title=[("fg:#DB0000 bold", "Sign Out")],
                value="Sign Out",
            )],
            "Customer": ["View Products", "Add Card", questionary.Choice(
                title=[("fg:#DB0000 bold", "Sign Out")],
                value="Sign Out",
            )],
        }

        answer = questionary.select(
            "Select an option",
            choices=options[self.user.role]
        ).ask()

        action = {
            "View Products": self.view_products,
            "Add Product": self.add_product,
            "Add Card": self.add_card,
            "Sign Out": self.sign_out,
        }.get(answer)

        action()

    def view_products(self) -> None:
        """
        Show all products in the database and allow a user to select one.
        """

        self.clear_screen()

        def view_product(product):
            """
            View options for a particular product
            """

            self.clear_screen()

            (_, _, title, price) = product
            print(f"\033[95m\033[1m {title} - ${price}\033[0m")

            options = {
                "Staff": ["Edit Product",
                          "Delete Product",
                          questionary.Choice(
                              title=[("fg:#DB0000 bold", "<- Go back")],
                              value="__back__"
                          )],
                "Customer": ["Make Purchase",
                             questionary.Choice(
                                 title=[("fg:#DB0000 bold", "<- Go back")],
                                 value="__back__",
                             )],
            }

            answer = questionary.select(
                "Select an option",
                choices=options[self.user.role]
            ).ask()

            if answer == "__back__":
                self.view_products()
            else:
                action = {
                    "Edit Product": self.edit_product,
                    "Delete Product": self.delete_product,
                    "Make Purchase": self.make_purchase,
                }.get(answer)

                action(product)

        products = self.product_service.get_all_products()

        if not products:
            print("No products available.")
            questionary.press_any_key_to_continue().ask()
            return

        name_width = 35
        stock_width = 8
        price_width = 10

        choices = [
            questionary.Choice(
                title=(
                    f"{prod[2]:<{name_width}}"
                    f"{str(prod[1]):<{stock_width}}"
                    f"{'$' + format(prod[3], '.2f'):<{price_width}}"
                ),
                value=prod
            )
            for prod in products
        ]

        choices.append(questionary.Choice(
            title=[("fg:#DB0000 bold", "<- Go back")],
            value="__back__",
        ))

        selected_product = questionary.select(
            "Select a product:",
            choices=choices
        ).ask()

        if selected_product == "__back__":
            return

        view_product(selected_product)

    def _product_edit_loop(self, product: Tuple[int, int, str, float], confirm: Callable[[Tuple[Optional[int], int, str, float]], None]):
        """
        Loop template for editing or adding a product.

        Takes a product (product_id, stock, title, price) and a function for adding or editing.
        """

        (product_id, stock, title, price) = product

        while True:
            self.clear_screen()
            print(f"\033[95m\033[1m{title} - ${price} - ({stock})\033[0m")

            answer = questionary.select(
                "Select an option to edit: ",
                choices=[
                    "Title",
                    "Stock",
                    questionary.Choice(
                        title="Price\n",
                        value="Price",
                    ),
                    questionary.Choice(
                        title=[("fg:#00DB15 bold", "Confirm ->")],
                        value="__confirm__",
                    ),
                    questionary.Choice(
                        title=[("fg:#DB0000 bold", "<- Cancel")],
                        value="__cancel__",
                    ),
                ]
            ).ask()

            def validate_price(text):
                if text is None:
                    return False
                try:
                    float(text)
                    return True
                except ValueError:
                    return False

            question = {
                "Title": questionary.text(
                    "Enter title: ",
                    validate=lambda text: True if len(
                        text) < 255 else "Titles cannot be longer than 255 characters"
                ),
                "Stock": questionary.text(
                    "Enter stock: ",
                    validate=lambda text: True if text.isdigit() else "Please enter a valid stock"
                ),
                "Price": questionary.text(
                    "Enter price: $",
                    validate=validate_price
                ),
            }.get(answer)

            if answer == "Title":
                title = question.ask()
            elif answer == "Stock":
                stock = question.ask()
            elif answer == "Price":
                price = question.ask()
            else:
                if answer == "__confirm__":
                    confirm((product_id, stock, title, price))
                break

    def add_product(self) -> None:
        """
        Add a new product by editing its stock, title, and price.
        """
        product = (None, 0, "New Product", 0.00)
        self._product_edit_loop(product, self.product_service.add_product)

        self.show_user_options()

    def edit_product(self, product) -> None:
        """
        Edit a product's stock, title, and / or price.
        """
        self._product_edit_loop(product, self.product_service.edit_product)

        self.view_products()

    def delete_product(self, product) -> None:
        (product_id, _, title, _) = product
        answer = questionary.confirm(f"Are you sure you want to delete {title}?").ask()

        if answer:
            self.product_service.delete_product(product_id)

    def make_purchase(self, product) -> None:
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
                validate=lambda text: True if len(
                    text) == 16 and text.isdigit() else "Please enter a valid card number"
            ),
            cc_name=questionary.text(
                "Name on card: ",
                validate=lambda text: True if len(
                    text) < 255 else "Name must be under 255 chars"
            ),
            exp_date=questionary.text(
                "Expiration date (YYYY-MM): ",
                validate=lambda text: True if validate_exp_date(
                    text) else "Enter a valid date (YYYY-MM)"
            ),
            csc=questionary.text(
                "CSC (3-digit security code): ",
                validate=lambda text: True if len(
                    text) == 3 and text.isdigit() else "Enter a valid CSC"
            )
        ).ask()

        response = self.customer_service.add_card(
            card_input["cc_number"],
            card_input["cc_name"],
            card_input["exp_date"],
            card_input["csc"]
        )

        if response:
            questionary.press_any_key_to_continue(
                f'Card added.\nPress any key to continue...').ask()
        else:
            questionary.press_any_key_to_continue(
                f'Error. Failed to add card.\nPress any key to continue...').ask()

    def loop(self) -> None:
        """
        Main loop for CLI interactions. Breaks when "Exit Program" is selected in the outermost loop.
        """

        while True:
            if not self.sign_in():
                break

            while self.user.signed_in:
                self.show_user_options()
