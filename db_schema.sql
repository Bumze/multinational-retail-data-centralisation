--Milestone 3, Task 1--Change the data types in the orders table

ALTER TABLE orders_table 
	ALTER COLUMN date_uuid TYPE uuid USING date_uuid::uuid,
	ALTER COLUMN user_uuid TYPE uuid USING user_uuid::uuid,
	ALTER COLUMN card_number TYPE varchar(19),
	ALTER COLUMN store_code TYPE varchar(12),
	ALTER COLUMN product_code TYPE varchar(11),
	ALTER COLUMN product_quantity TYPE smallint;

--Milestone 3, Task 2--Change the data types in the users table 

ALTER TABLE dim_users 
ALTER COLUMN first_name TYPE varchar(255),
ALTER COLUMN last_name TYPE varchar(255),
ALTER COLUMN date_of_birth TYPE DATE,
ALTER COLUMN country_code TYPE varchar(2),
ALTER COLUMN user_uuid TYPE uuid USING user_uuid::uuid,
ALTER COLUMN join_date TYPE DATE;

--Milestone 3,  Task 3--Update store table to remove N/A from longitude column.

UPDATE dim_store_details
SET 
    longitude = NULL
WHERE 
   longitude = 'N/A'

select * from dim_store_details 
   where staff_numbers = '' ;

--Milestone 3, Task 3--Alter stores table to cast data type

ALTER TABLE dim_store_details 
    ALTER COLUMN longitude TYPE FLOAT USING longitude::float,
    ALTER COLUMN locality TYPE VARCHAR (255),
    ALTER COLUMN store_code TYPE VARCHAR(12),
    ALTER COLUMN staff_numbers TYPE smallint USING staff_numbers::smallint,
    ALTER COLUMN opening_date TYPE DATE,
    ALTER COLUMN store_type TYPE VARCHAR (255),
    ALTER COLUMN latitude TYPE FLOAT using latitude::FLOAT,
    ALTER COLUMN country_code TYPE VARCHAR (2),
    ALTER COLUMN continent TYPE VARCHAR (255);

--Milestone 3, Task 4--Alter products table, add weight class and define conditions for delivery team

..Rename columns and update boolean conditions
ALTER TABLE dim_products 
   ADD COLUMN weight_class VARCHAR (20)
   RENAME removed TO still_available
   RENAME COLUMN "EAN" TO EAN

   UPDATE dim_products 
      SET weight_class =
	CASE
		WHEN weight < 2 THEN 'Light'
		WHEN (weight >= 2  and weight < 40) THEN'Mid_Sized'
		WHEN (weight >= 40  and weight < 140) THEN 'Heavy'
		WHEN weight >= 140 THEN 'Truck_Required'
	END;

--Milestone 3, Task 5--Alter products table to cast data type	

ALTER TABLE dim_products 
   ALTER COLUMN product_price TYPE float USING product_price::float,
   ALTER COLUMN weight TYPE float USING weight::float,
   ALTER COLUMN weight TYPE float USING weight::float,
   ALTER COLUMN still_available 
	SET DATA TYPE BOOLEAN
	USING CASE
		WHEN still_available = 'Still_avaliable' THEN TRUE
		WHEN still_available = 'Removed' THEN FALSE
		ELSE NULL
	END,

   ALTER COLUMN EAN TYPE VARCHAR (18), 
   ALTER COLUMN product_code TYPE VARCHAR (12),
   ALTER COLUMN date_added TYPE date,
   ALTER COLUMN uuid TYPE uuid USING uuid::uuid,
   ALTER COLUMN weight_class TYPE VARCHAR (14);

--Milestone 3, Task 6--Alter cards table to cast data type

ALTER TABLE dim_date_times 
   ALTER COLUMN month TYPE VARCHAR (2),
   ALTER COLUMN year TYPE VARCHAR (4),
   ALTER COLUMN day TYPE VARCHAR (2),
   ALTER COLUMN time_period TYPE VARCHAR (10),
   ALTER COLUMN date_uuid TYPE uuid USING date_uuid::uuid;

--Milestone 3, Task 7--Alter cards table to cast data type

ALTER TABLE dim_card_details 
   ALTER COLUMN  expiry_date TYPE VARCHAR (6),
   ALTER COLUMN  card_number TYPE VARCHAR (20),
   ALTER COLUMN date_payment_confirmed TYPE date;

--Milestone 3, Task 8--Alter tables and define primary keys

ALTER TABLE dim_date_times ADD PRIMARY KEY (date_uuid);
ALTER TABLE dim_users ADD PRIMARY KEY (user_uuid);
ALTER TABLE dim_card_details ADD PRIMARY KEY (card_number);
ALTER TABLE dim_store_details ADD PRIMARY KEY (store_code);
ALTER TABLE dim_products ADD PRIMARY KEY (product_code);

--Milestone 3, Task 9--Alter tables and add foreign keys


ALTER TABLE orders_table 
    ADD FOREIGN KEY (date_uuid) 
        REFERENCES dim_date_times(date_uuid);

ALTER TABLE orders_table 
    ADD FOREIGN KEY (user_uuid) 
        REFERENCES dim_users(user_uuid);

ALTER TABLE orders_table 
    ADD FOREIGN KEY (card_number) 
        REFERENCES dim_card_details (card_number);

ALTER TABLE orders_table 
    ADD FOREIGN KEY (store_code) 
        REFERENCES dim_store_det

ALTER TABLE orders_table 
    ADD FOREIGN KEY (product_code) 
        REFERENCES dim_products(product_code);
--error correction on product_code, check for missing values

