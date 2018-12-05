// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

function refresh_fields(frm) {
    if (frm.doc.penalty_type == ('Days')) {
        frm.set_df_property("day_value", "hidden", false)
        frm.set_df_property("penalty_days", "hidden", false)
        frm.set_df_property("penalty_amount", "hidden", true)

    } else if (frm.doc.penalty_type == ('Amount')) {
        frm.set_df_property("day_value", "hidden", true)
        frm.set_df_property("penalty_days", "hidden", true)
        frm.set_df_property("penalty_amount", "hidden", false)

    } else {
        frm.set_df_property("day_value", "hidden", true)
        frm.set_df_property("penalty_days", "hidden", true)
        frm.set_df_property("penalty_amount", "hidden", true)
    }
}
function validate(frm) {
    if (frm.doc.penalty_type == ('Days')) {
        frm.set_value("penalty_amount", 0)

    } else if (frm.doc.penalty_type == ('Amount')) {
        frm.set_value("day_value", 0)
        frm.set_value("penalty_days", 0)

    } else {
        frm.set_value("day_value", 0)
        frm.set_value("penalty_days", 0)
        frm.set_value("penalty_amount", 0)
        frm.set_value("amount", 0)
    }
}

function cal_penalty(frm) {
    if (frm.doc.penalty_type == ('Days')) {
        if (frm.doc.employee && frm.doc.day_value) {
            var total_deduct = (frm.doc.day_value) * frm.doc.penalty_days
            if (frm.doc.day_value && frm.doc.penalty_days) {
                frm.set_value('amount', total_deduct);
            } else {
                frm.set_value('amount', 0);
            }
        } else {
            frm.set_value('amount', 0);
            frm.set_value('day_value', 0);

        }


    } else if (frm.doc.penalty_type == ('Amount')) {
        frm.set_value('amount', frm.doc.penalty_amount);

    } else {
        frm.set_value('amount', 0);
    }
}

frappe.ui.form.on('Penalty', {
    refresh: function (frm) {
        refresh_fields(frm);
    },
    penalty_type: function (frm) {
        refresh_fields(frm);
        cal_penalty(frm);
    },
    penalty_amount: function (frm) {
        cal_penalty(frm);
    },
    penalty_days: function (frm) {
        cal_penalty(frm)
    },
    employee: function (frm) {
        if (frm.doc.employee) {
            frappe.call({
                "method": "get_salary",
                doc: frm.doc,
                args: { "employee": frm.doc.employee },
                callback: function (data) {
                    if (data) {
                        var total_deduct = (data.message / 30) * frm.doc.penalty_days
                        frm.set_value('day_value', data.message / 30);
                        if (data.message && frm.doc.penalty_days) {
                            frm.set_value('amount', total_deduct);
                        } else {
                            frm.set_value('amount', 0);
                        }
                    } else {
                        frm.set_value('amount', 0);
                        frm.set_value('day_value', 0);

                    }
                    cal_penalty(frm);
                }
            });
        }
    },
    validate: function (frm) {
        validate(frm)
    },
    onload: function (frm) {

        frm.set_query("deduction_type", function () {
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
cur_frm.add_fetch('employee', 'department', 'department');
