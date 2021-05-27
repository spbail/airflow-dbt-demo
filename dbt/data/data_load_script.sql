-- Simple script to load the data to a postgres DB instead of using dbt seed
-- which isn't optimized for large data as per their docs
-- This expects the CSV files to be present in the path below. They can be generated using the notebook code.
-- The customers table is pretty quick, the other two tables take a few minutes to load.

CREATE TABLE raw_customers (
        id DECIMAL,
        first_name VARCHAR,
        last_name VARCHAR
);

\COPY raw_customers from '/Users/sam/code/sample_data/jaffle_shop_data_large/raw_customers.csv' CSV HEADER;

CREATE TABLE raw_orders (
        id DECIMAL,
        user_id DECIMAL,
        order_date DATE,
        status VARCHAR
);

\COPY raw_orders from '/Users/sam/code/sample_data/jaffle_shop_data_large/raw_orders.csv' CSV HEADER;

CREATE TABLE raw_payments (
        id DECIMAL,
        order_id DECIMAL,
        payment_method VARCHAR,
        amount DECIMAL
);

\COPY raw_payments from '/Users/sam/code/sample_data/jaffle_shop_data_large/raw_payments.csv' CSV HEADER;
