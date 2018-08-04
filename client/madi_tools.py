# -*- coding: utf-8 -*-
# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from __future__ import division
import frappe
import frappe, os , math
from frappe.model.document import Document
from frappe.utils import get_site_base_path
from frappe.utils.data import flt, nowdate, getdate, cint
from frappe.utils.csvutils import read_csv_content_from_uploaded_file
from frappe.utils.password import update_password as _update_password
from frappe.utils import cint, cstr, flt, nowdate, comma_and, date_diff, getdate
from umalqurra.hijri_date import HijriDate
import datetime
from datetime import date
from dateutil.relativedelta import relativedelta
from erpnext.hr.doctype.expense_claim.expense_claim import get_expense_claim_account

# def make_ss():
#     import sys
#     from frappe.utils.csvutils import read_csv_content
#     from frappe.core.doctype.data_import.importer import upload
#     # print "Importing " + path
    
#     with open('/home/frappe/frappe-bench/apps/client/client/ss.csv', "r") as infile:
#         rows = read_csv_content(infile.read())

#     for row in rows:
#         emp = frappe.get_doc("Employee", {'employee_id': row[0]})
#         print(emp.name)
#         # if row[9] == emp.civil_id_no:
#         #     if not frappe.db.exists("Salary Structure", emp.designation):
#         #         print "Adding To New One"
#         if emp:
#             frappe.get_doc({
#                 "doctype": "Salary Structure",
#                 "name": emp.employee_name+"-"+emp.name,
#                 "company": "Taab",
#                 "payment_account": "Cash - T",
#                 "employees":[{
#                     "employee": emp.name,
#                     "from_date": emp.date_of_joining,
#                     "base": row[1]
#                 }],
#                 "earnings":[

#                     {
#                         "salary_component": "الراتب الاساسي",
#                         "amount_based_on_formula": 0,
#                         "amount": row[1]
#                     },
#                     {
#                         "salary_component": "بدل السكن",
#                         "amount_based_on_formula": 0,
#                         "amount": row[2]
#                     },

#                     {
#                         "salary_component": "بدل المواصلات",
#                         "amount_based_on_formula": 0,
#                         "amount": row[3]
#                     },

#                     {
#                         "salary_component": "بدل الهاتف",
#                         "amount_based_on_formula": 0,
#                         "amount": row[4]
#                     },
#                     {
#                         "salary_component": "بدل طعام",
#                         "amount_based_on_formula": 0,
#                         "amount": row[5]
#                     },
#                     {
#                         "salary_component": "بدل طبيعة عمل",
#                         "amount_based_on_formula": 0,
#                         "amount": row[6]
#                     },

#                     {
#                         "salary_component": "بدل اضافي",
#                         "amount_based_on_formula": 0,
#                         "amount": row[7]
#                     }  
#                 ]
#             }).insert()
#             frappe.db.commit()
#             print(emp.employee_name)
#             # else:
#             #     print "Adding To Existing One"
#             #     pre_saved_doc = frappe.get_doc("Salary Structure", {"name": emp.designation})
                
#             #     ss_emp = {
#             #     "employee": emp.name,
#             #     "from_date": "2018-01-15",
#             #     "base": row[4]
#             #     },

#             #     {"employee": emp.name,
#             #     "from_date": "2018-01-15",
#             #     "base": row[4]
#             #     }
#             #     emps_list = pre_saved_doc.get("employees")
#             #     emps_list.append(ss_emp)
#             #     pre_saved_doc.set("employees", emps_list)
#             #     pre_saved_doc.save(ignore_permissions=True)
#             #     frappe.db.commit()
#             # c+=1
            

