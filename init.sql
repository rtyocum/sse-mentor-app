-- Description: The initial SQL script to create the database schema
-- Author: Ryan Yocum

-- VERSION: 1
CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY,
  uid VARCHAR(255) NOT NULL UNIQUE,
  email VARCHAR(255) NOT NULL UNIQUE,
  firstname VARCHAR(255) NOT NULL,
  lastname VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS testcheckout (
  id INTEGER PRIMARY KEY,
  user_id INTEGER NOT NULL,
  course_code VARCHAR(255) NOT NULL,
  test_name VARCHAR(255) NOT NULL,
  checkout_date DATE NOT NULL,
  checkin_date DATE,
  FOREIGN KEY (user_id) REFERENCES users(id)
);
