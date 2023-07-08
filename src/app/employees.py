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


@dataclass
class Profile:
    """"""

    position: str
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
