// Copyright (c) 2018, ahmed zaqout and abedelrhman and contributors
// For license information, please see license.txt

cur_frm.add_fetch('employee','department','department');
frappe.ui.form.on('Reward', {
	refresh: function(frm) {

	},
    reward_type: function(frm) {
        // cur_frm.set_value('reward_amount', 0);
        // cur_frm.set_value('reward_days', 0);
        // cur_frm.set_value('amount', 0);
        // cur_frm.set_value('day_value', 0);
    },
    reward_amount: function(frm) {
        if(cur_frm.doc.reward_amount){
            cur_frm.set_value('amount', cur_frm.doc.reward_amount);
        }
    },
    reward_days: function(frm) {
        if(cur_frm.doc.employee){
            frappe.call({
                "method": "get_salary",
                doc: cur_frm.doc,
                args: { "employee": cur_frm.doc.employee },
                callback: function(data) {
                    if (data) {
                        var total_earn = (data.message/30)*cur_frm.doc.reward_days
                        cur_frm.set_value('amount', total_earn);
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

        cur_frm.set_query("earning_type", function() {
                return {
                    // query: "erpnext.hr.doctype.business_trip.business_trip.get_approvers",
                    filters: {
                    	"type": 'earning'
                        // ["Salary Component", "type", "==", 'deduction'],
                    }
                };
            });

    }
});
