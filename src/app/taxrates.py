"""
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class TaxBand:
    """A class representing a tax band"""

    id = None
    rate: int
    chargeable_income: int
    tax_payable: int
    cummulative_income: int
    cummulative_tax: int
    year: int = datetime.now().year
