# -*- coding:utf-8 -*-
# encoding: utf-8

# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import frappe
import os
from frappe.model.document import Document
from frappe.utils import get_site_base_path
from frappe.utils.data import flt, nowdate, getdate, cint
from frappe.utils.csvutils import read_csv_content_from_uploaded_file
from frappe.utils.password import update_password as _update_password
from frappe.utils import cint, cstr, flt, nowdate, comma_and, date_diff, getdate



def chek_emp():
	from frappe.utils.csvutils import read_csv_content
	from frappe.core.doctype.data_import.importer import upload
	with open("/home/frappe/frappe-bench/apps/client/client/empl.csv", "r") as infile:	
		rows = read_csv_content(infile.read())
        for index, row in enumerate(rows):
	        doc = frappe.db.sql("select name from `tabEmployee` where employee_name ='{0}'".format(row[3]))
	        if doc:
	        	print doc[0][0]
	        	doc = frappe.get_doc("Employee", doc[0][0])
	        	# doc.reports_to = row[3]
	        	# doc.append("leave_approvers", {
          #           "salary_component": "Income Tax",
          #           "amount_based_on_formula": 1,
          #           "formula": '(B+H)*.1',
          #           "condition": ""
          #       })
	        	# doc.save(ignore_permissions=True)
	        else:
	        	pass
	        	# print row[0]






def add_english_name_and_saluation():
    from frappe.utils.csvutils import read_csv_content
    from frappe.core.doctype.data_import.importer import upload
    with open("/home/frappe/Desktop/emps.csv", "r") as infile:
        rows = read_csv_content(infile.read())
        
    emps = frappe.get_all("Employee", fields='*')

    for emp in emps:
        for row in rows:
            if emp.gender == "ذكر":
                emp.salutation = "السيد"
            elif emp.gender == "أنثى":
                emp.salutation = "السيدة"

            if row[9] == emp.civil_id_no:
                print("adding english name ",row[0],"to",row[9])
                emp.employee_english_name = row[0]
                
            emp.save()



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

def add_accounts():
    from frappe.utils.csvutils import read_csv_content
    from frappe.core.doctype.data_import.importer import upload
    with open("/home/frappe/Desktop/Accounts.csv", "r") as infile:
        rows = read_csv_content(infile.read())
    x = 0
    y = 0
    
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

            testname = ""
            if acc_num:
                test_name = acc_num + "-" + account_name
            else:
                test_name = account_name


            try:
                frappe.get_doc({
                    "doctype": "Account",
                    "account_name": account_name,
                    "account_number": acc_num,
                    "parent_account": row[1]+ " - CAMA",
                    "is_group":row[2],
                    "root_type":row[3],
                    "report_type":row[4],
                    "account_currency":row[5],
                    "account_type":row[6],
                    "warehouse": row[7]
                }).insert(ignore_mandatory=True)
                x +=1
                print(str(x) + "      **********-----------*************")
                print acc_num,"-",account_name

            except:
                print "Updating....................................................."
                print row[0]
                ac_doc = frappe.get_doc("Account", row[0]+" - CAMA")
                #print ac_doc.name
                if row[1]:
                    ac_doc.update({
                        "parent_account": row[1] + " - CAMA"
                    })
                    x +=1
                    print(str(x) + "      **********-----------*************")


def add_accounts_heads():
    from frappe.utils.csvutils import read_csv_content
    from frappe.core.doctype.data_import.importer import upload
    with open("/home/frappe/Desktop/Accounts.csv", "r") as infile:
        rows = read_csv_content(infile.read())
    x = 0
    y = 0
    
    for id,row in enumerate(rows):
        if row[1] !=None:
            account_split = row[1].split("-")
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
                    account_name = row[1]

            if not frappe.db.exists("Account",{"account_name":account_name }):
                frappe.get_doc({
                    "doctype": "Account",
                    "account_name": account_name,
                    "account_number": acc_num,
                    "is_group": 1,
                    "root_type":row[3],
                    "report_type":row[4],
                    "account_currency":row[5],
                    "account_type":row[6],
                    "warehouse": row[7]
                }).insert(ignore_mandatory=True)
                x +=1
                print(str(x) + "      **********-----------*************")
                print account_name,"-",acc_num






