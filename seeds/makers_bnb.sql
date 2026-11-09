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
    user_id INT REFERENCES users(id)
);


INSERT INTO users (username, password) VALUES ('Syed', 'password123!');
INSERT INTO users (username, password) VALUES ('Riasat Supreme Leader', 'qwerty1');

INSERT INTO spaces (name, description, price, user_id) VALUES ('Cosy Shed', 'Just a shed /n PLEASE NOTE: NO BEN INCLUDED', 100, 1);
INSERT INTO spaces (name, description, price, user_id) VALUES ('Castle Black', 'Game of Thrones', 100 ,2);


