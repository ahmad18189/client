# -*- coding: utf-8 -*-
# Copyright (c) 2018, ahmed zaqout and abedelrhman and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document

class Reward(Document):
    def get_salary(self,employee):    
        result =frappe.db.sql("select net_pay from `tabSalary Slip` where employee='{0}' order by creation desc limit 1".format(employee))
        if result:
            return result[0][0]
        else:
            frappe.throw(_("No salary slip found for this employee"))