def make_ss():
    import sys
    from frappe.utils.csvutils import read_csv_content
    from frappe.core.doctype.data_import.importer import upload
    # print "Importing " + path
    
    with open('/home/frappe/frappe-bench/apps/client/emps.csv', "r") as infile:
        rows = read_csv_content(infile.read())

    emps = frappe.get_all("Employee", fields='*')
    c=0
    for emp in emps:
      for row in rows:
        if row[9] == emp.civil_id_no:
            if not frappe.db.exists("Salary Structure", emp.designation):
                print "Adding To New One"
                frappe.get_doc({
                    "doctype": "Salary Structure",
                    "name": emp.designation,
                    "payment_account": "Salary - T",
                    "employees":[{
                        "employee": emp.name,
                        "from_date": "2018-01-15",
                        "base": row[4]
                    }],
                    "earnings":[
                        {
                            "salary_component": "بدل السكن",
                            "amount_based_on_formula": 0,
                            "amount": row[5]
                        },

                        {
                            "salary_component": "بدل الموصلات",
                            "amount_based_on_formula": 0,
                            "amount": row[6]
                        },

                        {
                            "salary_component": "بدل الهاتف",
                            "amount_based_on_formula": 0,
                            "amount": row[7]
                        },

                        {
                            "salary_component": "بدل اضافي",
                            "amount_based_on_formula": 0,
                            "amount": row[8]
                        }   
                    ]
                }).insert()
                frappe.db.commit()
                c+=1

            else:
                print "Adding To Existing One"
                pre_saved_doc = frappe.get_doc("Salary Structure", {"name": emp.designation})
                
                ss_emp = {
                "employee": emp.name,
                "from_date": "2018-01-15",
                "base": row[4]
                },

                {"employee": emp.name,
                "from_date": "2018-01-15",
                "base": row[4]
                }
                emps_list = pre_saved_doc.get("employees")
                emps_list.append(ss_emp)
                pre_saved_doc.set("employees", emps_list)
                pre_saved_doc.save(ignore_permissions=True)
                frappe.db.commit()
            c+=1
            
               
        print c
        
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
    return False

def add_accounts_tree():
    from frappe.utils.csvutils import read_csv_content
    from frappe.core.doctype.data_import.importer import upload
    with open("/home/frappe/frappe-bench/apps/client/client/Accounts.csv", "r") as infile:
        rows = read_csv_content(infile.read())
    x = 0
    for id,row in enumerate(rows):
        if row[0] and row[1]:
            account_split = row[0].split("-")
            acc_num = ""
            account_name = ""

            if (len(account_split) == 1):
                account_name = account_split[0]
            elif len(account_split) > 2:
                i = 1
                acc_num = account_split[0]
                while i < len(account_split):
                    if i == 1:
                        account_name += account_split[i] 
                    else:
                        account_name += "-" + account_split[i] 
                    i+=1
            else:
                if is_number(account_split[0]):
                    account_name = account_split[1]
                    acc_num = account_split[0]
                else:
                    account_name = account_split[0] + "-" + account_split[1]
            if not frappe.db.exists("Account",{"account_name":account_name,"account_number":acc_num}):
                frappe.get_doc({
                    "doctype": "Account",
                    "account_name": account_name,
                    "account_number":acc_num,
                    "parent_account": row[1]+" - T",
                    "is_group":row[2],
                    "root_type":row[3],
                    "report_type":row[4],
                    "account_currency":row[5],
                    "account_type":row[6],
                    "warehouse": row[7]
                }).insert(ignore_mandatory=True)
                x +=1
                print row[0]
                print(str(x) + "      ------------------------------------")

def add_english_name_and_saluation():
    from frappe.utils.csvutils import read_csv_content
    from frappe.core.doctype.data_import.importer import upload
    with open("/home/frappe/frappe-bench/apps/client/emps.csv", "r") as infile:
        rows = read_csv_content(infile.read())
        

    for row in rows:
        print row[9]
        emp = frappe.get_doc("Employee",{'civil_id_no':row[9]})
        if emp.gender == "ذكر":
            emp.salutation = "السيد"
            emp.save()
        elif emp.gender == "أنثى":
            emp.salutation = "السيدة"
            emp.save()
        if row[9] == emp.civil_id_no:
            print("adding english name ",row[0],"to",row[9])
            emp.employee_english_name = row[0]
            emp.save()