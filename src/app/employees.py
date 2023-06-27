"""
"""

from dataclasses import dataclass


@dataclass
class Credential:
    """"""

    tin: str
    national_id: str
    ssnit_number: str


@dataclass
class Profile:
    """"""

    position: str
    residency: str
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
