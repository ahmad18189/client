# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt
from __future__ import unicode_literals
from frappe import throw, _
from frappe import msgprint, _
import json
import frappe
import frappe.handler
import frappe.client
from frappe.utils.response import build_response
from frappe import _
#from six.moves.urllib.parse import urlparse, urlencode


#from subprocess import Popen

@frappe.whitelist(allow_guest=True)
def test_instance():
    return 'this instance is working'

@frappe.whitelist(allow_guest=True)
def get_penalty_days(doc, method):
    penalty_days = frappe.get_list("Penalty", filters=[
		            ["docstatus", "=", 1],
                    ["employee", "=", doc.employee],
                    ["start_date", ">=", doc.start_date],
                    ["end_date", "<=", doc.end_date]
                ],
                fields=["days_count"]
            )
    if penalty_days:
        doc.penalty = penalty_days[0].days_count
    # doc.penalty = 0;
    # for penalty in penalties:
    #     if penalties:
    #         doc.penalty += penalty.days_count

@frappe.whitelist(allow_guest=True)
def asset_series(asset_category_code, asset_location):
    from frappe.model.naming import make_autoname

    asset_code = make_autoname(asset_location+"-"+asset_category_code+"-"+'.####')
    return asset_code
    