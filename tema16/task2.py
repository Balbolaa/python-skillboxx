
pip install tabulate

import sqlite3
import tabulate

# The database name (SQLite)
DATABASE = 'hw.db'

# Function to select all orders with customer and manager details
def select_all_orders():
    # Prints the headers of the output
    print('order_no\tpurchase_amount\tdate\tcustomer_id\tmanager_id')
    
    # Establishes a connection to the database
    with sqlite3.Connection(DATABASE) as con:
        res = []  # To store the results
        cur = con.cursor()
        
        # SQL query to get all orders along with the customer and manager full names
        query = """SELECT customer.full_name, manager.full_name, purchase_amount, date FROM "order"
                    LEFT JOIN customer ON "order".customer_id = customer.customer_id
                    LEFT JOIN manager ON "order".manager_id = manager.manager_id"""
        
        # Executes the query
        orders = cur.execute(query)
        
        # Loop through the results and append each order details into the 'res' list
        for order in orders:
            output = []
            for column in order:
                # Handling None values
                if column is None:
                    output.append('None')
                    continue
                output.append(str(column))
            res.append(output)
        
        # Prints the formatted results using tabulate
        print(tabulate.tabulate(res))

# Function to select customers who haven't placed any orders
def select_customers_without_orders():
    # Establishes a connection to the database
    with sqlite3.Connection(DATABASE) as con:
        res = []  # To store the results
        cur = con.cursor()
        
        # SQL query to get all customers without any orders
        query = """SELECT customer.full_name FROM customer
                    WHERE NOT EXISTS(SELECT * FROM "order" 
                    WHERE "order".customer_id = customer.customer_id)"""
        
        # Executes the query
        customers = cur.execute(query)
        
        # Loop through the results and append each customer without an order
        for customer in customers:
            output = []
            for column in customer:
                # Handling None values
                if column is None:
                    output.append('None')
                    continue
                output.append(str(column))
            res.append(output)
        
        # Prints the formatted results using tabulate
        print(tabulate.tabulate(res))

# Function to select orders where the customer and manager are from different cities
def select_task3():
    # Establishes a connection to the database
    with sqlite3.Connection(DATABASE) as con:
        res = []  # To store the results
        cur = con.cursor()
        
        # SQL query to get all orders where the customer's and manager's city don't match
        query = """SELECT "order".order_no,manager.full_name, customer.full_name FROM "order"
                    LEFT JOIN manager ON manager.manager_id = "order".manager_id
                    LEFT JOIN customer ON customer.customer_id = "order".customer_id
                    WHERE NOT customer.city = manager.city"""
        
        # Executes the query
        customers = cur.execute(query)
        
        # Loop through the results and append the orders with different city manager and customer
        for customer in customers:
            output = []
            for column in customer:
                # Handling None values
                if column is None:
                    output.append('None')
                    continue
                output.append(str(column))
            res.append(output)
        
        # Prints the formatted results using tabulate
        print(tabulate.tabulate(res))

# Function to select orders where no manager is assigned
def select_task4():
    # Establishes a connection to the database
    with sqlite3.Connection(DATABASE) as con:
        res = []  # To store the results
        cur = con.cursor()
        
        # SQL query to get all orders with no assigned manager
        query = """SELECT order_no, customer.full_name FROM "order"
                    LEFT JOIN customer ON customer.customer_id = "order".customer_id
                    WHERE "order".manager_id IS NULL"""
        
        # Executes the query
        customers = cur.execute(query)
        
        # Loop through the results and append each order without a manager
        for customer in customers:
            output = []
            for column in customer:
                # Handling None values
                if column is None:
                    output.append('None')
                    continue
                output.append(str(column))
            res.append(output)
        
        # Prints the formatted results using tabulate
        print(tabulate.tabulate(res))

# Main function to control the flow of the script
def main():
    # Uncomment one of the following lines to run the desired query:

    # 1. Get all orders with customer and manager details
    # select_all_orders()

    # 2. Get customers who haven't placed any orders
    # select_customers_without_orders()

    # 3. Get orders where the customer and manager are from different cities
    # select_task3()

    # 4. Get orders where no manager is assigned
    select_task4()

# Script entry point
if __name__ == '__main__':
    main()
