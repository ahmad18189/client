// Copyright (c) 2019, ahmed zaqout and abedelrhman and contributors
// For license information, please see license.txt

frappe.ui.form.on('Employee Balance Earning', {
	refresh: function(frm) {

	},
	employee: function(frm) {
		frappe.call({
            method: "get_employee_leave_balance",
            doc: cur_frm.doc,
            callback: function(r) {
            	if(r){
                	frm.set_value('current_leave_balance', r.message)
           		}
           	}	
        });
	}

});
