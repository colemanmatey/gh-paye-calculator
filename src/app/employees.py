"""
"""

from dataclasses import dataclass
from enum import Enum


@dataclass
class Credential:
    """"""

    tin: str
    national_id: str
    ssnit_number: str


class Residency(Enum):
    RESIDENT_FULLTIME = 1
    RESIDENT_PARTTIME = 2
    RESIDENT_CASUAL = 3
    NON_RESIDENT = 4


class Position(Enum):
    EXPATRIATE = 1
    MANAGEMENT = 2
    SENIOR = 3
    JUNIOR = 4
    OTHER = 5


@dataclass
class Profile:
    """"""

    position: Position
    residency: Residency
    has_secondary_employment: bool = False
    is_ssnit_member: bool = False


@dataclass
class Employee:
    """"""

    id: int
    firstname: str
    othernames: str
    lastname: str
    gender: str
    profile: Profile = None
    credential: Credential = None
