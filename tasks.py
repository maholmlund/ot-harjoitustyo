from invoke import task
import os
import sqlite3

@task
def start(ctx):
    ctx.run("python3 src/index.py", pty=True)

@task
def test(ctx):
    ctx.run("pytest src", pty=True)

@task
def coverage_report(ctx):
    ctx.run("coverage run --branch -m pytest src", pty=True)
    ctx.run("coverage report -m", pty=True)
    ctx.run("coverage html", pty=True)
    ctx.run("echo html report generated, please open htmlcov/index.html in your browser")

@task
def create_database(ctx):
    ctx.run("cat src/schema.sql | sqlite3 database.db")
    con = sqlite3.connect("database.db")
    for c in ["ruoka",
              "liikenne",
              "liikunta",
              "kulttuuri",
              "sijoitukset"]:
        con.execute("INSERT INTO Categories (name) VALUES (?)", [c])
    con.commit()