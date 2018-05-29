// Copyright (c) 2016, ahmed zaqout and abedelrhman and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Business Trip report"] = {
	"filters": [
		{
			"fieldname":"employee",
			"label": __("Employee"),
			"fieldtype": "Link",
			"options": "Employee"
		},
		{
	        "fieldname": "year",
	        "label": __("Year"),
	        "fieldtype": "Select",
	        "options": "\n2018\n2019\n2020"
    	}
	]
}
