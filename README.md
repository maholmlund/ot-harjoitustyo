# Ohjelmistotekniikka, harjoitustyö (ExpenseTracker)

Sovellus mahdollistaa oman talouden tarkkailun pitämällä kirjaa omista menoista. Sovelluksessa on mahdollista luoda useita käyttäjiä ja jokainen käyttäjä näkee vain omat menonsa. Dokumentaatio löytyy kansiosta [dokumentaatio](dokumentaatio).

## Dokumentaatio

- [arkkitehtuuri](dokumentaatio/arkkitehtuuri.md)
- [vaatimusmäärittely](dokumentaatio/vaatimusmaarittely.md)
- [työaikakirjanpito](dokumentaatio/tuntikirjanpito.md)
- [changelog](dokumentaatio/changelog.md)
- [käyttöohje](dokumentaatio/kaytto-ohje.md)
- [testausdokumentti](dokumentaatio/testaus.md)

## Käyttö

Sovelluksen käyttö vaatii Pythonin version 3.11 ([asennusohje](https://ohjelmistotekniikka-hy.github.io/python/toteutus#python-versioiden-hallinta)) tai uudemman sekä Poetryn ([asennusohje](https://ohjelmistotekniikka-hy.github.io/python/viikko2#asennus)). Sovelluksen asennus:

```
$ git clone https://github.com/maholmlund/ot-harjoitustyo
$ cd ot-harjoitustyo
$ poetry install
```

Tämän jälkeen voidaan suorittaa ohjelma:

```
$ poetry run invoke start
```

Sovellus tallentaa datan oletuksena tiedostoon database.db. Tätä voi muuttaa konfiguraatiotiedostossa ([ohje](./dokumentaatio/kaytto-ohje.md))

## Testit

Ohjelman testit voidaan suorittaa komennolla

```
$ poetry run invoke test
```

Testien kattavuusraportti puolestaan voidaan muodostaa komennolla

```
$ poetry run invoke coverage-report
```

## Lint

Pylint voidaan suorittaa koodille komennolla

```
$ poetry run invoke lint
```

## [Releaset](https://github.com/maholmlund/ot-harjoitustyo/releases/)
