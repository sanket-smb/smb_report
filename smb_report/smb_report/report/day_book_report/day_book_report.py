# Copyright (c) 2013, SMB and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from frappe import msgprint, _
import frappe
from frappe.utils import today
from frappe.utils import get_link_to_form

def execute(filters=None):
	columns, data = [], []
	columns = get_columns(filters)
	data = get_data(filters)
	return columns, data

def get_columns(report_filters):
	return [
		_("Date") + ":Date:120", _("Entry Type") + ":Data:170", _("Customer/Supplier")+ ":Data:150",
		_("ID") + ":Data:150", _("Amount") + ":Currency:120",
		_("Net Amount") + ":Currency:120", _("Paid Amount") + ":Currency:100",
		_("Outstanding Amount") + ":Currency:140", _("Mode Of Payment") + ":Data:120",
		_("User Details") + ":Data:120",_("Against") + ":Data:130"
	]	

def get_data(report_filters):
	data = []
	sinv_data = get_sales_invoice(report_filters)
	data.extend(sinv_data)
	pinv_data = get_purchase_invoice(report_filters)
	data.extend(pinv_data)
	pe_data = get_payment_entry(report_filters)
	data.extend(pe_data)
	return sorted(data, key = lambda i: i[11]) 


def get_sales_invoice(report_filters):
	if report_filters.get('date'):
		date = report_filters.get('date')
	else:
		date = today()
	filters = [
		["posting_date","=",date],
		["docstatus","=",1]
	]
	data = []
	inv_details = frappe.get_all("Sales Invoice",filters=filters,fields=["*"])
	for inv in inv_details:
		link = get_link_to_form("Sales Invoice",inv.name)
		invoice_details = frappe.get_doc("Sales Invoice",inv.name)
		row = [inv.posting_date,invoice_details.doctype,inv.customer,link,inv.grand_total,inv.net_total,inv.paid_amount,inv.outstanding_amount,'',inv.owner,'',inv.creation]
		mode_of_payments = ",".join(pay.mode_of_payment for pay in invoice_details.payments)
		row[8] = mode_of_payments
		data.append(row)
	return data

def get_purchase_invoice(report_filters):
	if report_filters.get('date'):
		date = report_filters.get('date')
	else:
		date = today()
	filters = [
		["posting_date","=",date],
		["docstatus","=",1]
	]
	data = []
	inv_details = frappe.get_all("Purchase Invoice",filters=filters,fields=["*"])
	for inv in inv_details:
		link = get_link_to_form("Purchase Invoice",inv.name)
		invoice_details = frappe.get_doc("Purchase Invoice",inv.name)
		row = [inv.posting_date,invoice_details.doctype,inv.supplier,link,inv.grand_total * (-1),inv.net_total * (-1),inv.paid_amount * (-1),inv.outstanding_amount * (-1),inv.mode_of_payment,inv.owner,'',inv.creation]
		data.append(row)
	return data

def get_payment_entry(report_filters):
	if report_filters.get('date'):
		date = report_filters.get('date')
	else:
		date = today()
	filters = [
		["posting_date","=",date],
		["docstatus","=",1],
		["payment_type","in",["Receive","Pay"]]
	]
	data = []
	pe_details = frappe.get_all("Payment Entry",filters=filters,fields=["*"])
	for pe in pe_details:
		link = get_link_to_form("Payment Entry",pe.name)
		pe_data = frappe.get_doc("Payment Entry",pe.name)
		if pe_data.payment_type == "Pay":
			pe.paid_amount = pe.paid_amount * (-1)
		row = [pe.posting_date,pe_data.doctype,pe.party,link,pe.paid_amount,pe.paid_amount,pe.paid_amount,'0',pe.mode_of_payment,pe.owner,'',pe.creation]
		references = ",".join(get_link_to_form(ref.reference_doctype,ref.reference_name) for ref in pe_data.references)
		row[10] = references
		data.append(row)
	return data