# Copyright (c) 2026, Madhan and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class AdmissionApplication(Document):
	def validate(self):
		settings = frappe.get_single("CampusFlow Settings")

		min_courses = settings.minimum_courses or 1
		courses = [row.course for row in self.course_selection if row.course]

		# 🔹 1. Minimum check
		if len(courses) < min_courses:
			frappe.throw(f"You must select at least {min_courses} courses")

		# 🔹 2. Duplicate check
		if len(courses) != len(set(courses)):
			frappe.throw("Duplicate courses are not allowed")

		# 🔹 3. Program validation
		for course in courses:
			course_program = frappe.get_value("Course", course, "program")

			if course_program != self.program:
				frappe.throw(f"Course {course} does not belong to Program {self.program}")