SELECT *
FROM orders_table 
LEFT JOIN dim_products
	ON orders_table.product_code = dim_products.product_code
	WHERE dim_products.product_code IS NULL;
	
--insert missing values on orders table

INSERT INTO dim_products
SELECT DISTINCT orders_table.product_code 
FROM orders_table
WHERE orders_table.product_code NOT IN 
	(SELECT dim_products.product_code
	FROM dim_products);
	
-- attempt adding foreign key again

ALTER TABLE orders_table 
   ADD CONSTRAINT FK_product_code 
	   FOREIGN KEY (product_code)
		   REFERENCES dim_products(product_code);	


--Milestone 4- Response to Operations team 
--Task 1-- How many stores does the business have and in which countries?

SELECT country_code, 
       COUNT(*) AS total_no_stores
FROM dim_store_details
GROUP BY country_code
ORDER BY total_no_stores DESC
LIMIT 3;

--Milestone 4, Task 2-- Which locations currently have the most stores?

SELECT locality, COUNT(*) AS total_no_stores
FROM dim_store_details
GROUP BY locality
ORDER BY total_no_stores DESC
LIMIT 7;
 
--Milestone 4, Task 3-- find out which months typically have the most sales?

SELECT SUM(product_price * product_quantity) as total_sales, month
FROM dim_date_times as d
JOIN orders_table as o
   ON d.date_uuid = o.date_uuid
JOIN dim_products as p
   ON o.product_code = p.product_code
GROUP BY month 
ORDER BY total_sales DESC;

---Milestone 4, Task 4--how many sales are happening online vs offline.

SELECT store_type AS location,
	   COUNT(o.*) AS total_sales,    
	   SUM(product_quantity) AS product_quantity_count
FROM orders_table AS o
JOIN dim_products AS p
   ON o.product_code = p.product_code
JOIN dim_store_details AS s
	ON o.store_code = s.store_code
GROUP BY 1
ORDER BY 3 DESC;


--Milestone 4, Task 5--the total and percentage of sales coming from each of the different store types.

SELECT store_type AS location,
	    ROUND(SUM(product_price * product_quantity)::numeric, 2) as total_sales,
       ROUND((100.0 * SUM(product_price * product_quantity)::numeric / SUM(SUM(product_price * product_quantity)::numeric) OVER()) ,2) AS Percentage_store_sale
FROM orders_table AS o
JOIN dim_products AS p
   ON o.product_code = p.product_code
JOIN dim_store_details AS s
	ON o.store_code = s.store_code
GROUP BY 1
ORDER BY 2 DESC;

--Milestone 4, Task 6--Which months in which years have had the most sales historically.

SELECT SUM(product_price * product_quantity) as total_sales, month, year
FROM dim_date_times as d
JOIN orders_table as o
   ON d.date_uuid = o.date_uuid
JOIN dim_products as p
   ON o.product_code = p.product_code
GROUP BY month, year
ORDER BY total_sales DESC
LIMIT 10;

--Milestone 4, Task 7--What is our staff headcount?

SELECT SUM(staff_numbers::numeric) as total_staff, 
       country_code AS country
FROM dim_store_details
GROUP BY country
ORDER BY total_staff DESC;

--Milestone 4, Task 8-- Determine which type of store is generating the most sales in Germany.

SELECT ROUND((SUM(product_price * product_quantity)::numeric),2) as total_sales,
       store_type,
       country_code
FROM orders_table AS o
JOIN dim_products AS p
   ON o.product_code = p.product_code
JOIN dim_store_details AS s
	ON o.store_code = s.store_code
Where country_code = 'DE'
GROUP BY 2,3
ORDER BY 1 ASC;

/* Milestone 4, Task 9 -- Determine the average time taken between each sale grouped by year.

The task is interpreted as finding the average of the time difference beteween each sale over 
the years. Average(sale timestamp - next sale timestamp) computed over the years and ordered by 
the average timestamp descending.

The solution uses three CTEs to concatenate given time details to form a timestamp. 
SQL window function LEAD() returns the next record in the timestamp set in the next_times column.
The average times column is derived with the AVG() function used on the difference between sale 
timestamps. FInally the required parameters are extracted from the average times. */


WITH date_times AS (
               SELECT 
				   year,
			  	   month, 
				   day, 
	            timestamp,
				   TO_TIMESTAMP(CONCAT(year, '/', month, '/', day, '/', timestamp), 'YYYY/MM/DD/HH24:MI:ss') as times
				   FROM dim_date_times d
						 JOIN orders_table o
						 ON d.date_uuid = o.date_uuid
						 JOIN dim_store_details s
						 ON o.store_code = s.store_code
				   ORDER BY times DESC),		   	
next_times AS(
		 SELECT year, 
		 times,
		 LEAD(times) OVER(ORDER BY times DESC) AS next_times
		 FROM date_times),
		 
avg_times AS(
		SELECT year,
		(AVG(times - next_times)) AS avg_times	
		FROM next_times
		GROUP BY year
		ORDER BY avg_times DESC)
	
SELECT year,
		CONCAT('"Hours": ', (EXTRACT(HOUR FROM avg_times)),','
		' "minutes": ', (EXTRACT(MINUTE FROM avg_times)),','
	    ' "seconds": ', ROUND((EXTRACT(SECOND FROM avg_times)), 0),','
	    ' "milliseconds": ', (EXTRACT(MILLISECOND FROM avg_times))-ROUND((EXTRACT(SECOND FROM avg_times)), 0)*1000)
	as actual_time_taken
FROM avg_times
GROUP BY year, avg_times
ORDER BY avg_times DESC
LIMIT 5;  
					