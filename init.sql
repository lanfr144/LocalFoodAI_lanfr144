-- ---------------------------------------------------------
-- Initial Database and User Setup (Run as MySQL Root)
-- ---------------------------------------------------------
CREATE DATABASE IF NOT EXISTS food_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 1. Create the Owner User
-- Has full rights and can grant privileges to others.
CREATE USER IF NOT EXISTS 'db_owner'@'%' IDENTIFIED BY 'owner_pass';
GRANT ALL PRIVILEGES ON food_db.* TO 'db_owner'@'%' WITH GRANT OPTION;

-- 2. Create the Reader User
-- Has only connect and read permissions.
CREATE USER IF NOT EXISTS 'db_reader'@'%' IDENTIFIED BY 'reader_pass';
GRANT USAGE ON *.* TO 'db_reader'@'%';

-- 3. Create the Loader User
-- Has connect and data manipulation permissions to load files.
CREATE USER IF NOT EXISTS 'db_loader'@'%' IDENTIFIED BY 'loader_pass';
GRANT USAGE ON *.* TO 'db_loader'@'%';
GRANT FILE ON *.* TO 'db_loader'@'%'; -- Essential for LOAD DATA INFILE from any directory

-- 4. Create the App Auth User
-- Segregation of Duties: Handles only users table for web application routing.
CREATE USER IF NOT EXISTS 'db_app_auth'@'%' IDENTIFIED BY 'app_auth_placeholder_pass';
-- Note: Replace 'app_auth_placeholder_pass' later outside this script.
GRANT USAGE ON *.* TO 'db_app_auth'@'%';

FLUSH PRIVILEGES;


-- ---------------------------------------------------------
-- Table Creation & Grants (Logically executed by db_owner)
-- ---------------------------------------------------------
USE food_db;

-- NOTE: The syntax you provided (`read_csv_auto`) is specific to DuckDB!
-- MySQL does NOT support `read_csv_auto()` to dynamically create tables from CSV.
-- In MySQL, you MUST define the table schema first, and then use LOAD DATA INFILE.
-- Here is the MySQL equivalent process:

-- Step A.1: Create Web Users Table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

GRANT SELECT, INSERT, UPDATE ON food_db.users TO 'db_app_auth'@'%';

-- Step A.2: Create Health Profiles Table
CREATE TABLE IF NOT EXISTS user_health_profiles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    illness_health_condition_diet_dislikes_name VARCHAR(100),
    illness_health_condition_diet_dislikes_value VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB;

GRANT SELECT, INSERT, UPDATE, DELETE ON food_db.user_health_profiles TO 'db_app_auth'@'%';

-- Step A.3: Create Plate Builder Tables
CREATE TABLE IF NOT EXISTS plates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    plate_name VARCHAR(255) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS plate_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    plate_id INT NOT NULL,
    product_code VARCHAR(50) NOT NULL,
    quantity_grams FLOAT NOT NULL,
    FOREIGN KEY (plate_id) REFERENCES plates(id) ON DELETE CASCADE
) ENGINE=InnoDB;

GRANT SELECT, INSERT, UPDATE, DELETE ON food_db.plates TO 'db_app_auth'@'%';
GRANT SELECT, INSERT, UPDATE, DELETE ON food_db.plate_items TO 'db_app_auth'@'%';
FLUSH PRIVILEGES;

-- Step A.2: Create the table with known columns (Example structure for OpenFoodFacts)
CREATE TABLE IF NOT EXISTS products (
    code VARCHAR(50) PRIMARY KEY,
    url TEXT,
    creator VARCHAR(255),
    created_t VARCHAR(50),
    created_datetime VARCHAR(50),
    last_modified_t VARCHAR(50),
    last_modified_datetime VARCHAR(50),
    product_name TEXT,
    generic_name TEXT,
    quantity VARCHAR(255),
    packaging TEXT,
    brands TEXT,
    categories TEXT,
    origins TEXT,
    labels TEXT,
    stores TEXT,
    countries TEXT,
    ingredients_text TEXT,
    allergens TEXT,
    traces TEXT,
    
    -- Add FULLTEXT index for context search on ingredients and products
    FULLTEXT INDEX ft_idx_search (product_name, ingredients_text)
) ENGINE=InnoDB;

-- Step B: The Owner grants explicit privileges to the Reader and Loader
-- Grant explicit privileges to the Reader
GRANT SELECT ON food_db.products TO 'db_reader'@'%';
GRANT SELECT ON food_db.products_core TO 'db_reader'@'%';
GRANT SELECT ON food_db.products_allergens TO 'db_reader'@'%';
GRANT SELECT ON food_db.products_macros TO 'db_reader'@'%';
GRANT SELECT ON food_db.products_vitamins TO 'db_reader'@'%';
GRANT SELECT ON food_db.products_minerals TO 'db_reader'@'%';

-- Grant broad privileges to the Loader on food_db to allow temp tables and UPSERT modifications
GRANT SELECT, INSERT, UPDATE, DELETE, DROP, CREATE, ALTER, INDEX ON food_db.* TO 'db_loader'@'%';
FLUSH PRIVILEGES;

-- Step C: The Loader user would then run this MySQL command to import:
/*
LOAD DATA INFILE '/path/to/en.openfoodfacts.org.products.converted.csv'
INTO TABLE products
FIELDS TERMINATED BY '\t'
ENCLOSED BY ''
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;
*/
