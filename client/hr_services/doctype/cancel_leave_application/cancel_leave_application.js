// Copyright (c) 2019, ahmed zaqout and abedelrhman and contributors
// For license information, please see license.txt

cur_frm.add_fetch('leave_application', 'employee', 'employee');
cur_frm.add_fetch('leave_application', 'employee_name', 'employee_name');
cur_frm.add_fetch('leave_application', 'posting_date', 'posting_date');
cur_frm.add_fetch('leave_application', 'leave_type', 'leave_type');
cur_frm.add_fetch('leave_application', 'leave_balance', 'leave_balance');
cur_frm.add_fetch('leave_application', 'from_date', 'from_date');
cur_frm.add_fetch('leave_application', 'to_date', 'to_date');
cur_frm.add_fetch('leave_application', 'total_leave_days', 'total_leave_days');

frappe.ui.form.on('Cancel Leave Application', {
	onload: function(frm) {

    	frm.set_query("leave_application", function() {
            return {
			    filters: [
			        ['Leave Application', 'docstatus', '=', 1]
			    ]
			}
        });

	}
});
