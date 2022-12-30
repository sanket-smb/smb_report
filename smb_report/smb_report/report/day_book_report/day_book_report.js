// Copyright (c) 2016, SMB and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Day Book Report"] = {
	"filters": [
		{
			"fieldname":"date",
			"label": __("Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
			"reqd": 1
		}
	]
};
