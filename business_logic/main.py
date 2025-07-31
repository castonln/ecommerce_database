import questionary
from user import User
from connector import Connector

def sign_in():
    answers = questionary.form(
        sign_in_type=questionary.select(
            "Sign in as staff or customer?",
            choices=["Staff", "Customer"]
        ),
        username=questionary.text(
            "Username: "
        ),
        password=questionary.password(
            "Password: "
        )
    ).ask()

    sign_in_method = {
        "Staff": user.sign_in_staff,
        "Customer": user.sign_in_customer
    }.get(answers["sign_in_type"])

    if not sign_in_method:
        return False
    
    return sign_in_method(answers["username"], answers["password"])

if __name__ == "__main__":
    connector = Connector()
    mycursor = connector.cursor
    print(mycursor)
    user = User(mycursor)

    while not user.username:
        sign_in()
