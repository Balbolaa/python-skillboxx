import random
import sqlite3

# SQL script to create the database schema (tables for customer, manager, and order)
CREATE_TABLES = """
-- Drop the customer table if it already exists
DROP TABLE IF EXISTS 'customer';
-- Create a new customer table with an auto-incrementing customer_id, full_name, city, and a foreign key to manager
CREATE TABLE 'customer' (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name VARCHAR(50) NOT NULL,
    city VARCHAR(50) NOT NULL,
    manager_id INTEGER REFERENCES manager(manager_id)
);

-- Drop the manager table if it already exists
DROP TABLE IF EXISTS 'manager';
-- Create a new manager table with an auto-incrementing manager_id, full_name, and city
CREATE TABLE 'manager' (
    manager_id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name VARCHAR(50) NOT NULL,
    city VARCHAR(50) NOT NULL
);

-- Drop the order table if it already exists
DROP TABLE IF EXISTS 'order';
-- Create a new order table with an auto-incrementing order_no, purchase_amount, date,
-- and foreign keys linking to customer and manager
CREATE TABLE 'order' (
    order_no INTEGER PRIMARY KEY AUTOINCREMENT,
    purchase_amount INTEGER NOT NULL,
    date VARCHAR(255) NOT NULL,
    customer_id INTEGER REFERENCES customer(customer_id),
    manager_id INTEGER REFERENCES manager(manager_id)
);
"""

# Function to generate a random date in the format "2020-MM-DD"
def _get_random_date() -> str:
    day = random.randint(1, 30)    # Random day between 1 and 30
    month = random.randint(1, 12)  # Random month between 1 and 12
    return f"2020-{month}-{day}"   # Return date formatted as "2020-MM-DD"

# List of common family names
families = """Иванов
Васильев
Петров
Смирнов
Михайлов
Фёдоров
Соколов
Яковлев
Попов
Андреев
Алексеев
Александров
Лебедев
Григорьев
Степанов
Семёнов
Павлов
Богданов
Николаев
Дмитриев
Егоров
Волков
Кузнецов
Никитин
Соловьёв""".split()

# Russian alphabet letters for generating random initials
name_letters = "абвгдежзиклмнопрстуфхцчшщэюя".upper()

# Function to generate a random full name in the format "Lastname X.Y."
def _get_random_full_name() -> str:
    is_male = random.choice((True, False))  # Randomly choose if the name is male or female
    family_name = random.choice(families)   # Choose a random family name
    if not is_male:                         # Add "а" to the family name for female
        family_name += "а"

    # Generate random initials for the first and middle names
    first_letter, last_letter = random.choice(name_letters), random.choice(name_letters)

    return f"{family_name} {first_letter}.{last_letter}."  # Return the full name as "Lastname X.Y."

# List of cities for assigning to customers and managers
cities = """
Москва
Омск
Барнаул
Ярославль
Краснодар
Севастополь
Ялта
Сочи
Ижевск
Иркутск
Мурманск
Санкт-Петербург
Архангельск
""".split()

# Function to prepare (initialize) the tables and populate them with random data
def prepare_tables():
    if __name__ == "__main__":  # Ensure that the script runs only if executed directly
        with sqlite3.connect("hw.db") as conn:  # Connect to the SQLite database
            cursor = conn.cursor()
            cursor.executescript(CREATE_TABLES)  # Execute the script to create the tables
            conn.commit()

            # Generate 30 random managers with names and cities
            managers = [
                (_get_random_full_name(), random.choice(cities))
                for _ in range(30)
            ]
            # Insert the managers into the 'manager' table
            conn.executemany(
                """
                    INSERT INTO 'manager'(full_name, city)
                    VALUES (?, ?)
                """,
                managers
            )

            # Generate 500 random customers with names, cities, and random manager assignments
            customers = [
                (
                    _get_random_full_name(),   # Random full name
                    random.choice(cities),     # Random city
                    random.choice([i for i in range(1, 21)] + [None])  # Assign a manager randomly or None
                )
                for _ in range(500)
            ]
            # Insert the customers into the 'customer' table
            conn.executemany(
                """
                    INSERT INTO 'customer'(full_name, city, manager_id)
                    VALUES(?, ?, ?)
                """,
                customers
            )

            # Generate 10,000 random orders with purchase amounts, dates, customer IDs, and manager IDs
            orders = [
                (
                    random.randint(10, 1000),  # Random purchase amount between 10 and 1000
                    _get_random_date(),        # Random date
                    random.randint(1, 100),    # Random customer ID
                    random.choice([i for i in range(1, 21)] + [None])  # Random manager assignment or None
                )
                for _ in range(10000)
            ]

            # Insert the orders into the 'order' table
            conn.executemany(
                """
                    INSERT INTO 'order'(purchase_amount, date, customer_id, manager_id)
                    VALUES(?, ?, ?, ?)
                """,
                orders
            )

# Run the table preparation when the script is executed
if __name__ == '__main__':
    prepare_tables()
