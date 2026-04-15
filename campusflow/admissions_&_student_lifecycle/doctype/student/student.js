// Copyright (c) 2026, Madhan and contributors
// For license information, please see license.txt

frappe.ui.form.on("Student", {
	refresh: function (frm) {
		if (!frm.is_new()) {
			frm.add_custom_button(
				__("Request Course Change"),
				() => {
					frappe.new_doc("Course Change Request", {
						student: frm.doc.name,
						current_course: frm.doc.course,
					});
				},
				__("Actions")
			);
		}
	},
});
