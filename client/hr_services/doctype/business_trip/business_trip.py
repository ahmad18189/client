# -*- coding: utf-8 -*-
# Copyright (c) 2017, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils.data import getdate
from frappe.utils import cint, cstr, date_diff, flt, formatdate, getdate
from datetime import date, datetime

class OverlapError(frappe.ValidationError): pass

class BusinessTrip(Document):
    def validate(self):
        self.validate_dates()
        self.get_number_of_leave_days()
        self.get_ja_cost()
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


    def validate_dates(self):
        if getdate(self.from_date) > getdate(self.to_date):
            frappe.throw(_('To Date field must be less than To Date field'))

        
    def before_insert(self):
        pass

    def get_department_managers(self):
        department = self.get_department()
        query = """select user.* from tabEmployee employee
                            Inner Join tabUserRole role on employee.user_id = role.parent
                            Inner Join tabUser user on employee.user_id = user.name
                            where role.role = 'Department Manager' and employee.department='{department}'"""

        department_managers = frappe.db.sql(query.format(department=frappe.db.escape(department)), as_dict=1)
        return department_managers

    def get_department(self):
        employee = frappe.get_doc('Employee', {'user_id': self.owner})
        department = employee.department
        return department

    def get_users_in_role(self, role_name):
        query = """select user.* from tabUser user
                                    Inner Join tabUserRole role on user.name = role.parent
                                    where role.role = '{role}'"""
        users = frappe.db.sql(query.format(role=frappe.db.escape(role_name)), as_dict=1)
        return users

    def get_user(self, user):
        return frappe.get_doc('User', {'name': user})

    def get_employee(self, user):
        return frappe.get_doc('Employee', {'user_id': user})


    def get_employee_from_session (self):
        if self.get('__islocal'):
            employee = frappe.get_list("Employee", fields=["name","employee_name"]
            , filters = {"user_id":frappe.session.user},ignore_permissions=True)
            if employee != []:
                self.employee = employee[0].name
                self.employee_name = employee[0].employee_name



    def get_number_of_leave_days(self):
        if self.to_date and self.from_date:
            number_of_days = date_diff(self.to_date, self.from_date)
            if number_of_days<0:
                self.days = 0
                return 0
            self.days=number_of_days+1

    def get_ja_cost(self):
        total =0.0
        if self.days:
            if self.assignment_type=="Internal":
                total = flt(self.days)*flt(self.internal_per_diem_rate) +self.ticket_cost
            if self.assignment_type=="External":
                total = flt(self.days)*flt(self.external_per_diem_rate)+self.ticket_cost
                
        self.cost_total = total
        self.get_total_cost()

    def get_total_cost(self):
        total =0.0
        if self.assignment_type=="In City Assign" :
            total = flt(self.transportation_costs)*flt(self.days)
        if self.assignment_type=="Internal" or self.assignment_type=="External":
            total = flt(self.cost_total)
        self.total = total


    def get_default_cost_center(self,company):
        cost_center = frappe.get_doc('Company', company)
        return cost_center.cost_center


    # def get_current_user(self):
    #     user = frappe.session.user
    #     employees = frappe.get_list("Employee", fields=["name"], filters={'user_id': user}, ignore_permissions=True)
    #     if employees:
    #         employee = frappe.get_doc('Employee', {'name': employees[0].name})
    #         return employee

