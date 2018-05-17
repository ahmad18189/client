# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"module_name": "client to all customer",
			"color": "grey",
			"icon": "octicon octicon-file-directory",
			"type": "module",
			"label": _("client to all customer")
		},
		{
			"module_name": "HR Services",
			"color": "#3498db",
			"icon": "octicon octicon-repo",
			"type": "module",
			"hidden": 0
		},
	]
