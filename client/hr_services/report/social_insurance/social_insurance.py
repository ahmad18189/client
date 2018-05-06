# encoding: utf-8
# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt
from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import formatdate, getdate, flt, add_days
from datetime import datetime
import datetime
# import operator
import re
from datetime import date
from dateutil.relativedelta import relativedelta


def execute(filters=None):
	columns, data = get_columns(filters), get_data(filters)
	
	total_col= [""]*len(columns)

	for row in data:
		for i, col in enumerate(row):
			if i >2:
				total_col[i] = flt(total_col[i]) + flt(col)
			
	for i, col in enumerate(total_col):
		if i >2:
			total_col[i] = flt(total_col[i],2)


	total_col[0]='Totals'
		
	data.append(total_col)


	return columns, data

def get_columns(filters):
	return [
		_("Name") + ":Link/Employee:150",
		_("Employee Name") + "::150",
		_("Nationality") + "::150",
		_("Insurance Salary") + "::150",
		_("Occupational hazards") + "::150",
		_("Disabling work") + "::150",
		_("Salary") + "::150",
		_("Total") + "::150"
		
		]


def get_conditions(filters):
	conditions = ""

	if filters.get("company"): conditions += " and company= '{0}' ".format(filters.get("company"))

	if filters.get("branch"): conditions += " and branch= '{0}' ".format(filters.get("branch"))
	
	if filters.get("warrantor"): conditions += " and warrantor= '{0}' ".format(filters.get("warrantor"))


	return conditions


def get_data(filters):
	data =[]
	conditions = get_conditions(filters)
	li_list=frappe.db.sql("""select name, employee_name, emp_nationality, insurance_salary from `tabEmployee`
		where insurance_salary is not null {0} """.format(conditions),as_dict=1)

	for emp in li_list:

		row = [
		emp.name,
		emp.employee_name,
		emp.emp_nationality,
		emp.insurance_salary,
		round(flt(emp.insurance_salary)*0.02),
		round(flt(emp.insurance_salary)*0.02) if emp.emp_nationality=='Saudi Arabia' else 0,
		round(flt(emp.insurance_salary)*0.18) if emp.emp_nationality=='Saudi Arabia' else 0,
		(round(flt(emp.insurance_salary)*0.02)) + (round(flt(emp.insurance_salary)*0.02) if emp.emp_nationality=='Saudi Arabia' else 0) + (round(flt(emp.insurance_salary)*0.18) if emp.emp_nationality=='Saudi Arabia' else 0),
		]
		data.append(row)

	return data
