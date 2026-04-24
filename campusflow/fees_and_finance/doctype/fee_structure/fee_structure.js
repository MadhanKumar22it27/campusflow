// Copyright (c) 2026, Madhan and contributors
// For license information, please see license.txt

frappe.ui.form.on("Fee Structure", {
	default(frm) {
		if (!frm.doc.default) return;

		frappe.db
			.get_value(
				"Fee Structure",
				{
					program: frm.doc.program,
					default: 1,
					name: ["!=", frm.doc.name],
				},
				"name"
			)
			.then((r) => {
				if (!r.message) return;

				frappe.confirm(
					__("Another default exists. Replace it?"),
					() => {
						frappe.db.set_value("Fee Structure", r.message.name, "default", 0);
						frm.save();
					},
					() => {
						frm.set_value("default", 0);
						frm.save();
					}
				);
			});
	},
});
