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

Sovelluksen rakenne on kolmikerroksinen: Ohjelman sovelluslogiikka on eriytetty erilliseen luokkaansa nimeltä Expensetracker. Sovelluksen käyttöliittymä kommunikoi Expensetracker-luokasta luodun globaalin instanssin kanssa ja näyttää siltä saamansa datan. ExpenseTracker-luokka ottaa konstruktorissa argumenttina tietokantayhteyden ja tallentaa ja lukee dataa tämän yhteyden kautta.

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

## Järjestelmän pääkomponentit

### ExpenseTracker

Sovelluslogiikasta vastaa luokka nimeltä ExpenseTracker. Tästä luokasta luodaan globaali instanssi jota käyttöliittymä käyttää. Luokka tarjoaa funktioita esimerkiksi liittyen käyttäjien hallintaan ja menojen kirjaamiseen. Kaikki tallentamista vaativa data annetaan tietokannalle tallennettavaksi. Yhteys tähän tietokantaan annetaan luokan konstruktorissa.

### UI

Komponentti, joka vastaa graafisesta käyttöliittymästä hyödyntäen TkInter-kirjastoa. Kommunikoi globaalin ExpenseTracker-instanssin kanssa suorittaakseen käyttäjän haluamat toiminnot ja näyttääkseen tarvittavan datan. Sisältää kolme päänäkymää:
- LoginView, joka tarjoaa ikkunan sisäänkirjautumiseen ja uuden käyttäjän luontiin
- MainView, joka tarjoaa käyttöliittymän uusien menojen kirjaamiseen ja vanhojen menojen tarkasteluun
- StatsView, joka näyttää erillisessä ikkunassa statistiikkaa käyttäjän kuukausittaisista menoista valitulta kuukaudelta

### DataBase

Luokka, joka tarjoaa tietokannan käsittelyyn tarvittavat funktiot. Luo konstruktorissa yhteyden tietokantaan ja on tämän jälkeen valmis suorittamaan ExpenseTracker-luokan pyytämät tehtävät. Tarvittaessa tiedon tallennustapa voidaan muuttaa koskematta sovelluslogiikkaan muokkaamalla tätä luokkaa (kts. [testit](../src/tests/expensetracker_test.py)).

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
