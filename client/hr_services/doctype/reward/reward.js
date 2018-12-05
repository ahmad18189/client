// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

function refresh_fields(frm) {
    if (frm.doc.reward_type == ('Days')) {
        frm.set_df_property("day_value", "hidden", false)
        frm.set_df_property("reward_days", "hidden", false)
        frm.set_df_property("reward_amount", "hidden", true)

    } else if (frm.doc.reward_type == ('Amount')) {
        frm.set_df_property("day_value", "hidden", true)
        frm.set_df_property("reward_days", "hidden", true)
        frm.set_df_property("reward_amount", "hidden", false)

    } else {
        frm.set_df_property("day_value", "hidden", true)
        frm.set_df_property("reward_days", "hidden", true)
        frm.set_df_property("reward_amount", "hidden", true)
    }
}
function validate(frm) {
    if (frm.doc.reward_type == ('Days')) {
        frm.set_value("reward_amount", 0)

    } else if (frm.doc.reward_type == ('Amount')) {
        frm.set_value("day_value", 0)
        frm.set_value("reward_days", 0)

    } else {
        frm.set_value("day_value", 0)
        frm.set_value("reward_days", 0)
        frm.set_value("reward_amount", 0)
        frm.set_value("amount", 0)
    }
}

function cal_reward(frm) {
    if (frm.doc.reward_type == ('Days')) {
        if (frm.doc.employee && frm.doc.day_value) {
            console.log("hello1")
            var total_earn = (frm.doc.day_value) * frm.doc.reward_days
            console.log("hello2")

            if (frm.doc.day_value && frm.doc.reward_days) {
            console.log("hello3")

                frm.set_value('amount', total_earn);
            } else {
            console.log("hello4")

                frm.set_value('amount', 0);
            }
        } else {
            console.log("hello5")

            frm.set_value('amount', 0);
            frm.set_value('day_value', 0);

        }


    } else if (frm.doc.reward_type == ('Amount')) {
        frm.set_value('amount', frm.doc.reward_amount);

    } else {
        frm.set_value('amount', 0);
    }
}

frappe.ui.form.on('Reward', {
    refresh: function (frm) {
        refresh_fields(frm);
    },
    reward_type: function (frm) {
        refresh_fields(frm);
        cal_reward(frm);
    },
    reward_amount: function (frm) {
        cal_reward(frm);
    },
    reward_days: function (frm) {
        cal_reward(frm)
    },
    employee: function (frm) {
        if (frm.doc.employee) {
            frappe.call({ 
                "method": "get_salary",
                doc: frm.doc,
                args: { "employee": frm.doc.employee },
                callback: function (data) {
                    if (data) {
                        var total_earn = (data.message / 30) * frm.doc.reward_days
                        frm.set_value('day_value', data.message / 30);
                        if (data.message && frm.doc.reward_days) {
                            frm.set_value('amount', total_earn);
                        } else {
                            frm.set_value('amount', 0);
                        }
                    } else {
                        frm.set_value('amount', 0);
                        frm.set_value('day_value', 0);

                    }
                    cal_reward(frm);

                }
            });
        }
    },
    validate: function (frm) {
        validate(frm)
    },
    onload: function (frm) {

        frm.set_query("earning_type", function () {
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
cur_frm.add_fetch('employee', 'department', 'department');
