"""
"""

from .database import RatesDB

import math



class PAYE:
    """A class representing the tax information of an Employee"""

    employee_bonus_percentage = 0.02
    bonus_tax_rate = 0.05
    overtime_tax_rate = 0.05

    def __init__(self, employee, basic_salary) -> None:
        """Constructor for the PAYE class"""
        self.employee = employee
        self.basic_salary = basic_salary
        self.third_tier = 0
        self.cash_allowances = 0
        self.accommodation_element = 0
        self.vehicle_element = 0
        self.non_cash_benefit = 0
        self.deductible_reliefs = 0
        self.overtime_income = 0

    def __str__(self) -> str:
        return f"{self.employee.__str__()}"

    @property
    def basic_salary(self):
        """The employee's basic salary"""
        return self._basic_salary

    @basic_salary.setter
    def basic_salary(self, value):
        if isinstance(value, (int, float)):
            if value < 0:
                raise ValueError
            self._basic_salary = value
        else:
            raise TypeError

    def compute_ssf(self):
        """Calculates the employee's social security contribution

        This is the amount contributed to the Social Security Fund by
        the employee

        Returns:
            float: A number representing 5.5% of the employee's basic salary if a ssnit member or 0 if not a ssnit member
        """
        if self.employee.profile.is_ssnit_member:
            ssnit_contribution = self.basic_salary * 0.055
            return ssnit_contribution
        return 0

    def compute_bonus_income(self):
        """Calculates the bonus income for an employee

        This creates two new instance attributes: one for bonus income up to 15%
        of annual income and one for any excess bonus

        """
        annual_income = self.basic_salary * 12
        limit = annual_income * 0.15
        bonus = annual_income * self.employee_bonus_percentage
        if bonus <= limit:
            self.bonus_income = bonus
            self.excess_bonus = 0
        else:
            self.bonus_income = limit
            self.excess_bonus = bonus - limit

    def compute_final_tax_on_bonus(self):
        """Calculate the final tax on bonus to employee

        This tax is on up to 15%  of the employees Annual basic salary

        Returns:
            float: A number representing 5% tax on the employee's annual basic salary
        """
        return self.bonus_income * self.bonus_tax_rate

    def compute_total_cash_emolument(self):
        """Calculates that total cash emolument

        This is the sum of the basic salary, cash allowances and excess bonu

        Returns:
            float: A number representing the total cash emolument for the employee
        """
        self.compute_bonus_income()
        return self.basic_salary + self.cash_allowances + self.excess_bonus

    def compute_total_assessable_income(self):
        """Calculates the total assessable income

        Returns:
            float: This is the sum of total cash emolument, accommodation and vehicle elements, and non-cash benefits
        """
        total_cash_emolument = self.compute_total_cash_emolument()
        benefits = (
            self.accommodation_element + self.vehicle_element + self.non_cash_benefit
        )
        return total_cash_emolument + benefits

    def compute_total_reliefs(self):
        """Calculates the total reliefs applicable to employee

        Returns:
            float: The sum of allowable pension reliefs granted to the employee and deductible reliefs
        """
        ssnit_contribution = self.compute_ssf()
        return ssnit_contribution + self.third_tier + self.deductible_reliefs

    def compute_chargeable_income(self):
        """Calculates the chargeable income for an employee

        This is the total assessable income less total reliefs
        """
        total_assessable_income = self.compute_total_assessable_income()
        total_reliefs = self.compute_total_reliefs()
        return total_assessable_income - total_reliefs

    def compute_tax_deductible(self):
        """Calculates the tax deductible

        This is the value of tax on Chargeable Income (total taxable emolument)
        using the rates in the First schedule of Internal Revenue Act, 2000 (Act 592) as amended
        """
        db = RatesDB("rates.db")
        rates = db.get_rates()
        cum_incs = db.get_cum_incomes()
        cum_taxes = db.get_cum_taxes()

        taxable = self.compute_chargeable_income()

        def round_half_up(n, decimals=0):
            multiplier = 10**decimals
            return math.floor(n * multiplier + 0.5) / multiplier

        def at_level(num):
            tax = (taxable - cum_incs[num - 1]) * rates[num]
            payable = tax + cum_taxes[num - 1]
            return payable
        tax = 0
        match self.employee.residency.name:
            case 'RESIDENT_FULLTIME':
                if taxable <= cum_incs[0]:
                    tax = taxable * rates[0]
                elif taxable <= cum_incs[1]:
                    tax = at_level(1)
                elif taxable <= cum_incs[2]:
                    tax = at_level(2)
                elif taxable <= cum_incs[3]:
                    tax = at_level(3)
                elif taxable <= cum_incs[4]:
                    tax = at_level(4)
                elif taxable <= cum_incs[5]:
                    tax = at_level(5)
                elif taxable <= cum_incs[6]:
                    tax = at_level(6)
            case 'RESIDENT_PARTTIME':
                tax = taxable * 0.10
            case 'RESIDENT_CASUAL':
                tax = taxable * 0.05
            case 'NON_RESIDENT':
                tax = taxable * 0.25

        return round_half_up(tax, 2)

    def compute_overtime_tax(self):
        """Calculates the overtime tax"""
        pass
