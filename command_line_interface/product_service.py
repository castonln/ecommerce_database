class ProductService:
    def __init__(self, connector):
        self.connector = connector

    def get_all_products(self):
        self.connector.cursor.execute("SELECT * FROM products")
        return self.connector.cursor.fetchall()
    
    def add_product(self, product):
        (_, stock, title, price) = product
        self.connector.cursor.execute(
                "INSERT INTO products (stock, title, price) VALUES (%s, %s, %s)", (stock, title, price))
        self.connector.db.commit()

    def edit_product(self, product):
        (product_id, stock, title, price) = product
        self.connector.cursor.execute(
                "UPDATE products SET title = %s, stock = %s, price = %s WHERE product_id = %s", (title, stock, price, product_id))
        self.connector.db.commit()

    def delete_product(self, product_id):
        self.connector.cursor.execute(
                "DELETE FROM products WHERE product_id = %s", (product_id,))
        self.connector.db.commit()