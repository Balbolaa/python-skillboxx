
SELECT 
    customer.full_name,         -- The full name of the customer making the order
    manager.full_name,          -- The full name of the manager overseeing the order
    purchase_amount,            -- The total amount of the purchase in the order
    date                        -- The date when the order was made
FROM "order"                    -- From the "order" table which stores order data

-- Left Join the "customer" table based on the customer_id
-- Retrieves additional information from the customer table, specifically the full name
LEFT JOIN customer 
    ON "order".customer_id = customer.customer_id

-- Left Join the "manager" table based on the manager_id
-- Retrieves the manager's full name from the manager table
LEFT JOIN manager 
    ON "order".manager_id = manager.manager_id;
