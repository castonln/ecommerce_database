USE ecommerce;

CREATE TABLE Customers (
	customer_username varchar(255) NOT NULL,
    customer_password varchar(255) NOT NULL,
    customer_name varchar(255) NOT NULL,
    PRIMARY KEY (customer_username)
);

INSERT INTO Customers(customer_username, customer_password, customer_name)
VALUES
('logan', 'password', 'Logan Castonguay'),
('shopper1', 'SHD&A_*', 'John Doe'),
('buyingit', 'cool123', 'Jane Doe'),
('summer2025', 'sunnyday45!', 'Emily Sun'),
('techlover', 'P@ssw0rd2025', 'Alex Smith'),
('discountqueen', 'shopTillDrop!', 'Riley Evans'),
('luxshopper', 'Ch@nel2025', 'Jordan Kim'),
('secureuser', 'Y*7gFvB!p9', 'Taylor Ray');

CREATE TABLE CreditCards (
	cc_number bigint NOT NULL,
    cc_name varchar(255) NOT NULL,
    exp_date date NOT NULL,
    csc smallint NOT NULL,
    customer_username varchar(255) NOT NULL,
    PRIMARY KEY (cc_number),
    FOREIGN KEY (customer_username) REFERENCES Customers(customer_username)
);

INSERT INTO CreditCards (cc_number, cc_name, exp_date, csc, customer_username)
VALUES
(4532756273945842, 'Logan Castonguay', '2027-05-01', 123, 'logan'),

(4716283749382738, 'John Doe', '2026-11-01', 456, 'shopper1'),
(4916123456789012, 'John Doe', '2029-07-01', 111, 'shopper1'),

(4485273728392011, 'Jane Doe', '2025-08-01', 789, 'buyingit'),
(4556737586899855, 'Jane Doe', '2026-04-01', 222, 'buyingit'),

(5196087452938475, 'Emily Sun', '2028-04-01', 321, 'summer2025'),

(6011000990139424, 'Alex Smith', '2029-01-01', 654, 'techlover'),
(3530111333300000, 'Alex Smith', '2026-06-01', 333, 'techlover'),

(378282246310005, 'Riley Evans', '2026-12-01', 987, 'discountqueen'),

(5555555555554444, 'Jordan Kim', '2027-06-01', 852, 'luxshopper'),
(5105105105105100, 'Jordan Kim', '2028-02-01', 444, 'luxshopper'),

(4111111111111111, 'Taylor Ray', '2026-03-01', 963, 'secureuser');

CREATE TABLE Products (
	product_id int NOT NULL AUTO_INCREMENT,
    stock int DEFAULT 0,
    title varchar(255) NOT NULL,
    price decimal(15,2) DEFAULT 0.00,
    PRIMARY KEY (product_id)
);

INSERT INTO Products (stock, title, price)
VALUES
(50, 'Wireless Mouse', 19.99),
(20, 'Mechanical Keyboard', 89.95),
(100, 'USB-C Charging Cable', 9.49),
(10, '27" 4K Monitor', 299.99),
(35, 'Bluetooth Headphones', 59.99),
(15, 'Gaming Chair', 199.99),
(80, 'Smartphone Stand', 12.99),
(25, 'Portable SSD 1TB', 129.99),
(60, 'Webcam 1080p', 39.99),
(5, 'Laptop - 16GB RAM, 512GB SSD', 899.00),
(100, 'Reusable Water Bottle', 14.99),
(40, 'Desk Lamp with USB Port', 27.50),
(75, 'Ergonomic Office Chair Cushion', 24.95),
(30, 'Noise-Cancelling Earbuds', 49.99),
(12, 'Wireless Router', 79.00);

CREATE TABLE Purchases (
	customer_username varchar(255) NOT NULL,
    product_id int NOT NULL,
    cc_number bigint NOT NULL,
    amount int NOT NULL,
    purchase_time timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (customer_username, product_id, purchase_time),
    FOREIGN KEY (customer_username) REFERENCES Customers(customer_username),
	FOREIGN KEY (product_id) REFERENCES Products(product_id),
    FOREIGN KEY (cc_number) REFERENCES CreditCards(cc_number)
);

INSERT INTO Purchases (customer_username, product_id, cc_number, amount, purchase_time)
VALUES
-- Logan buys a wireless mouse
('logan', 1, 4532756273945842, 1, '2025-07-28 14:15:00'),

-- shopper1 buys a keyboard and a webcam
('shopper1', 2, 4716283749382738, 1, '2025-07-29 10:05:00'),
('shopper1', 9, 4916123456789012, 2, '2025-07-29 11:22:00'),

-- buyingit buys a gaming chair
('buyingit', 6, 4556737586899855, 1, '2025-07-30 09:30:00'),

-- summer2025 buys 2 water bottles and 1 desk lamp
('summer2025', 11, 5196087452938475, 2, '2025-07-30 15:45:00'),
('summer2025', 12, 5196087452938475, 1, '2025-07-30 15:46:30'),

-- techlover buys a 1TB SSD and a laptop
('techlover', 8, 6011000990139424, 1, '2025-07-28 12:30:00'),
('techlover', 10, 3530111333300000, 1, '2025-07-29 13:00:00'),

-- discountqueen buys 3 smartphone stands
('discountqueen', 7, 378282246310005, 3, '2025-07-30 16:10:00'),

-- luxshopper buys earbuds and a monitor
('luxshopper', 4, 5555555555554444, 1, '2025-07-29 09:00:00'),
('luxshopper', 14, 5105105105105100, 2, '2025-07-29 09:15:00'),

-- secureuser buys 1 USB-C cable and a desk lamp
('secureuser', 3, 4111111111111111, 1, '2025-07-30 08:00:00'),
('secureuser', 12, 4111111111111111, 1, '2025-07-30 08:01:30');

CREATE TABLE Staff (
	staff_username varchar(255) NOT NULL,
    staff_password varchar(255) NOT NULL,
    staff_name varchar(255) NOT NULL,
    PRIMARY KEY (staff_username)
);

INSERT INTO Staff(staff_username, staff_password, staff_name)
VALUES
('theboss', 'urfired', 'Damien Eaton'),
('midmanager', 'password', 'Zuri Holly');
