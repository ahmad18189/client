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
	return columns, data


def get_columns(filters):
	return [
		_("Name") + ":Link/Leave Application:100",
		_("Employee") + ":Link/Employee:100",
		_("Employee Name") + "::180",
		_("Leave Type") + ":Link/Leave Type:180",
		_("From Date") + ":Date:100",
		_("To Date") + ":Date:100",
		_("Total Leave Days") + "::70"
		]


def get_conditions(filters):
	conditions = ""

	if filters.get("employee"): conditions += " and employee = '{0}' ".format(filters.get("employee"))

	if filters.get("leave_type"): conditions += " and leave_type = '{0}' ".format(filters.get("leave_type"))

	if filters.get("from_date"): conditions += " and from_date >= '{0}' ".format(filters.get("from_date"))
	if filters.get("to_date"): conditions += " and to_date <= '{0}' ".format(filters.get("to_date"))

	return conditions


def get_data(filters):
	data = []
	conditions = get_conditions(filters)
	li_list=frappe.db.sql("""select name, employee, employee_name, leave_type, from_date, to_date,
		total_leave_days from `tabLeave Application` where docstatus = 1 {0} """.format(conditions),as_dict=1)

	for leave in li_list:

		row = [
		leave.name,
		leave.employee,
		leave.employee_name,
		leave.leave_type,
		leave.from_date,
		leave.to_date,
		leave.total_leave_days
		]
		data.append(row)

	return data
