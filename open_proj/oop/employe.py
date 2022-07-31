'''
Author: sherry
LastEditors: sherry
Date: 2022-07-30 22:05:27
FilePath: \open_project\oop\employe.py
Description: 
Copyright (c) 2022 by sherry , All Rights Reserved.
'''



class Employee:
    raise_ant = 1.04

    def __init__(self, first, last, pay) -> None:
        self.first = first
        self.last = last
        self.email = first + last + "@sherry.com"
        self.pay = pay

    def applay_raise(self):
        self.pay = int(self.pay * self.raise_ant)
    
    def fullname(self):
        return self.first+ ' ' + self.last

    @classmethod
    def set_raise_ant(cls, amount):
        cls.raise_ant = amount

    @classmethod
    def from_string(cls, emp_str):
        first, last, pay = emp_str.split('-')
        return cls(first, last, pay)

    @staticmethod
    def is_workday(day):
        if day.weekday() == 5 or day.weekday() == 6:
            return False
        return True

class Developer(Employee):
    raise_ant = 1.10
    def __init__(self, first, last, pay, prog_lang) -> None:
        super().__init__(first, last, pay)
        self.prog_lang = prog_lang

class Mangager(Employee):
    def __init__(self, first, last, pay, employees=None) -> None:
        super().__init__(first, last, pay)
        if employees is None:
            self.employees = []
        else:
            self.employees = employees

    def add_emp(self, emp):
        if emp not in self.employees:
            self.employees.append(emp)
    
    def remove_emp(self, emp):
        if emp in self.employees:
            self.employees.remove(emp)

    def print_emps(self):
        for emp in self.employees:
            print('-->', emp.fullname())

new_emp_1 = Employee.from_string('John-Doe-7000')

print(new_emp_1.email)
print(new_emp_1.pay)

import datetime
my_date = datetime.date(2022, 7, 30)
print(Employee.is_workday(my_date))
