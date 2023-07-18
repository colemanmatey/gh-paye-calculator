"""
"""

import pytest

from app.database import RatesDB
from app.employees import Credential, Employee, Position, Profile, Residency
from app.paye import PAYE


@pytest.fixture
def credential():
    yield Credential("P7281302938", "GHA-751450821-0", "F203948123583")


@pytest.fixture
def profile():
    yield Profile(Position.JUNIOR, Residency.RESIDENT_FULLTIME)


@pytest.fixture
def employee(credential, profile):
    yield Employee(1, "John", "Dave", "Smith", "Male", profile, credential)


@pytest.fixture
def paye(employee):
    yield PAYE(employee, 900)


@pytest.fixture
def db(tmpdir):
    file = tmpdir.mkdir("sub").join("rates.db")
    database = RatesDB(file)
    yield database


@pytest.fixture
def conn(db):
    db.connect()
    yield db.connection
    db.disconnect()


@pytest.fixture
def cur(conn):
    cursor = conn.cursor()
    yield cursor
    cursor.close()
    conn.rollback()


@pytest.fixture
def query(cur):
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS rates (
            id INTEGER PRIMARY KEY,
            year INTEGER,
            rate REAL,
            chargeable_income REAL,
            tax_payable REAL,
            cummulative_income REAL,
            cummulative_tax REAL
        )
        """
    )

    bands = (
        (2021, 402, 0, 0, 402.00, 0),
        (2021, 110, 5, 5.5, 512.00, 5.5),
        (2022, 130, 10, 13, 642.00, 18.5),
        (2023, 3000, 17.5, 525, 3642.00, 543.5),
        (2023, 16395, 25, 4098.75, 20037.00, 4642.25),
        (2023, 29963, 30, 8988.90, 50000.00, 13631.15),
        (2024, 50000, 35, 17500, 0, 0),
    )

    cur.executemany(
        """
        INSERT INTO rates (
            year,
            chargeable_income,
            rate,
            tax_payable,
            cummulative_income,
            cummulative_tax
            )
        VALUES (?,?,?,?,?,?)
        """,
        bands,
    )

    yield cur
    cur.close()


@pytest.fixture
def expected_tax():
    tax = {
        "RESIDENT_FULLTIME": {
            True: 54.99,
            False: 63.65,
        },
        "RESIDENT_PARTTIME": {
            True: 85.05,
            False: 90.00,
        },
        "RESIDENT_CASUAL": {
            True: 42.53,
            False: 45.00,
        },
        "NON_RESIDENT": {
            True: 212.63,
            False: 225.00,
        },
    }
    yield tax
