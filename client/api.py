# -*- coding: utf-8 -*-
# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
import json

@frappe.whitelist(allow_guest=True)
def make_attendance():
	args = frappe.local.form_dict
    return args
