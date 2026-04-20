# Copyright (c) 2026, Madhan and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class AdmissionApplication(Document):
	def validate(self):
		if self.is_new() and not self.course_selection:
			return

		settings = frappe.get_single("CampusFlow Settings")

		min_courses = settings.minimum_courses or 1
		courses = [row.course for row in self.course_selection if row.course]

		# 🔹 Minimum check
		if len(courses) < min_courses:
			frappe.throw(f"You must select at least {min_courses} courses")

		# 🔹 Duplicate check
		if len(courses) != len(set(courses)):
			frappe.throw(_("Duplicate courses are not allowed"))

		# 🔹 Program validation
		for course in courses:
			course_program = frappe.get_value("Course", course, "program")

			if course_program != self.program:
				frappe.throw(f"Course {course} does not belong to Program {self.program}")

	def after_insert(self):
		self.set_course_selection()

	def set_course_selection(self):
		if not self.program:
			return

		courses = frappe.get_list("Course", filters={"program": self.program}, fields=["name"], limit=5)

		if not courses:
			return

		self.set("course_selection", [{"course": c.name} for c in courses])

		self.save(ignore_permissions=True)
