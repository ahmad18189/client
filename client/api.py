# -*- coding: utf-8 -*-
# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
import json
from frappe.utils import cint, getdate, formatdate,get_datetime
from datetime import tzinfo, timedelta, datetime
from dateutil import parser
from datetime import date
from dateutil.relativedelta import relativedelta
from frappe.utils import cint, cstr, flt, nowdate, comma_and, date_diff, getdate, get_datetime
import datetime



def hooked_leave_allocation_builder():
    length=frappe.db.sql("select count(name) from `tabEmployee` where status!='left'")
    emp=frappe.db.sql("select name,date_of_joining,employee_name,department,emp_nationality,work_days from `tabEmployee` where status!='left'")
    c=0
    for i in range(length[0][0]):
        leave_allocation=frappe.db.sql("select from_date,to_date from `tabLeave Allocation` where employee='{0}' order by creation desc ".format(emp[i][0]))
        if leave_allocation:

            if str(datetime.date.today()) > str(leave_allocation[0][1]):
                next_allocation = datetime.datetime.strptime(str(leave_allocation[0][1]), '%Y-%m-%d')

                frappe.get_doc({
                    "doctype":"Leave Allocation",
                    "employee": emp[i][0],
                    "employee_name": emp[i][2],
                    "department": emp[i][3],
                    "leave_type": 'Annual Leave - اجازة اعتيادية',
                    "from_date": date(next_allocation.year, next_allocation.month, next_allocation.day) + relativedelta(days=+1),
                    "to_date": date(next_allocation.year, next_allocation.month, next_allocation.day) + relativedelta(days=+1,years=+10),
                    "carry_forward": cint(1),
                    "new_leaves_allocated": 0,
                    "docstatus": 1
                }).insert(ignore_permissions=True)

                print leave_allocation[0][0],leave_allocation[0][1]
                c+=1
        
        else:

            first_allocation = datetime.datetime.strptime(str(emp[i][1]), '%Y-%m-%d')
            next_first_allocation= date(first_allocation.year, first_allocation.month, first_allocation.day) + relativedelta(years=+0)
            next_second_allocation= date(first_allocation.year, first_allocation.month, first_allocation.day) + relativedelta(years=+10)

            if str(datetime.date.today()) > str(next_first_allocation):
                frappe.get_doc({
                    "doctype":"Leave Allocation",
                    "employee": emp[i][0],
                    "employee_name": emp[i][2],
                    "department": emp[i][3],
                    "leave_type": 'Annual Leave - اجازة اعتيادية',
                    "from_date": next_first_allocation,
                    "to_date": next_second_allocation,
                    "carry_forward": cint(1),
                    "new_leaves_allocated": 0,
                    "docstatus": 1
                }).insert(ignore_permissions=True)


    print 'Count ',c





def increase_leave_balance():
    length=frappe.db.sql("select count(name) from `tabEmployee` where status!='left'")
    emp=frappe.db.sql("select name,work_days,designation from `tabEmployee` where status!='left'")
    leaves=0
    for i in range(length[0][0]):
    	if emp[i][2]=='فني':
    		leaves = 18
    	else:
    		leaves = emp[i][1]
        deserved_leave = round(flt(leaves)/12, 2)
        allocation = frappe.db.sql("select name from `tabLeave Allocation` where employee='{0}' order by creation desc limit 1".format( emp[i][0]))
        if allocation:
            if str(frappe.utils.get_last_day(nowdate())) == str(nowdate()):
                doc = frappe.get_doc('Leave Allocation', allocation[0][0])
                doc.new_leaves_allocated += deserved_leave
                doc.flags.ignore_validate = True
                doc.save(ignore_permissions=True)
                print 'Done'
                



@frappe.whitelist(allow_guest=True)
def make_attendance(data,mac =None):
	print(data)
	frappe.flags.ignore_permissions = True
	if not data:
		return "No Data"
	row_data = json.loads(data)
	#~ print (row_data)
	#~ print type(row_data)
	for row in row_data:
		user_id= row.get("user_id", "none")
		status= row.get("status", "none")
		print (row.get("user_id", "none"))
		print get_datetime(row.get("timestamp", "none"))
		print type(get_datetime(row.get("timestamp", "none")))
		
		timestamp = get_datetime(row.get("timestamp", "none"))
		#~ employee = frappe.get_list('Employee', fields=["name"] , filters={"personal_number":user_id]})
		#~ employee = frappe.get_list('Employee', fields=['name'], filters={ "personal_number":user_id })
		employee = frappe.db.sql("""select name from `tabEmployee` where personal_number = '%s' """%user_id, as_dict=1)
		if employee:
			print ("found employee")
			print employee[0].name
		
		
			attendance_list = frappe.db.sql( """select name from `tabAttendance` where employee = '%s' and attendance_date = '%s'"""%(employee[0].name,timestamp.date() ))	
			if attendance_list:				
				attendance_name = attendance_list[0][0]
			else:
				try:
					attendance = frappe.new_doc("Attendance")
					attendance.attendance_date = timestamp.date()
					attendance.employee = employee[0].name
					attendance.insert(ignore_permissions=True)
					attendance_name = attendance.name
					print ("Insert ",attendance_name)
				except:
					attendance_name="In Valid"
					print ("Bad Insert ",attendance_name)
					
			if attendance_name and attendance_name !="In Valid":
				attendance_list = frappe.db.sql( """select name from `tabAttendance Movement` where parent = '%s' and status = '%s'"""%(attendance_name,status))
				if not attendance_list:
					
					attendance_doc = frappe.get_doc('Attendance',attendance_name)
					print attendance_doc
					print attendance_doc.name
					print attendance_doc
					child = attendance_doc.append('attendance_movement', {})
					child.serial = attendance_name
					#~ child.move_type = move_type
					if status== 1:
						state = 'Check In'
					elif status == 0:
						state = 'Check Out'
					else:
						state = 'Undefined'
					child.move_type = state
					child.time = timestamp
					child.status = status
					if mac :
						child.mach_no= mac
					#~ child.mach_no = row[5]
					attendance_doc.save(ignore_permissions=True)	
		else:
			print ("not found employee")

			


			
			
	return "done"





