"""
"""

import pytest

from app.employees import Residency


@pytest.mark.parametrize("salary", ["300", 2 + 5j])
def test_basic_salary_is_a_valid_number(paye, salary):
    with pytest.raises(TypeError) as e:
        paye.basic_salary = salary
        assert not isinstance(paye.basic_salary, (int, float))


def test_basic_salary_is_greater_than_zero(paye):
    with pytest.raises(ValueError) as e:
        paye.basic_salary = -25.0
        assert paye.basic_salary < 0


@pytest.mark.parametrize("membership, expected", [(True, 49.5), (False, 0)])
def test_compute_ssnit_contribution(paye, membership, expected):
    paye.employee.profile.is_ssnit_member = membership
    actual = paye.compute_ssf()
    assert actual == expected


def test_all_bonuses_equals_zero_when_bonus_percentage_is_zero(paye):
    paye.employee_bonus_percentage = 0
    paye.compute_bonus_income()
    assert paye.bonus_income == 0
    assert paye.excess_bonus == 0


@pytest.mark.parametrize(
    "rate, bonus, excess",
    [
        (0.02, 216, 0),
        (0.076, 820.8, 0),
        (0.11, 1188, 0),
        (0.15, 1620, 0),
        (0.16, 1620, 108),
        (0.18, 1620, 324),
    ],
)
def test_compute_bonus_income_gives_correct_results(paye, rate, bonus, excess):
    paye.employee_bonus_percentage = rate
    paye.compute_bonus_income()
    assert paye.bonus_income == bonus
    assert paye.excess_bonus == excess


@pytest.mark.parametrize("rate", [0, 0.09, 0.15, 0.16, 0.22])
def test_compute_final_tax_on_bonus(paye, rate):
    paye.employee_bonus_percentage = rate
    paye.compute_bonus_income()
    expected = 0.05 * paye.bonus_income
    assert paye.compute_final_tax_on_bonus() == expected


@pytest.mark.parametrize("cash_allowances", [0, 100])
@pytest.mark.parametrize("rate", [0, 0.02, 0.15, 0.16])
def test_compute_total_cash_emolument(paye, rate, cash_allowances):
    paye.cash_allowances = cash_allowances
    paye.employee_bonus_percentage = rate
    paye.compute_bonus_income()
    expected = paye.basic_salary + paye.cash_allowances + paye.excess_bonus
    assert paye.compute_total_cash_emolument() == expected


@pytest.mark.parametrize("rate", [0, 0.02, 0.15, 0.16])
def test_compute_total_assessable_income(paye, rate):
    paye.employee_bonus_percentage = rate
    paye.compute_bonus_income()
    total_cash_emolument = paye.compute_total_cash_emolument()
    benefits = paye.accommodation_element + paye.vehicle_element + paye.non_cash_benefit
    expected = total_cash_emolument + benefits
    assert paye.compute_total_assessable_income() == expected


@pytest.mark.parametrize("deductible", [0, 120, 370])
@pytest.mark.parametrize("third_tier", [0, 50, 100])
@pytest.mark.parametrize(
    "ssnit_membership",
    [pytest.param(True, id="ssnit"), pytest.param(False, id="no_ssnit")],
)
def test_compute_total_reliefs(paye, ssnit_membership, third_tier, deductible):
    paye.employee.profile.is_ssnit_member = ssnit_membership
    paye.third_tier = third_tier
    paye.deductible_reliefs = deductible
    ssnit_contribution = paye.compute_ssf()
    expected = ssnit_contribution + paye.third_tier + paye.deductible_reliefs
    assert paye.compute_total_reliefs() == expected


@pytest.mark.parametrize(
    "excess, benefit, deductible",
    [(0, 0, 0), (0, 130, 100), (108, 200, 0), (10, 80, 240)],
)
@pytest.mark.parametrize(
    "ssnit_membership",
    [pytest.param(True, id="ssnit"), pytest.param(False, id="no_ssnit")],
)
def test_compute_chargeable_income(paye, ssnit_membership, excess, benefit, deductible):
    paye.employee.profile.is_ssnit_member = ssnit_membership
    paye.excess_bonus = excess
    paye.accommodation_element = benefit
    paye.deductible_reliefs = deductible
    total_assessable_income = paye.compute_total_assessable_income()
    total_reliefs = paye.compute_total_reliefs()
    expected = total_assessable_income - total_reliefs
    assert paye.compute_chargeable_income() == expected


@pytest.mark.parametrize(
    "ssnit_membership",
    [pytest.param(True, id="ssnit"), pytest.param(False, id="no_ssnit")],
)
@pytest.mark.parametrize(
    "residency",
    [
        pytest.param(Residency.RESIDENT_FULLTIME, id="res_ft"),
        pytest.param(Residency.RESIDENT_PARTTIME, id="res_pt"),
        pytest.param(Residency.RESIDENT_CASUAL, id="res_ca"),
        pytest.param(Residency.NON_RESIDENT, id="non_res"),
    ],
)
def test_compute_tax_deductible(paye, ssnit_membership, residency, expected_tax):
    paye.employee.profile.is_ssnit_member = ssnit_membership
    paye.employee.profile.residency = residency
    actual_tax = paye.compute_tax_deductible()
    assert actual_tax == expected_tax[residency.name][ssnit_membership]


@pytest.mark.skip(reason="Not implemented")
def test_compute_overtime_tax(paye, overtime):
    pass
