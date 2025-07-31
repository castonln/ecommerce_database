from user import User
from connector import Connector
from cli import Command_Line_Interface

if __name__ == "__main__":
    connector = Connector()
    mycursor = connector.cursor
    user = User(mycursor)
    cli = Command_Line_Interface(user)

    cli.loop()
