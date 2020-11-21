-- schema.sql
-- Since we might run the import many times we'll drop if exists

CREATE DATABASE IF NOT EXISTS challenge;

-- Make sure we're using our `blog` database
USE challenge;

-- We can create our user table
CREATE TABLE IF NOT EXISTS users
(
    id        BIGINT(8) AUTO_INCREMENT,
    public_id VARCHAR(40),
    name      VARCHAR(100),
    password  VARCHAR(100),
    admin     BOOLEAN,
    PRIMARY KEY (id)

);