# Ohjelmistotekniikka, harjoitustyö (ExpenseTracker)

Sovellus mahdollistaa oman talouden tarkkailun pitämällä kirjaa omista menoista. Sovelluksessa on mahdollista luoda useita käyttäjiä ja jokainen käyttäjä näkee vain omat menonsa. Dokumentaatio löytyy kansiosta [dokumentaatio](dokumentaatio).

## Dokumentaatio

- [arkkitehtuuri](dokumentaatio/arkkitehtuuri.md)
- [vaatimusmäärittely](dokumentaatio/vaatimusmaarittely.md)
- [työaikakirjanpito](dokumentaatio/tuntikirjanpito.md)
- [changelog](dokumentaatio/changelog.md)

## Käyttö

Sovelluksen käyttö vaatii Pythonin version 3.10 tai uudemman sekä Poetryn. Sovelluksen asennus:

```
$ git clone https://github.com/maholmlund/ot-harjoitustyo
$ cd ot-harjoitustyo
$ poetry install
```

Tämän jälkeen voidaan alustaa tietokanta (tehtävä ennen sovelluksen käyttöä) ja suorittaa ohjelma:

```
$ poetry run invoke create-database
$ poetry run invoke start
```

Tietokannan alustus luo ainoastaan tietokannan, käyttäjän on itse luotava oma käyttäjänsä.

## Testit

Ohjelman testit voidaan suorittaa komennolla

```
$ poetry run invoke test
```

Testien kattavuusraportti puolestaan voidaan muodostaa komennolla

```
$ poetry run invoke coverage-report
```