def add_accounts_tree():
    from frappe.utils.csvutils import read_csv_content
    from frappe.core.doctype.data_import.importer import upload
    with open("/home/frappe/frappe-bench/apps/client/client/Accounts.csv", "r") as infile:
        rows = read_csv_content(infile.read())
    x = 0
    for id,row in enumerate(rows):
        if row[1] == None and row[0] != None:
            print(row[0])
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
            if not frappe.db.exists("Account",{"account_name":account_name }):
                frappe.get_doc({
                    "doctype": "Account",
                    "account_name": account_name,
                    "account_number":acc_num,
                    "is_group":row[2],
                    "root_type":row[3],
                    "report_type":row[4],
                    "account_currency":row[5],
                    "account_type":row[6]
                }).insert(ignore_mandatory=True)
                x +=1
                print(str(x) + "      **********-----------*************")
        elif row[0] != None:
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
                    "parent_account": row[1]+" - CAMA",
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



def add_gosi_component():
    emps = frappe.get_all("Employee",filters={'company': "Tadweer" },fields={'name','employee_name'})
    for emp in emps:
        doc = frappe.db.sql("""select parent from `tabSalary Structure Employee` where employee = '{0}' """.format(emp.name))
        if (doc):
            x = frappe.get_doc("Salary Structure",doc[0][0])
            x.append("deductions", {
                            "salary_component": "Income Tax",
                            "amount_based_on_formula": 1,
                            "formula": '(B+H)*.1',
                            "condition": ""
                        })
            print("---------------------")
            x.save(ignore_permissions=True)
            print("*********************")
            print(x.name)



def new_add_salary():
    from frappe.utils.csvutils import read_csv_content
    from frappe.core.doctype.data_import.importer import upload
    with open("/home/frappe/Desktop/emps.csv", "r") as infile:
        rows = read_csv_content(infile.read())
        
    emps = frappe.get_all("Employee", fields='*')

    for emp in emps:
        print "Hello"
        for row in rows:
            if emp.employee_name == row[1]:
                print emp.name
                if not frappe.db.exists("Salary Structure", emp.designation):
                    print "Adding To New One"
                    print emp.designation
                    frappe.get_doc({
                        "doctype": "Salary Structure",
                        "name": emp.designation,
                        "payment_account": "Salary - T",
                        "employees": [{
                            "employee": emp.name,
                            "from_date": emp.date_of_joining,
                            "base": row[4]
                        }],
                        "earnings": [
                            {
                            "salary_component": "بدل السكن",
                            "amount_based_on_formula": 0,
                            "amount": row[5]
                        }
                        , 
                        {
                            "salary_component": "بدل الموصلات",
                            "amount_based_on_formula": 0,
                            "amount": row[6]
                        }
                        ,
                        {
                            "salary_component": "بدل الهاتف",
                            "amount_based_on_formula": 0,
                            "amount": row[7]
                        }, {
                            "salary_component": "بدل اضافي",
                            "amount_based_on_formula": 0,
                            "amount": row[8]
                        }]
                    }).insert()

                else:
                    print "Adding To Existing One"
                    existing_sal_str = frappe.get_doc("Salary Structure",{"name": emp.designation})
                
                    existing_sal_str.append("employees", {
                        "employee": emp.name,
                        "from_date": emp.date_of_joining,
                        "base": row[4]
                    })
                    existing_sal_str.save(ignore_permissions=True)


def my_add_salary():
    from frappe.utils.csvutils import read_csv_content
    from frappe.core.doctype.data_import.importer import upload
    with open("/home/frappe/Desktop/emps.csv", "r") as infile:
        rows = read_csv_content(infile.read())
    des_doc = frappe.get_list("Designation", fields="name")
    for i in des_doc:
        x = i.name
        employees = []
        Housing_Com = 0
        Transport_Com = 0
        Telephone_Com = 0
        Others_Com = 0
        for index, row in enumerate(rows):
            base = row[4]
            if row[2] == i.name:
                Housing_Com = row[5]
                Transport_Com = row[6]
                Telephone_Com = row[7]
                Others_Com = row[8]
                print "We are here  - " + row[0]
                employees.append(frappe.get_list("Employee", fields=["employee_name", "date_of_joining", "name"],
                                                 filters={"employee_name": row[1]})[0])
        Sal_comp = ["بدل السكن", "بدل الموصلات", "بدل الهاتف", "بدل اضافي"]
        Sal_Amount = [Housing_Com, Transport_Com, Telephone_Com, Others_Com]

        print(employees)

        if employees != []:
            sal_doc = frappe.new_doc("Salary Structure")
            sal_doc.update({
                "doctype": "Salary Structure",
                "name": i.name,
                #"from_date": filtered_emp[0].date_of_joining,
                "employees": get_employee_from_id(employees, base),
                "payment_account": "Marketing Expenses - CAMA",


            })
            for i in Sal_comp:
                if i != "0":
                    comp = {"doctype": "Salary Detail", "salary_component": i,
                            "parenttype": "Salary Structure",
                            "parentfield": "earnings", "amount": i}
                    sal_doc.append("earnings", comp)

            sal_doc.insert()

        print "*********************************"
        #get_employee_from_id(employees, base)

        print("///////////////////////////////////////")


