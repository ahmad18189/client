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
