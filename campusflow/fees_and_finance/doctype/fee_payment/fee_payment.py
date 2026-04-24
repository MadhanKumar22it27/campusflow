# Copyright (c) 2026, Madhan and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class FeePayment(Document):
	def validate(self):
		# Fetch total fee
		if self.fee_structure:
			self.total_fee = frappe.db.get_value("Fee Structure", self.fee_structure, "total_fee")

		if not self.amount_paid:
			self.amount_paid = 0

		if self.total_fee:
			self.remaining_amount = self.total_fee - self.amount_paid

			if self.remaining_amount <= 0:
				self.status = "Paid"
				self.remaining_amount = 0
			elif self.amount_paid == 0:
				self.status = "Pending"
			else:
				self.status = "Partial"