def get_employee_from_id(employees, base):
    emps_data = []
    for i in employees:
        emps_data.append({
            "employee": i.name,
            "base": base,
            "from_date": i.date_of_joining,
            "employee_name": i.employee_name
        })

    for i in emps_data:
        print i["from_date"]
    return emps_data




def add_bus_trips():
    emps = frappe.get_list("Employee", fields=["employee"], filters=None)
    for x in emps:
        print x.encode()

    for i in range(20):
        frappe.get_doc({
            "doctype": "Business Trip App",
            "employee": str(random.choice(emps)[1]).encode()
        }).insert(ignore_permissions=True)

def level():
    from frappe.utils.csvutils import read_csv_content
    from frappe.core.page.data_import_tool.importer import upload
    with open("/home/frappe/frappe-bench/apps/erpnext/erpnext/level.csv", "r") as infile:
        rows = read_csv_content(infile.read())
    for index, row in enumerate(rows):

        comps = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
        for c, i in zip(comps, range(2, 17)):
            print c
            frappe.get_doc({
                "doctype": "Level",
                "level_name": str(row[0]),
                "grade": str(c),
                "main_payment": row[i],
                "annual_bonus": row[17],
                "transportation": row[19],
                "living": row[18],
                "level_designation": [
                    {
                        "doctype": "Level Designation",
                        "parenttype": "Level",
                        "designation": row[1],
                        "parentfield": "level_designation"
                    }
                ],
                "internal_assignment": row[20],
                "external_assignment": row[21]

            }).insert(ignore_permissions=True)


def add_salary():
    from frappe.utils.csvutils import read_csv_content
    from frappe.core.page.data_import_tool.importer import upload
    with open("/home/frappe/frappe-bench/apps/erpnext/erpnext/salary.csv", "r") as infile:
        rows = read_csv_content(infile.read())
    for index, row in enumerate(rows):
        if row[0]:
            query = frappe.db.sql(
                "select name, employee_name, employee_no, date_of_joining, nationality, status from `tabEmployee` where civil_id='{0}'".format(row[2]), as_dict=1)
            if query:
                deductions = []
                earnings = []
                comps = ["Basic", "Housing", "Transportation",
                         "Communication", "Living", "Other Earnings"]
                idx = 1
                for c, i in zip(comps, range(6, 12)):
                    if row[i]:
                        comp = {"doctype": "Salary Detail", "salary_component": c, "parenttype": "Salary Structure",
                                "parentfield": "earnings", "formula": row[i], "idx": idx}
                        idx += 1
                        earnings.append(comp)

                if query[0].status == "Active":
                    print query[0].name
                    print row[2]
                    ss = frappe.new_doc("Salary Structure")
                    ss.update(
                        {
                            "doctype": "Salary Structure",
                            "name": query[0].name + "-SS",
                            "owner": "Administrator",
                            "from_date": query[0].date_of_joining,
                            "company": "جمعية الاطفال المعوقين",
                            "is_active": "Yes",
                            "payment_account": "النفقات - جاا",
                            "employees": [
                                {
                                    "doctype": "Salary Structure Employee",
                                    "parenttype": "Salary Structure",
                                    "base": row[6],
                                    "variable": 0,
                                    "from_date":query[0].date_of_joining,
                                    "employee": query[0].name,
                                    "docstatus": 0,
                                    "employee_name": query[0].employee_name,
                                    "parentfield": "employees"
                                }
                            ],
                            "earnings": earnings,
                            "deductions": deductions,
                            "hour_rate": 0,
                            "salary_slip_based_on_timesheet": 0
                        }
                    )
                    ss.insert()


