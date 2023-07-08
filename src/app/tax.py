"""
"""

from dataclasses import dataclass


@dataclass
class TaxBand:
    """A class representing a tax band"""

    bands = []

    def __init__(
        self,
        year,
        chargeable,
        rate,
        tax_payable,
        cummulative_income,
        cummulative_tax,
    ):
        """"""
        self.year = year
        self.chargeable_income = chargeable
        self.rate = rate
        self.tax_payable = tax_payable
        self.cummulative_income = cummulative_income
        self.cummulative_tax = cummulative_tax

        self.bands.append(self)

    def __str__(self) -> str:
        return f"Year: {self.year}\tRate: {self.rate}"

    def save(self, db):
        """Save tax band to database"""
        band = (
            self.year,
            self.chargeable_income,
            self.rate,
            self.tax_payable,
            self.cummulative_income,
            self.cummulative_tax,
        )
        db.insert_band(band)

    @classmethod
    def save_all(cls, db):
        """"""
        for band in cls.bands:
            band.save(db)

    @classmethod
    def add_bands(cls, data):
        """"""
        for i in data:
            TaxBand(
                year=i[0],
                chargeable=i[1],
                rate=i[2],
                tax_payable=i[3],
                cummulative_income=i[4],
                cummulative_tax=i[5],
            )

    @classmethod
    def from_database(cls, data):
        for tax_band in data:
            id, year, chargeable, rate, tax, cum_inc, cum_tax = tax_band
            TaxBand(year, chargeable, rate, tax, cum_inc, cum_tax)
        return cls.bands
