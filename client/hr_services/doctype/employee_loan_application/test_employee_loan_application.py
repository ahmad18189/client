# -*- coding: utf-8 -*-
# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# See license.txt
from __future__ import unicode_literals

import frappe
import unittest
from erpnext.hr.doctype.salary_structure.test_salary_structure import make_employee

class TestEmployeeLoanApplication(unittest.TestCase):
	def setUp(self):
		self.create_loan_type()
		self.employee = make_employee("kate_loan@loan.com")
		self.create_loan_application()

	def create_loan_type(self):
		if not frappe.db.get_value("Loan Type", "Home Loan"):
			frappe.get_doc({
				"doctype": "Loan Type",
				"loan_name": "Home Loan",
				"maximum_loan_amount": 500000,
				"rate_of_interest": 9.2
			}).insert()

	def create_loan_application(self):
		if not frappe.db.get_value("Employee Loan Application", {"employee":self.employee}, "name"):
			loan_application = frappe.new_doc("Employee Loan Application")
			loan_application.update({
				"employee": self.employee,
				"loan_type": "Home Loan",
				"rate_of_interest": 9.2,
				"loan_amount": 250000,
				"repayment_method": "Repay Over Number of Periods",
				"repayment_periods": 24
			})
			loan_application.insert()
	

	def test_loan_totals(self):
		loan_application = frappe.get_doc("Employee Loan Application", {"employee":self.employee})
		self.assertEquals(loan_application.repayment_amount, 11445)
		self.assertEquals(loan_application.total_payable_interest, 24680)
		self.assertEquals(loan_application.total_payable_amount, 274680)

		loan_application.repayment_method = "Repay Fixed Amount per Period"
		loan_application.repayment_amount = 15000
		loan_application.save()

		self.assertEquals(loan_application.repayment_periods, 18)
		self.assertEquals(loan_application.total_payable_interest, 20000)
		self.assertEquals(loan_application.total_payable_amount, 270000)