def add_translation(ignore_links=False, overwrite=False, submit=False, pre_process=None, no_email=True):
    import sys
    from frappe.utils.csvutils import read_csv_content
    from frappe.core.page.data_import_tool.importer import upload
    with open('/home/frappe/frappe-bench/apps/erpnext/erpnext/trans.csv', "r") as infile:
        rows = read_csv_content(infile.read())
        for index, row in enumerate(rows):
            if not frappe.db.exists("Translation", {"source_name": row[0]}) and (row[0] is not None):
                print index, '---', row[0]
                frappe.get_doc({
                    "doctype": "Translation",
                    "language": 'ar',
                                "source_name": row[0],
                                "target_name": row[1]
                }).insert(ignore_permissions=True)


def test():
    atr = "atawefawe'awefawef'awefawfe'"
    print atr
    print "**********"
    print atr.replace("'", "`")


def translation_edit():
    final = frappe.db.sql(
        "select count(target_name) from tabTranslation where target_name like '%<br>%' and name not in ('00497355b4')")
    finall = frappe.db.sql(
        "select target_name,name from tabTranslation where target_name like '%<br>%' and name not in ('00497355b4')")
    c = 0
    for i in range(final[0][0]):
        c += 1
        print finall[i][1]
        print c
        print finall[i][0]
        print "-------------"
        removing = finall[i][0].split("<br>", 1)[0]
        removing2 = removing.strip()
        print "******"
        print removing2
        removewithcom = removing2.replace("'", "`")
        # frappe.db.sql(""" update tabTranslation set target_name='{0}' where name='{1}' """.format(str(removewithcom),finall[i][1]))
        print "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
    print c


def add_sup():
    import sys
    from frappe.utils.csvutils import read_csv_content
    from frappe.core.page.data_import_tool.importer import upload
    with open("/home/frappe/frappe-bench/apps/erpsystem/erpsystem/supp.csv", "r") as infile:
        rows = read_csv_content(infile.read())
        c = 0
        for index, row in enumerate(rows):
            frappe.get_doc({
                "doctype": "Supplier",
                "supplier_type": row[1],
                "name": row[2],
                "supplier_name": row[3],
                "cr_no": row[4],
                "cr_no_expiry_date": row[5],
                "default_currency": row[12]


            }).insert(ignore_permissions=True)
            c += 1
    print c


def add_add():
    import sys
    from frappe.utils.csvutils import read_csv_content
    from frappe.core.page.data_import_tool.importer import upload
    with open("/home/frappe/frappe-bench/apps/erpsystem/erpsystem/supp.csv", "r") as infile:
        rows = read_csv_content(infile.read())
        c = 0
        for index, row in enumerate(rows):
            frappe.get_doc({
                "doctype": "Address",
                "address_title": row[3],
                "address_type": "Billing",
                "address_line1": row[7],
                "phone": row[8],
                "fax": row[9],
                "city": "RIYADH",
                "email_id": row[10],
                "country": "Saudi Arabia",
                "supplier": row[3],
                "supplier_name": row[3]


            }).insert(ignore_permissions=True)

            c += 1
    print c


def add_emp():
    import sys
    from frappe.utils.csvutils import read_csv_content
    from frappe.core.page.data_import_tool.importer import upload
    with open("/home/frappe/frappe-bench/apps/erpnext/erpnext/employee_names.csv", "r") as infile:
        rows = read_csv_content(infile.read())
        c = 0
        for index, row in enumerate(rows):
            print index, " ** ", row[3]
            frappe.get_doc({
                "doctype": "Employee",
                "employee_no": row[1],
                "employee_name": row[2],
                "civil_id": row[3],
                "permanent_address": row[4],
                "cell_number": row[5],
                "date_of_joining": row[6],
                "date_of_birth": row[7],
                "gender": row[8],
                "nationality": row[9],
                "employment_type": row[10],
                "city": row[11],
                "branch": row[12],
                "designation": row[13],
                "grade": row[14]
                # "level":row[14],"-", row[15]

            }).insert(ignore_permissions=True)
            c += 1
    print c


def add_members():
    import sys
    from frappe.utils.csvutils import read_csv_content
    from frappe.core.page.data_import_tool.importer import upload
    with open("/home/frappe/frappe-bench/apps/erpnext/erpnext/members.csv", "r") as infile:
        rows = read_csv_content(infile.read())
        c = 0
        for index, row in enumerate(rows):
            print index, " ** ", row[1]
            frappe.get_doc({
                "doctype": "Member",
                "full_name": row[0],
                "civil_id": row[1],
                "membership_no": row[2],
                "payment_date": row[3],
                "cell_number": row[4]

            }).insert(ignore_permissions=True)
            c += 1
    print c


