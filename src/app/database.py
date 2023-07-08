"""
"""

import sqlite3


class Database:
    """"""

    def __init__(self, database) -> None:
        self.database = database
        self.connect()
        print("Connected to '{}'".format(self.database))

    def connect(self):
        self.connection = sqlite3.connect(self.database)
        self.cursor = self.connection.cursor()

    def disconnect(self):
        self.connection.close()


class RatesDB(Database):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.create_rates_table()

    def create_rates_table(self):
        with self.connection:
            self.cursor.execute(
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

    def insert_band(self, params):
        with self.connection:
            self.cursor.execute(
                """
                INSERT INTO rates (
                    year,
                    rate,
                    chargeable_income,
                    tax_payable,
                    cummulative_income,
                    cummulative_tax
                    )
                VALUES (?,?,?,?,?,?)
                """,
                params,
            )

    def get_all(self):
        self.cursor.execute(
            """
            SELECT * FROM rates
            """
        )
        return self.cursor.fetchall()

    def get_by_year(self, year):
        self.cursor.execute(
            """
            SELECT * FROM rates WHERE year = ?
            """,
            (year,),
        )
        return self.cursor.fetchall()
