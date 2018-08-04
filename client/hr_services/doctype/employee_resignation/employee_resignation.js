// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
cur_frm.add_fetch("employee", "employee_name", "employee_name");
cur_frm.add_fetch('employee', 'department', 'department');
cur_frm.add_fetch('employee', 'direct_manager', 'direct_manager');

frappe.ui.form.on('Employee Resignation', {
    refresh: function(frm) {

    },
    validate: function(frm){
        var start = Date.parse(cur_frm.doc.date_of_joining);
        var end = Date.parse(cur_frm.doc.last_working_date);
        if (end < start) {
            frappe.throw("تاريخ اخر يوم عمل يجب أن يكون بعد تاريخ الانضمام للشركة");
    }
        var end = Date.parse(cur_frm.doc.permission_date);
        if (end < start) {
            frappe.throw("تاريخ طلب الاستقالة يجب أن يكون بعد تاريخ الانضمام للشركة");
        }
    }
});
