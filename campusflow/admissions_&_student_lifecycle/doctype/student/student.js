// Copyright (c) 2026, Madhan and contributors
// For license information, please see license.txt

frappe.ui.form.on("Student", {
	refresh: function (frm) {
		let roles = frappe.user_roles;

		// 🔹 Always enforce default state
		if (roles.includes("Student") || roles.includes("Teacher")) {
			frm.set_df_property("course_selection", "read_only", 1);

			frm.fields_dict.course_selection.grid.update_docfield_property(
				"course",
				"read_only",
				1
			);

			frm.refresh_field("course_selection");
		}

		// 🔹 Add button ONLY ONCE
		if (roles.includes("Teacher") && !frm.custom_buttons_added) {
			frm.add_custom_button("Course Change", function () {
				frm.set_value("allow_course_edit", 1);

				// Enable editing
				frm.set_df_property("course_selection", "read_only", 0);

				frm.fields_dict.course_selection.grid.update_docfield_property(
					"course",
					"read_only",
					0
				);

				frm.refresh_field("course_selection");

				frappe.msgprint("You can now edit courses. Save to apply changes.");
			});

			frm.custom_buttons_added = true; // prevent duplicates
		}
	},

	after_save: function (frm) {
		let roles = frappe.user_roles;

		if (roles.includes("Teacher")) {
			frm.set_df_property("course_selection", "read_only", 1);

			frm.fields_dict.course_selection.grid.update_docfield_property(
				"course",
				"read_only",
				1
			);

			frm.refresh_field("course_selection");
		}
	},
});
