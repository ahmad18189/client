# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "client"
app_title = "client to all customer"
app_publisher = "ahmed zaqout and abedelrhman"
app_description = "client to all customer"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "ahmedzaqout@outlook.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
app_include_css = ['/assets/client/css/desk.css',"/assets/client/js/c3/c3.min.css"]
app_include_js = ["/assets/client/js/c3/c3.min.js"]
website_context = {
	"favicon": 	"/assets/client/images/logo_new.png",
	"splash_image": "/assets/client/images/logo_new.png"
# 	# "favicon": 	"/assets/erpnext/images/favicon.png",
# 	# "splash_image": "/assets/erpnext/images/erp-icon.svg"
}
# include js, css files in header of web template
# web_include_css = "/assets/client/css/client.css"
# web_include_js = "/assets/client/js/client.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "client.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "client.install.before_install"
# after_install = "client.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "client.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"client.tasks.all"
# 	],
# 	"daily": [
# 		"client.tasks.daily"
# 	],
# 	"hourly": [
# 		"client.tasks.hourly"
# 	],
# 	"weekly": [
# 		"client.tasks.weekly"
# 	]
# 	"monthly": [
# 		"client.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "client.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "client.event.get_events"
# }
fixtures = ["Custom Script","Custom Field"]
