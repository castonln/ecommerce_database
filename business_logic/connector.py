import mysql.connector


class Connector:
    """
    Connects to the database.
    """
    def __init__(self):
        self.db = mysql.connector.connect(
            host="localhost",
            user="logan",
            password="password",
            database="ecommerce"
        )
        self.cursor = self.db.cursor()
