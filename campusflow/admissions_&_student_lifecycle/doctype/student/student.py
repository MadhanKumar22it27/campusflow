import frappe
from frappe import _
from frappe.model.document import Document


class Student(Document):
	def before_save(self):
		roles = frappe.get_roles(frappe.session.user)

		if "Teacher" in roles:
			if not self.allow_course_edit:
				# Check if child table modified
				old_doc = self.get_doc_before_save()

				if old_doc and old_doc.course_selection != self.course_selection:
					frappe.throw(_("You are not allowed to modify courses"))

		self.allow_course_edit = 0
