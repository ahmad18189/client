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
		_("Employee") + "::150",
		_("Assignment Type") + "::150",
		_("Target City") + "::150",
		_("Trip Reason") + "::150",
		_("From Date") + ":Date:150",
		_("To Date") + ":Date:150",
		_("Days") + "::150",
		_("total") + "::150"
		]


def get_conditions(filters):
	conditions = ""

	if filters.get("year"): conditions += " and from_date between '{0}-01-01' and '{0}-12-30' ".format(filters.get("year"))

	if filters.get("employee"): conditions += " and employee = '{0}'".format(filters.get("employee"))


	return conditions


def get_data(filters):
	data = []
	conditions = get_conditions(filters)
	business_trip = frappe.db.sql("""select employee_name,assignment_type,target_city,trip_reason,from_date,to_date,days,total
	from `tabBusiness Trip` where docstatus = 1 {0} """.format(conditions),as_dict=1)

	for bt_list in business_trip:

		row = [
		bt_list.employee_name,
		bt_list.assignment_type,
		bt_list.target_city,
		bt_list.trip_reason,
		bt_list.from_date,
		bt_list.to_date,
		bt_list.days,
		bt_list.total
		]
		data.append(row)

	return data
