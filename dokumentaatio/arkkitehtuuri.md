# Arkkitehtuuri

Ohjelma käyttää kolmea keskeistä luokkaa: Expense-luokka kuvaa kirjattua menoa, User-luokka käyttäjää ja Category menokategoriaa. Tietokannassa jokainen näistä luokista vastaa yhtä taulua.

```mermaid
 classDiagram
      Expense "*" --> "1" User
      Expense "*" --> "1" Category
      class User{
          username
          password
      }
      class Expense{
          amount
          description
          date
      }
      class Category{
        name
      }
```

```mermaid
---
  config:
    class:
      hideEmptyMembersBox: true
---
classDiagram
     ui --> expensetracker
     expensetracker --> database
```

## Ohjelman toiminta

Käyttäjän sisäänkirjautuminen noudattaa seuraavaa sekvenssikaaviota:
```mermaid
sequenceDiagram
  actor User
  participant UI
  participant Expensetracker
  participant Database
  User->>UI: click Login-button
  UI->>Expensetracker: login("esimerkki", "salasana")
  Expensetracker->>Database: get_user_by_username("esimerkki")
  Database-->>Expensetracker: user
  Expensetracker-->>UI: user
  UI->UI: MainView()
```

Menon kirjaamista kuvaava sekvenssikaavio:
```mermaid
sequenceDiagram
  actor User
  participant UI
  participant Expensetracker
  participant Database
  User->>UI: click Create-button
  UI->>Expensetracker: create_expense("2.2", "kurkkua", "ruoka", "2025-04-14")
  Expensetracker->>Database: create_expense(1, 2, 2, "kurkkua", "ruoka", "2025-04-14")
  Database-->>Expensetracker: None
  Expensetracker-->>UI: None
  UI->>UI: MainView()
```
