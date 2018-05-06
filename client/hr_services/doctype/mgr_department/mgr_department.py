# -*- coding: utf-8 -*-
# Copyright (c) 2018, ahmed zaqout and abedelrhman and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class MGRDepartment(Document):
	nsm_parent_field = 'parent_mgr_department'

	def validate(self):
		pass

	def on_update(self):
		self.update_nsm_model()

	def on_trash(self):
		self.validate_trash()
		self.update_nsm_model()

	def update_nsm_model(self):
		"""update lft, rgt indices for nested set model"""
		frappe.utils.nestedset.update_nsm(self)

	def validate_trash(self):
		pass