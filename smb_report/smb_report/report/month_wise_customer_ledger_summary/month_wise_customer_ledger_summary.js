// Copyright (c) 2024, SMB and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Month Wise Customer Ledger Summary"] = {
	"onload": function(report) {
        var fiscal_year = erpnext.utils.get_fiscal_year(frappe.datetime.get_today());
        frappe.call({
            method: "frappe.client.get",
            args: {
                doctype: "Fiscal Year",
                name: fiscal_year
            },
            callback: function(r) {
                if (r.message) {
                    var fy = r.message;
                    frappe.query_report.set_filter_value({
                        fiscal_year: fiscal_year,
                        from_date: fy.year_start_date,
                        to_date: fy.year_end_date
                    });
                }
            }
        });
    },
	"filters": [
		{
			"fieldname":"company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": frappe.defaults.get_user_default("Company")
		},
		{
			"fieldname": "fiscal_year",
			"label": __("Fiscal Year"),
			"fieldtype": "Link",
			"options": "Fiscal Year",
			"default": erpnext.utils.get_fiscal_year(frappe.datetime.get_today()),
			"reqd": 1,
			"on_change": function(query_report) {
				var fiscal_year = query_report.get_values().fiscal_year;
				if (!fiscal_year) {
					return;
				}
				frappe.model.with_doc("Fiscal Year", fiscal_year, function(r) {
					var fy = frappe.model.get_doc("Fiscal Year", fiscal_year);
					frappe.query_report.set_filter_value({
						from_date: fy.year_start_date,
						to_date: fy.year_end_date
					});
				});
			}
		},
		{
            "fieldname": "from_date",
            "label": __("From Date"),
            "fieldtype": "Date",
            "reqd": 1,
			"read_only": 1
        },
        {
            "fieldname": "to_date",
            "label": __("To Date"),
            "fieldtype": "Date",
            "reqd": 1,
			"read_only": 1
        },
		{
			"fieldname":"party",
			"label": __("Customer"),
			"fieldtype": "Link",
			"options": "Customer",
			"reqd": 1
		}
	]
};
