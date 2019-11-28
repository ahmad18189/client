# -*- coding: utf-8 -*-
# Copyright (c) 2018, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
import datetime
from datetime import date
from dateutil.relativedelta import relativedelta
from frappe.utils import cint, cstr, flt, nowdate, comma_and, date_diff, getdate, get_datetime

class Warrantor(Document):
    pass
