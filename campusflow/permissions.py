import frappe


def student_query(user):
	roles = frappe.get_roles(user)

	if "Campus Admin" in roles:
		return ""

	if "Teacher" in roles:
		return ""

	if "Parent" in roles:
		return f"`tabStudent`.parent_name = {frappe.db.escape(user)}"

	return ""
