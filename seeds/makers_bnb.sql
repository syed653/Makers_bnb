DROP TABLE IF EXISTS bookings;
DROP TABLE IF EXISTS spaces;
DROP TABLE IF EXISTS users;

-- Then, we recreate them
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE spaces (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price INT,
    user_id INT REFERENCES users(id),
    available_from DATE,
    available_to DATE
);

CREATE TABLE bookings (
    id SERIAL PRIMARY KEY,
    space_id INT REFERENCES spaces(id),
    user_id INT REFERENCES users(id),
    date DATE NOT NULL,
    status VARCHAR(255) NOT NULL DEFAULT 'pending'
);

INSERT INTO users (username, password) VALUES ('syed', 'password123!');
INSERT INTO users (username, password) VALUES ('riasat', 'qwerty1');

INSERT INTO spaces (name, description, price, user_id, available_from, available_to) VALUES ('Cosy Shed', 'Just a shed PLEASE NOTE: NO BED INCLUDED', 100, 1, '2026-12-01', '2026-12-31');
INSERT INTO spaces (name, description, price, user_id, available_from, available_to) VALUES ('Castle Black', 'Game of Thrones', 100, 2, '2026-12-01', '2026-12-31');