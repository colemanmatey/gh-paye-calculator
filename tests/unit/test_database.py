"""
"""

import sqlite3


def test_connection_can_be_made_to_database(conn):
    assert type(conn) == sqlite3.Connection


def test_connect_method_creates_a_cursor(cur):
    assert type(cur) == sqlite3.Cursor


def test_fetch_data_from_rates_database(query):
    query.execute(
        """
        SELECT * FROM rates WHERE cummulative_tax = 18.5;
    """
    )
    expected = (3, 2022, 130.0, 10.0, 13.0, 642.0, 18.5)
    assert query.fetchone() == expected


def test_get_all_tax_bands_method_retrieves_all_data(db, query):
    db.cursor = query
    assert len(db.get_all()) == 7


def test_insert_band_method_persists_data_to_database(db, query):
    db.cursor = query
    band = (2025, 77060, 40, 20000, 56900, 0)
    db.insert_band(band)
    assert len(db.get_all()) == 8


def test_get_rates_by_year_method_retrieves_data_by_year(db, query):
    db.cursor = query
    assert len(db.get_by_year(2023)) == 3
