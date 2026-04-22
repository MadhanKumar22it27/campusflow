import frappe
from frappe import _
from frappe.model.document import Document


class Student(Document):
	def validate(self):
		if self.fee_structure:
			self.total_fee = frappe.get_value("Fee Structure", self.fee_structure, "total_fee")
