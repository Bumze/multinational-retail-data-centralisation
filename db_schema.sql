-----MIlestone 3, Task 1-------

ALTER TABLE orders_table 
	ALTER COLUMN date_uuid TYPE uuid USING date_uuid::uuid,
	ALTER COLUMN user_uuid TYPE uuid USING user_uuid::uuid,
	ALTER COLUMN card_number TYPE varchar(19),
	ALTER COLUMN store_code TYPE varchar(12),
	ALTER COLUMN product_code TYPE varchar(11),
	ALTER COLUMN product_quantity TYPE smallint;

-----MIlestone 3, Task 2-------

ALTER TABLE dim_users 
ALTER COLUMN first_name TYPE varchar(255),
ALTER COLUMN last_name TYPE varchar(255),
ALTER COLUMN date_of_birth TYPE DATE,
ALTER COLUMN country_code TYPE varchar(2),
ALTER COLUMN user_uuid TYPE uuid USING user_uuid::uuid,
ALTER COLUMN join_date TYPE DATE;


-----MIlestone 3, Task 3-------Update store table to remove N/A from longitude column.

UPDATE dim_store_details
SET 
    longitude = NULL
WHERE 
   longitude = 'N/A'

select * from dim_store_details 
   where staff_numbers = '' ;

---------------------------------------------------------------------------------
Alter stores table to cast data type
------------------------------------------------------------------------------------

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


---------------------------------------------------------------------------------
Alter products table, add weight class and define conditions
--------------------------------------------------------------------------------
..Rename columns and update boolran conditions
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

---------------------------------------------------------------------------------
--Alter products table to cast data type
--------------------------------------------------------------------------------		

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


ALTER TABLE dim_date_times 
   ALTER COLUMN month TYPE VARCHAR (2),
   ALTER COLUMN year TYPE VARCHAR (4),
   ALTER COLUMN day TYPE VARCHAR (2),
   ALTER COLUMN time_period TYPE VARCHAR (10),
   ALTER COLUMN date_uuid TYPE uuid USING date_uuid::uuid;

---------------------------------------------------------------------------------
Alter cards table to cast data type
---------------------------------------------------------------------------------

ALTER TABLE dim_card_details 
   ALTER COLUMN  expiry_date TYPE VARCHAR (6),
   ALTER COLUMN  card_number TYPE VARCHAR (20),
   ALTER COLUMN date_payment_confirmed TYPE date;

---------------------------------------------------------------------------------
--Alter tables and define primary keys
---------------------------------------------------------------------------------

ALTER TABLE dim_date_times ADD PRIMARY KEY (date_uuid);
ALTER TABLE dim_users ADD PRIMARY KEY (user_uuid);
ALTER TABLE dim_card_details ADD PRIMARY KEY (card_number);
ALTER TABLE dim_store_details ADD PRIMARY KEY (store_code);
ALTER TABLE dim_products ADD PRIMARY KEY (product_code);


---------------------------------------------------------------------------------
--Alter tables and add foreign keys
---------------------------------------------------------------------------------

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
--error correction on product_code,, check formissing values

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


