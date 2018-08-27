// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Penalty', {
	refresh: function(frm) {

	},
    penalty_type: function(frm) {
        // cur_frm.set_value('penalty_amount', 0);
        // cur_frm.set_value('penalty_days', 0);
        // cur_frm.set_value('amount', 0);
        // cur_frm.set_value('day_value', 0);
    },
    penalty_amount: function(frm) {
        if(cur_frm.doc.penalty_amount){
            cur_frm.set_value('amount', cur_frm.doc.penalty_amount);
        }
    },
    penalty_days: function(frm) {
        if(cur_frm.doc.employee){
            frappe.call({
                "method": "get_salary",
                doc: cur_frm.doc,
                args: { "employee": cur_frm.doc.employee },
                callback: function(data) {
                    if (data) {
                        var total_deduct = (data.message/30)*cur_frm.doc.penalty_days
                        cur_frm.set_value('amount', total_deduct);
                        cur_frm.set_value('day_value', data.message/30);
                    } else {
                        cur_frm.set_value('amount', 0);
                        cur_frm.set_value('day_value', 0);

                    }
                }
            });
        }
    },
	onload: function(frm) {

        cur_frm.set_query("deduction_type", function() {
                return {
                    // query: "erpnext.hr.doctype.business_trip.business_trip.get_approvers",
                    filters: {
                    	"type": 'deduction'
                        // ["Salary Component", "type", "==", 'deduction'],
                    }
                };
            });

    }
});
cur_frm.add_fetch('employee','department','department');
