class ProductService:
    def __init__(self, connector):
        self.connector = connector

    def get_all_products(self):
        self.connector.cursor.execute("SELECT * FROM products")
        return self.connector.cursor.fetchall()