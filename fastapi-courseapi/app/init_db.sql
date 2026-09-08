-- Create the database if it doesn't already exist
CREATE DATABASE IF NOT EXISTS app_db;

-- Switch to the newly created database
USE app_db;

-- Create the course_counter table
CREATE TABLE IF NOT EXISTS course_counter (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    count INT NOT NULL DEFAULT 0
);

-- Insert the initial record
INSERT INTO course_counter (id, name, count) 
VALUES (1, 'FIT3184', 0);