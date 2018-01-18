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
