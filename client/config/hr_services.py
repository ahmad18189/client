from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Self Service"),
			"items": [
				{
					"type": "doctype",
					"name": "May Concern Letter",
					"description":_("May Concern Letter"),
					"hide_count": True
				},
				{
					"type": "doctype",
					"name": "Employee Loan",
					"description":_("Employee Loan"),
				},
				{
					"type": "doctype",
					"name": "Employee Loan Application",
					"description":_("Employee Loan Application"),
				},
				{
					"type": "doctype",
					"name": "End of Service Award",
					"description":_("End Of Service Award"),
				},
				{
					"type": "doctype",
					"name": "Overtime Request",
					"description":_("Overtime Request"),
				},
				{
					"type": "doctype",
					"name": "Financial Custody",
					"description":_("Financial Custody"),
				},
				{
					"type": "doctype",
					"name": "Employee Resignation",
					"description":_("Employee Resignation"),
				},
				{
					"type": "doctype",
					"name": "Promotion and Merit Increase",
					"description":_("Promotion and Merit Increase")
				},
				{
					"type": "doctype",
					"name": "Employee Badge Request",
					"description":_("Employee Badge Request")
				},
				{
					"type": "doctype",
					"name": "Employee Change IBAN",
					"description":_("Employee Change IBAN")
				},
				{
					"type": "doctype",
					"name": "Medical Insurance Application",
					"description": _("Medical Insurance Application."),
				},
			]
		}
	]