def add_benef():
    import sys
    from frappe.utils.csvutils import read_csv_content
    from frappe.core.page.data_import_tool.importer import upload
    with open("/home/frappe/frappe-bench/apps/erpnext/erpnext/Beneficiaries.csv", "r") as infile:
        rows = read_csv_content(infile.read())
        c = 0
        for index, row in enumerate(rows):
            if row[5] == "تسليم":
                pass
                print index, " ** ", row[4]
                frappe.get_doc({
                    "doctype": "Beneficiary",
                    "full_name": row[0],
                    "cell_number": row[1],
                    "secondary_cell_number": row[2],
                    "disability_type": row[3],
                    "record_number": row[4],
                    "card_delivered": 'Yes',
                    "received_device": row[6],
                    "received_date": row[7]

                }).insert(ignore_permissions=True)
                c += 1
            else:
                print index, " ** ", row[4]
                frappe.get_doc({
                    "doctype": "Beneficiary",
                    "full_name": row[0],
                    "cell_number": row[1],
                    "secondary_cell_number": row[2],
                    "disability_type": row[3],
                    "record_number": row[4],
                    "card_delivered": 'No',
                    "received_device": row[6],
                    "received_date": row[7]

                }).insert(ignore_permissions=True)
                c += 1
    print c


def txt():
    zz = frappe.db.sql("select membership_no,civil_id from tabMember")
    x = 0
    for i in range(len(zz)):
        print zz[i][1]
        print zz[i][0].replace(',', '')
        frappe.db.sql("update tabMember set membership_no={0} where civil_id={1}".format(
            zz[i][0].replace(',', ''), zz[i][1]))
        x += 1
    print x


def add_level():
    import sys
    from frappe.utils.csvutils import read_csv_content
    from frappe.core.page.data_import_tool.importer import upload
    with open("/home/frappe/frappe-bench/apps/erpnext/erpnext/employee_names.csv", "r") as infile:
        rows = read_csv_content(infile.read())
        c = 0
        for index, row in enumerate(rows):
            print index, " ** ", row[3]
            frappe.db.sql("update tabEmployee set level='{0}' where civil_id={1}".format(
                row[14]+'-'+row[15], row[3]))

            c += 1
    print c


def add_usr():
    import sys
    from frappe.utils.csvutils import read_csv_content
    from frappe.core.doctype.data_import.importer import upload
    # print "Importing " + path
    with open('/home/frappe/Desktop/employees.csv', "r") as infile:
        rows = read_csv_content(infile.read())
        emails = []
        names = []
        cc = 0
        for index, row in enumerate(rows):
            dublicate = ""
            cc += 1
            string = (row[1])
            tt = string.split()
            full_name = tt[0] + "-" + tt[-1]
            names.append(tt[-1])

            email = full_name + "@Tadweer.sa"
            if email not in emails:
                print("new email added")
            else:
                print("Dublicate catched")
                email = tt[0] + "-" + tt[1] + "@Tadweer.sa"
            emails.append(email)

            print cc
        for i in names:
            print i


def fix():
        # extract_employees_emails3()
        # import_doc(str(get_site_base_path()) +"/private/files/Master - Data To System - Final with Nat.csv")
        # print "ttt>>"
        # pass
        # print getdate("sss")
        # fix_employee_emails()
        # fix_employee_names()
        # fix_employee_salary_structure()

    doc = frappe.new_doc("Fiscal Year Company",
                         frappe.get_doc("Fiscal Year", "2016"))
    doc.company = u"تحكم"
    doc.save()
    frappe.db.commit()


def create_icons():
    users = frappe.get_list("User", "name")
    for index, u in enumerate(users):
        print "========================================"
        print "index: %d" % index
        print "user: %s" % u
        if not frappe.db.exists("Desktop Icon", {"owner": u.name}):
            frappe.get_doc({
                'doctype': 'Desktop Icon',
                'label': "Human Resources",
                'owner': u.name,
                'module_name': "HR",
                'link': None,
                'type': "module",
                '_doctype': None,
                'icon': None,
                'color': None,
                'reverse': 0,
                'custom': 0,
                'standard': 0
            }).insert(ignore_permissions=True)


