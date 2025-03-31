CREATE TABLE Users (
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE,
        passwd TEXT
);

CREATE TABLE Expenses (
        id INTEGER PRIMARY KEY,
        user_id INTEGER REFERENCES Users ON DELETE CASCADE,
        amount_int INTEGER,
        amount_decimal INTEGER,
        desc TEXT,
        date DATETIME
);