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
        category INTEGER REFERENCES Categories ON DELETE CASCADE,
        date DATETIME
);

CREATE TABLE Categories (
        id INTEGER PRIMARY KEY,
        name TEXT
);
