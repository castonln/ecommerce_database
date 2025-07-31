USE ecommerce;
    
-- "Show the names of customers along with the names of the products they purchased where product price > $100."
SELECT customers.customer_name, products.title
FROM purchases
JOIN products ON purchases.product_id = products.product_id
JOIN customers ON purchases.customer_username = customers.customer_username
WHERE products.price > 100;

