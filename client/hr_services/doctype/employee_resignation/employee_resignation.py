# -*- coding: utf-8 -*-
# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import msgprint, _
from client.hr_services.doctype.end_of_service_award.end_of_service_award import get_award
from frappe.utils import cint, cstr, date_diff, flt, formatdate, getdate, get_link_to_form, \
    comma_or, get_fullname, add_years, add_months, add_days, nowdate, get_first_day, get_last_day
import math
import datetime

class EmployeeResignation(Document):

    # def validate(self):
    #     frappe.throw(str(get_first_day(getdate(self.last_working_date))))
    #     frappe.msgprint(str(self.last_working_date))
    #     frappe.msgprint(str(self.last_working_date)-str(get_first_day(getdate(self.last_working_date))))

    def diff_dates(date1, date2):
        return abs(date2-date1).days

    def on_submit(self):
        emp = frappe.get_doc("Employee",self.employee)
        emp.status ="Left"
        emp.relieving_date =self.last_working_date
        emp.save(ignore_permissions=True)

        sal_structure = frappe.db.sql("select parent from `tabSalary Structure Employee` where parenttype='Salary Structure' and employee='{0}'".format(self.employee))
        if sal_structure:
            sal = frappe.get_doc("Salary Structure", sal_structure[0][0])
            sal.is_active = 'No'
            sal.save(ignore_permissions=True)

        salary = frappe.get_list("Salary Slip", filters={"employee": self.employee}, fields=["net_pay"])

        if salary:
            award_info = get_award(self.date_of_joining, self.last_working_date, salary[0].net_pay,self.employment_type, "استقالة الموظف")


        total_leave_balance = frappe.db.sql("select total_leaves_allocated,from_date,to_date,name from `tabLeave Allocation` where employee='{0}' order by creation desc limit 1".format(self.employee))
        if total_leave_balance:
            leave_days = frappe.db.sql("select sum(total_leave_days) from `tabLeave Application` where employee='{0}' and posting_date between '{1}' and '{2}'".format(self.employee,total_leave_balance[0][1],total_leave_balance[0][2]))[0][0]
            if not leave_days:
                leave_days = 0
            leave_balance =  int(total_leave_balance[0][0])-int(leave_days)

        if emp.ticket_total_cost:
            pass
        else:
            emp.ticket_total_cost = 0


        month_worked_days = datetime.datetime.strptime(self.last_working_date, '%Y-%m-%d')

        eos_award = frappe.new_doc("End of Service Award")
        eos_award.employee = self.employee
        eos_award.employee_name = self.employee_name
        eos_award.department = self.department
        eos_award.type_of_contract = self.employment_type
        eos_award.work_start_date = self.date_of_joining
        eos_award.end_date = self.last_working_date
        eos_award.salary = salary[0].net_pay
        eos_award.reason = "استقالة الموظف"
        eos_award.days = award_info['days']
        eos_award.months = award_info['months']
        eos_award.years = award_info['years']
        eos_award.award = award_info['award']
        eos_award.ticket_number = emp.ticket_number
        eos_award.ticket_cost = emp.ticket_cost
        eos_award.ticket_total_cost = emp.ticket_total_cost
        eos_award.leave_number = leave_balance
        eos_award.leave_cost = round(salary[0].net_pay/30)
        eos_award.leave_total_cost = eos_award.leave_number*eos_award.leave_cost
        eos_award.days_number = int(month_worked_days.day)
        eos_award.day_value = round(salary[0].net_pay/30)
        eos_award.total_month_salary = eos_award.days_number*eos_award.day_value
        eos_award.total = flt(eos_award.leave_total_cost) + flt(eos_award.ticket_total_cost) + flt(eos_award.award) + flt(eos_award.total_month_salary)
        eos_award.insert()
        msg = """تم انشاء مكافأة نهاية الخدمة: <b><a href="#Form/End of Service Award/{0}">{0}</a></b>""".format(eos_award.name)
        frappe.msgprint(msg)

        # total_leave_balance = frappe.db.sql("select total_leaves_allocated,from_date,to_date,name from `tabLeave Allocation` where employee='{0}' order by creation desc limit 1".format(self.employee))
        # deserved_claim = 0
        # if total_leave_balance:
        #     leave_days = frappe.db.sql("select sum(total_leave_days) from `tabLeave Application` where employee='{0}' and posting_date between '{1}' and '{2}'".format(self.employee,total_leave_balance[0][1],total_leave_balance[0][2]))[0][0]
        #     if not leave_days:
        #         leave_days = 0
        #     leave_balance =  int(total_leave_balance[0][0])-int(leave_days)
        #     deserved_claim = (salary[0].net_pay / 30) * leave_balance


        # ec_doc = frappe.get_doc({
        #     "doctype":"Expense Claim",
        #     "exp_approver": 'Administrator',
        #     "posting_date": nowdate(),
        #     "employee": self.employee,
        #     "expenses": [
        #                   {
        #                     "doctype": "Expense Claim Detail",
        #                     "parenttype": "Expense Claim",
        #                     "parentfield": "expenses",
        #                     "expense_date": nowdate(),
        #                     "expense_type": 'بدل اجازات',
        #                     "claim_amount": round(deserved_claim),
        #                     "sanctioned_amount": round(deserved_claim)
        #                   },
        #                   {
        #                     "doctype": "Expense Claim Detail",
        #                     "parenttype": "Expense Claim",
        #                     "parentfield": "expenses",
        #                     "expense_date": nowdate(),
        #                     "expense_type": 'بدل تذاكر',
        #                     "claim_amount": 0,
        #                     "sanctioned_amount": 0
        #                   },
        #                   {
        #                     "doctype": "Expense Claim Detail",
        #                     "parenttype": "Expense Claim",
        #                     "parentfield": "expenses",
        #                     "expense_date": nowdate(),
        #                     "expense_type": 'نهاية الخدمة',
        #                     "claim_amount": round(flt(award_info['award']),2),
        #                     "sanctioned_amount": round(flt(award_info['award']),2)
        #                   }
        #                 ],
        #     "employee_name": self.employee_name,
        #     "company": frappe.defaults.get_user_default("Company")
        # }).insert(ignore_permissions=True)
        # msg = """تم انشاء المطالبة المالية: <b><a href="#Form/Expense Claim/{0}">{0}</a></b>""".format(ec_doc.name)
        # frappe.msgprint(msg)

        # doc = frappe.get_doc("Leave Allocation", total_leave_balance[0][3])
        # doc.new_leaves_allocated = 0
        # doc.total_leaves_allocated = 0
        # doc.save(ignore_permissions=True)
                        


    def get_salary(self):
        start_date = get_first_day(getdate(nowdate()))
        end_date = get_last_day(getdate(nowdate()))
        doc = frappe.new_doc("Salary Slip")
        doc.salary_slip_based_on_timesheet="0"

        doc.payroll_frequency= "Monthly"
        doc.start_date= start_date
        doc.end_date= end_date
        doc.employee= self.employee
        doc.employee_name= self.employee_name
        doc.company= frappe.defaults.get_user_default("Company")
        doc.posting_date= start_date
        
        doc.insert()

        grosspay =doc.gross_pay
        result=grosspay
        if result:
            return result
        else:
            frappe.throw("لا يوجد قسيمة راتب لهذا الموظف")
    
        

    def validate(self):
        if not self.last_working_date:
            frappe.throw("Please enter your last working date")

        if frappe.get_value('Employee Loan', filters={'employee' : self.employee,'status':'Sanctioned'}):
            name=frappe.get_value('Employee Loan', filters={'employee' : self.employee,'status':'Sanctioned'}) 
            loan_emp =frappe.get_doc("Employee Loan",name)      
            mm=loan_emp.status
            frappe.throw(self.employee+"/ "+self.employee_name+" have an active loan")

        self.validate_emp()
        if hasattr(self,"workflow_state"):
            if self.workflow_state:
                if "Rejected" in self.workflow_state:
                    self.docstatus = 1
                    self.docstatus = 2


    def validate_emp(self):
        if self.employee:
            employee_user = frappe.get_value("Employee", filters={"name": self.employee}, fieldname="user_id")
            if self.get('__islocal') and employee_user:
                if u'Direct Manager' in frappe.get_roles(employee_user):
                    self.workflow_state = "Created by Direct Manager"
                elif u'Employee TS' in frappe.get_roles(employee_user):
                    self.workflow_state = "Pending TS"
                elif u'Employee' in frappe.get_roles(employee_user):
                    self.workflow_state = "Pending"

            if not employee_user and self.get('__islocal'):
                self.workflow_state = "Pending TS"

                