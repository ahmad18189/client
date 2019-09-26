# -*- coding: utf-8 -*-
# Copyright (c) 2019, ahmed zaqout and abedelrhman and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class CancelLeaveApplication(Document):
	def before_submit(self):
		doc = frappe.get_doc("Leave Application", self.leave_application)
		doc.docstatus = 2
		doc.status = 'Rejected'
		doc.workflow_state = 'Rejected'
		doc.save(ignore_permissions=True)
