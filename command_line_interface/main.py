from user import User
from connector import Connector
from cli import Command_Line_Interface
from product_service import ProductService
from customer_service import CustomerService

if __name__ == "__main__":
    connector = Connector()
    user = User(connector)
    product_service = ProductService(connector)
    customer_service = CustomerService(connector, user)

    cli = Command_Line_Interface(user, product_service, customer_service)

    cli.loop()
