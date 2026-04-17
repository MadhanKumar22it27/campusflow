// Copyright (c) 2026, Madhan and contributors
// For license information, please see license.txt

frappe.ui.form.on("Student", {
	refresh(frm) {
		// Always keep original table read-only
		frm.set_df_property("course_selection", "read_only", 1);

		if (frappe.user.has_role("Teacher")) {
			frm.add_custom_button("Course Change", () => {
				let course_data = (frm.doc.course_selection || []).map((row) => {
					return {
						course: row.course,
					};
				});

				let d = new frappe.ui.Dialog({
					title: "Edit Courses",
					size: "large",
					fields: [
						{
							fieldname: "courses",
							fieldtype: "Table",
							label: "Courses",
							in_place_edit: true,
							editable_grid: 1,
							cannot_add_rows: false,
							reqd: 1,
							fields: [
								{
									fieldname: "course",
									label: "Course",
									fieldtype: "Link",
									options: "Course",
									in_list_view: 1,
									reqd: 1,
								},
							],
						},
					],

					primary_action_label: "Save",
					primary_action(values) {
						if (!values.courses || values.courses.length === 0) {
							frappe.msgprint("At least one course is required");
							return;
						}

						// 🔥 Call backend API instead of frm.save()
						frappe.call({
							method: "campusflow.api.update_student_courses",
							args: {
								student: frm.doc.name,
								courses: values.courses,
							},
							callback: function () {
								frappe.show_alert({
									message: "Courses updated successfully",
									indicator: "green",
								});

								frm.reload_doc(); // refresh data from backend
							},
						});

						d.hide();
					},
				});

				d.show();

				// Inject existing data into dialog table
				let table = d.fields_dict.courses;
				table.df.data = course_data;
				table.grid.refresh();

				// UX polish
				setTimeout(() => {
					d.$wrapper.find(".grid-body").css({
						"max-height": "300px",
						"overflow-y": "auto",
					});
				}, 200);
			});
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
