CREATE TABLE users (
    id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    username VARCHAR(255),
    password TEXT
);

CREATE TABLE ingredients (
    id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    ingredient VARCHAR(255),
    user_id INTEGER,
    count INTEGER DEFAULT 0,
    last_used TIMESTAMP,
    is_group BOOLEAN DEFAULT FALSE
);

CREATE TABLE ingredient_types (
    id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    type VARCHAR(255),
    user_id INTEGER
);

CREATE TABLE group_ingredients (
    id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    group_id INTEGER, -- linked to an ingredient "group"
    ingredient_id INTEGER,
    quantity INTEGER,
    quantity_type INTEGER
);

CREATE TABLE journal_entry (
    id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    user_id INTEGER,
    created TIMESTAMP,
    updated TIMESTAMP,
    notes TEXT DEFAULT ''
);

CREATE TABLE entry_ingredients (
    id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    ingredient_id INTEGER,
    quantity INTEGER,
    quantity_type INTEGER,
    notes TEXT DEFAULT ''
);

