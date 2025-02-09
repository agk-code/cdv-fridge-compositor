CREATE TABLE IF NOT EXISTS fridge (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    quantity INT NOT NULL
);

INSERT INTO fridge (name, quantity)
VALUES 
    ('pepperoni', 10),
    ('mushroom', 20),
    ('cheese', 15)
ON CONFLICT (name) DO NOTHING;