def import_doc(path, overwrite=False, ignore_links=False, ignore_insert=False, insert=False, submit=False, pre_process=None):
    if os.path.isdir(path):
        files = [os.path.join(path, f) for f in os.listdir(path)]
    else:
        files = [path]

    for f in files:
        if f.endswith(".json"):
            frappe.flags.mute_emails = True
            frappe.modules.import_file.import_file_by_path(
                f, data_import=True, force=True, pre_process=pre_process)
            frappe.flags.mute_emails = False
            frappe.db.commit()
        elif f.endswith(".csv"):
            import_file_by_path(f, ignore_links=ignore_links,
                                overwrite=overwrite, submit=submit, pre_process=pre_process)


def import_file_by_path(path, ignore_links=False, overwrite=False, submit=False, pre_process=None, no_email=True):
    import sys
    from frappe.utils.csvutils import read_csv_content
    from frappe.core.page.data_import_tool.importer import upload
    print "Importing " + path
    with open(path, "r") as infile:
        rows = read_csv_content(infile.read())
        for index, row in enumerate(rows):
            if index != 0:
                # print '----------------------------------'
                # print '----------------------------------'
                # print '----------------------------------'
                # print '----------------------------------'
                # for cindex, cell in enumerate(row):
                # 	print cindex,'->', row[cindex]
                # print '----------------------------------'
                try:
                    print "%"*50
                    print "employee:", row[1]
                    print "index: ", index
                    set_employees_leave(row)
                    frappe.db.commit()
                except:
                    import sys
                    import traceback
                    traceback.print_exc()


def set_employees_leave(row):

    new_name = "EMP%05s" % str(row[0])
    leaves = frappe.get_list("Leave Allocation", filters={
                             "employee": new_name, "leave_type": u"اجازة اعتيادية"}, fields=["name", "new_leaves_allocated"])
    # print "leaves", leaves
    if len(leaves) > 0 and cint(row[2]):
        doc = frappe.get_doc("Leave Allocation", leaves[0].name)
        print "old %s" % doc.new_leaves_allocated
        print "new %s" % cint(row[2])
        doc.new_leaves_allocated = cint(row[2])
        doc.total_leaves_allocated = cint(row[2])
        doc.save(ignore_permissions=True)


exuludes = ["12756", "10013", "10008", "10000", "10001", "12452", "12460", "12521", "10012",
            "12475", "10406", "10759", "10967", "11206", "10011", "12407", "12538", "12738", "10002", "12758"]


def extract_employees_emails2(row):
    if row[1] not in exuludes:
        new_name = "EMP%05s" % str(row[1])
        user_id = frappe.get_value("Employee", new_name, "user_id")
        if user_id:
            user = frappe.rename_doc(
                "User", user_id, row[4], debug=True, ignore_permissions=True)
            frappe.db.sql(
                "update tabUser set email=%s where name=%s", (row[4], row[4]))
            password = str(row[5]).strip()
            if password:
                # user = frappe.db.get_value("User", {"name": empl.user_id})
                _update_password(user, str(row[5]).strip())


def extract_employees_emails3():
    employees = frappe.get_list("Employee", fields=["name", "user_id"])
    for index, empl in enumerate(employees):
        try:
            print "88888888888888888888888888888888"
            print "index: %d" % index
            print "email:"+empl.user_id if empl.user_id else "**"
            if empl.user_id and '@' in empl.user_id and empl.name not in ["EMP%05s" % str(e) for e in exuludes]:
                new_email = empl.user_id.split("@")[0] + '@erp.tahakom.com'
                if not frappe.db.exists("User", new_email):

                    print "new_email:"+new_email
                    user = frappe.rename_doc(
                        "User", empl.user_id, new_email, debug=True, ignore_permissions=True)
                    frappe.db.sql(
                        "update tabUser set email=%s where name=%s", (new_email, new_email))
                    frappe.db.commit()
                # password = str(row[5]).strip()
        except:
            continue


def R0(row):
    r = frappe.new_doc("Region")
    r.region = row[0]
    r.parent_region = "HQ"
    r.save()


excluded_users = ["Administrator", "Guest"]


