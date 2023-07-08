"""
"""

import pytest

from app.employees import Employee


def test_employee_is_initialized_correctly(employee):
    assert employee.id == 1
    assert employee.firstname == "John"
    assert employee.othernames == "Dave"
    assert employee.lastname == "Smith"
    assert employee.gender == "Male"


def test_employee_instance_is_initialized_with_data():
    with pytest.raises(TypeError) as e:
        employee = Employee()


@pytest.mark.skip(reason="NotImplemented")
def test_method_returns_employee_full_name(employee):
    assert employee.fullname() == "SMITH, John Dave"
