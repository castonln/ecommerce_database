from connector import Connector
from typing import List, Tuple

class ProductService:
    def __init__(self, connector: Connector):
        self.connector = connector

    def get_all_products(self) -> List[Tuple[int, int, str, float]]:
        self.connector.cursor.execute("SELECT * FROM products")
        return self.connector.cursor.fetchall()
    
    def add_product(self, product: Tuple[int, int, str, float]) -> bool:
        """
        Adds a new product to the database.

        Returns True if insertion was successful.

        Returns False otherwise.
        """
        try:
            (_, stock, title, price) = product
            self.connector.cursor.execute(
                    "INSERT INTO products (stock, title, price) VALUES (%s, %s, %s)", (stock, title, price))
            self.connector.db.commit()
            return True
        except Exception as e:
            return False

    def edit_product(self, product: Tuple[int, int, str, float]) -> bool:
        """
        Edits an existing product in the database.

        Returns True if update was successful.

        Returns False otherwise.
        """
        try:
            (product_id, stock, title, price) = product
            self.connector.cursor.execute(
                    "UPDATE products SET title = %s, stock = %s, price = %s WHERE product_id = %s", (title, stock, price, product_id))
            self.connector.db.commit()
            return True
        except Exception as e:
            return False

    def delete_product(self, product_id: int) -> bool:
        """
        Deletes an exisiting product from the database.

        Returns True if deletion was successful.

        Returns False otherwise.
        """
        try:
            self.connector.cursor.execute(
                    "DELETE FROM products WHERE product_id = %s", (product_id,))
            self.connector.db.commit()
            return True
        except Exception as e:
            return False

    def update_product_stock_transaction(self, product_id: int, amount: int):
        """
        Update a product's stock after a transaction has gone through (minuses its stock by the amount of units purchased).
        
        Returns if insertion was successful.

        Returns an Error otherwise.
        """
        self.connector.cursor.execute(
                "UPDATE products SET stock = stock - %s WHERE product_id = %s", (amount, product_id))
        self.connector.db.commit()