def fix_employee():
    print "fixing national_id_number"
    frappe.db.sql(
        "UPDATE tabEmployee set national_id_number=civil_identity_number")

    print "fixing passwords"
    employees = frappe.get_list(
        "Employee", fields=["user_id", "civil_identity_number"])

    for index, empl in enumerate(employees):
        if not empl.user_id or empl.user_id in excluded_users:
            continue

        print "index:%d" % index
        print "user_id:"+empl.user_id
        print "password:"+empl.civil_identity_number
        print "---------------------------"
        user = frappe.db.get_value("User", {"name": empl.user_id})
        # doc = frappe.get_doc("User", {"name": empl.user_id})

        # doc.flags.ignore_mandatory = True
        # doc.flags.ignore_save_passwords = True
        # doc.flags.no_welcome_mail = True
        # doc.new_password = empl.civil_identity_number

        _update_password(user, str(empl.civil_identity_number).strip())

        # doc._save_passwords()
        # doc.save()


def add_leave_alocation():
    employees = frappe.get_list("Employee", fields=["name"])
    print len(employees)
    lt = [["Annual Leave - اجازة اعتيادية", 30], ["Compensatory off - تعويضية", 120], ["Death - وفاة", 3], ["Educational - تعليمية", 20],
          ["emergency -اضطرارية", 5], ["Hajj leave - حج", 15], ["Marriage - زواج", 5], ["New Born - مولود جديد", 5], ["Sick Leave - مرضية", 150]]
    for d in employees:
        for l in lt:
            print l[0]
            la = frappe.new_doc('Leave Allocation')
            la.set("__islocal", 1)
            la.employee = cstr(d.name)
            la.employee_name = frappe.db.get_value(
                'Employee', cstr(d.name), 'employee_name')
            la.leave_type = l[0]
            la.from_date = "2017-01-01"
            la.to_date = "2018-01-01"
            la.carry_forward = cint(0)
            la.new_leaves_allocated = flt(l[1])
            la.docstatus = 1
            la.save()
            print la.name
            print d.name


def is_valid_email(email):
    import re
    regex = r"^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$"
    matches = re.search(regex, email, re.IGNORECASE)
    if matches:
        return True
    else:
        return False


def fix_employee_emails():
    print "fixing emails"
    employees = frappe.get_list(
        "Employee", fields=["name", "user_id", "personal_email"])

    for index, empl in enumerate(employees):
        print "+++++++++++++++++++++++++++++++++++++++++++++"
        print "is_valid : " + \
            str(is_valid_email(empl.personal_email)
                if empl.personal_email else "no email")
        if empl.user_id not in ["Administrator", "Guest"] and empl.user_id and empl.personal_email and is_valid_email(empl.personal_email):
            try:
                print "index:%d" % index
                print "user_id:"+empl.user_id
                print "password:"+empl.personal_email

                frappe.rename_doc(
                    "User", empl.user_id, empl.personal_email, debug=True, ignore_permissions=True)
                print "1"
                print "user name  : " + \
                    str(frappe.db.get_value("User", empl.personal_email, "name"))
                frappe.db.sql("UPDATE tabUser set email=%s WHERE name=%s",
                              (empl.personal_email, empl.user_id))
                print "user name  : " + \
                    str(frappe.db.get_value("User", empl.personal_email, "name"))
                frappe.db.commit()
            except:
                continue
        print "-----------------------------------------"
        # doc._save_passwords()
        # doc.save()


def fix_employee_names():
    print "fixing employee_names"
    employees = frappe.get_list(
        "Employee", fields=["name", "employee_identity_number"])

    for index, empl in enumerate(employees):
        if empl.employee_identity_number:
            print "index:%d" % index
            print "user_id:"+empl.name
            print "employee_identity_number:"+empl.employee_identity_number

            try:
                print '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@-'
                new_name = "EMP%05s" % empl.employee_identity_number
                frappe.rename_doc("Employee", empl.name, new_name,
                                  debug=True, ignore_permissions=True)
                print new_name

            except:
                continue
        # doc._save_passwords()
        # doc.save()


def fix_employee_salary_structure():
    print "fixing salary_structure"
    ss_employees = frappe.get_list(
        "Salary Structure Employee", fields=["parent", "employee"])

    for index, ss_empl in enumerate(ss_employees):
        print '---------------------------------'
        print 'index :%d' % index
        print 'employee: '+ss_empl.employee
        try:
            ss_old_name = ss_empl.parent
            ss_new_name = ss_empl.employee+"-Salary Structure"
            frappe.rename_doc("Salary Structure", ss_old_name,
                              ss_new_name, debug=True, ignore_permissions=True)

        except:
            continue
