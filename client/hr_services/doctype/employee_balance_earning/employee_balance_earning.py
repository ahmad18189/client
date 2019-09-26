# -*- coding: utf-8 -*-
# Copyright (c) 2019, ahmed zaqout and abedelrhman and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from erpnext.hr.doctype.leave_application.leave_application import get_leave_allocation_records

class EmployeeBalanceEarning(Document):
    def on_submit(self):
        leave_allocation = frappe.db.sql("select name from `tabLeave Allocation` where leave_type='Annual Leave - اجازة اعتيادية' and employee='{0}' and '{1}' between from_date and to_date".format(self.employee,self.earning_date))
        if leave_allocation:
            allocation = frappe.get_doc("Leave Allocation", leave_allocation[0][0])
            allocation.new_leaves_allocated = allocation.new_leaves_allocated+self.balance
            allocation.save(ignore_permissions=True)
            frappe.msgprint("Successfully added")


    def get_employee_leave_balance(self):
	    allocation_records = get_leave_allocation_records(self.posting_date, self.employee).get(self.employee, frappe._dict())
	    allocation = allocation_records.get('Annual Leave - اجازة اعتيادية', frappe._dict())

	    return allocation.total_leaves_allocated
