# -*- coding: utf-8 -*-
# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import _
from frappe.utils import getdate, validate_email_add, today, add_years, cint, cstr, flt, nowdate, comma_and, date_diff

class GovernmentalDocuments(Document):
    def validate(self):
        self.validate_dates()
        # self.validate_notification_message()
        # self.hooked_validate_notification_message()

    def validate_dates(self):
        from frappe.utils import getdate
        for d in self.get('governmental_documents'):
            if getdate(d.issue_date) > getdate(d.expired_date):
                frappe.throw(_("Issue Date must be smaller than expired date"))

    def validate_notification_message(self):
        from frappe.utils import getdate, add_months, nowdate
        message_hold = ""
        self.is_message = 0
        for d in self.get('governmental_documents'):
            if getdate(d.expired_date) <= getdate(add_months(nowdate(), 2)):
                message_hold += "<h5>The expired date of {0} will be expired on {1}</h5><br />".format(d.document_name, d.expired_date)
                self.is_message = 1
        self.message = message_hold

def hooked_validate_notification_message():
    from frappe.utils import getdate, add_months, nowdate
    gds  = frappe.get_all("Governmental Documents")
    if gds:
        for gd in gds:
            gdd = frappe.get_doc("Governmental Documents", gd.name)
            message_hold = ""
            gdd.is_message = 0
            for gdtab in gdd.get("governmental_documents"):
                    if getdate(gdtab.expired_date) <= getdate(add_months(nowdate(), 2)):
                        message_hold += "<h5>The expired date of {0} will be expired on {1}</h5><br />".format(gdtab.document_name, gdtab.expired_date)
                        gdd.is_message = 1

            if gdd.message != message_hold:
                gdd.message = message_hold
                gdd.save(ignore_permissions=True)
                frappe.db.commit()


def get_permission_query_conditions(user):
    if not user: user = frappe.session.user
    employees = frappe.get_list("Employee", fields=["name"], filters={'user_id': user}, ignore_permissions=True)
    if employees:
        query = ""
        employee = frappe.get_doc('Employee', {'name': employees[0].name})
        
        if u'Employee' in frappe.get_roles(user):
            if query != "":
                query+=" or "
            query+=""" employee = '{0}'""".format(employee.name)
        return query




def governmental_documents_validate_check():
    from frappe.core.doctype.communication.email import make
    frappe.flags.sent_mail = None

    emp = frappe.db.sql("select name,expired_date,employee,notification,document_name from `tabGovernmental Documents`")

    for i in emp:
        emp_doc = frappe.get_doc("Employee", i[2])

        if i[1] and i[3]:
            date_difference = date_diff(i[1], getdate(nowdate()))

            if date_difference <= 60 :
                unsubscribe_msg = "<br><h5>To unsubscribe this notification please edit the expiry date or uncheck the notification button</h5>"

                content_msg_emp="Your Governmental Documents {0} validity will end after {1} days".format(i[4],date_difference)
                content_msg_mng="Governmental Documents {0} validity will end after {1} days for employee: {2}".format(i[4],date_difference,i[0])
                if date_difference <= 0:
                    content_msg_emp="Your Governmental Documents validity has been ended"
                    content_msg_mng="Governmental Documents {0} validity has been ended for employee: {1}".format(i[4],i[0])

                prefered_email = frappe.get_value("Employee", filters = {"name": emp_doc.user_id}, fieldname = "prefered_email")
                prefered_email_mng = frappe.get_value("Employee", filters = {"name": 'EMP0015'}, fieldname = "prefered_email")
                prefered_email_mng1 = frappe.get_value("Employee", filters = {"name": 'EMP0007'}, fieldname = "prefered_email")
                prefered_email_mng2 = frappe.get_value("Employee", filters = {"name": 'EMP0050'}, fieldname = "prefered_email")

                if prefered_email:
                    try:
                        sent = 0
                        make(subject = "Governmental Documents Validity Notification", content=content_msg_emp+unsubscribe_msg, recipients=prefered_email,
                            send_email=True, sender="info@tadweeer.com")

                        make(subject = "Governmental Documents Validity Notification", content=content_msg_mng+unsubscribe_msg, recipients=prefered_email_mng,
                            send_email=True, sender="info@tadweeer.com")

                        make(subject = "Governmental Documents Validity Notification", content=content_msg_mng+unsubscribe_msg, recipients=prefered_email_mng1,
                            send_email=True, sender="info@tadweeer.com")

                        make(subject = "Governmental Documents Validity Notification", content=content_msg_mng+unsubscribe_msg, recipients=prefered_email_mng2,
                            send_email=True, sender="info@tadweeer.com")
                        
                        sent = 1
                        print 'send email for '+prefered_email
                    except:
                        frappe.msgprint("could not send")

                print content_msg_emp
                print '----------------------------------------------------------------'

