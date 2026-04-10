import frappe


def process_fee_background(student):
	frappe.logger().info(f"Processing fee for {student}")


def create_student_on_approval(doc, method):
	if doc.status == "Approved":
		if not frappe.db.exists("Student", {"student_name": doc.applicant_name}):
			student = frappe.get_doc(
				{
					"doctype": "Student",
					"student_name": doc.applicant_name,
					"program": doc.program,
					"parent_name": doc.parent_name,
					"contact_number": doc.contact_number,
				}
			)
			student.insert(ignore_permissions=True)


@frappe.whitelist()
def get_student_fee(student: str) -> dict:
	payments = frappe.get_all(
		"Fee Payment", filters={"student": student, "docstatus": 1}, fields=["amount_paid"]
	)

	total = sum([p.amount_paid for p in payments])

	return {"student": student, "total_paid": total, "payment_count": len(payments)}


@frappe.whitelist()
def get_attendance(student: str) -> dict:
	records = frappe.get_all("Attendance Detail", filters={"student": student}, fields=["status"])

	total = len(records)
	present = len([r for r in records if r.status == "Present"])
	absent = len([r for r in records if r.status == "Absent"])

	return {
		"total_classes": total,
		"present": present,
		"absent": absent,
		"percentage": (present / total * 100) if total > 0 else 0,
	}


@frappe.whitelist()
def get_student_details(student: str) -> dict:
	doc = frappe.get_doc("Student", student)

	return {
		"student_id": doc.name,
		"student_name": doc.student_name,
		"program": doc.program,
		"contact": doc.contact_number,
		"parent": doc.parent_name,
		"total_fee": doc.total_fee,
	}


@frappe.whitelist()
def get_total_students():
	return frappe.db.count("Student")


@frappe.whitelist()
def get_total_collected():
	result = frappe.db.sql("""
		SELECT IFNULL(SUM(amount_paid), 0)
		FROM `tabFee Payment`
		WHERE docstatus = 1
	""")

	return result[0][0] or 0


@frappe.whitelist()
def get_pending_fees():
	total_fee = frappe.db.sql("""
		SELECT IFNULL(SUM(total_fee), 0)
		FROM `tabStudent`
	""")[0][0]

	collected = frappe.db.sql("""
		SELECT IFNULL(SUM(amount_paid), 0)
		FROM `tabFee Payment`
		WHERE docstatus = 1
	""")[0][0]

	return total_fee - collected


@frappe.whitelist()
def get_fully_paid_students():
	return frappe.db.sql("""
        SELECT COUNT(*) FROM (
            SELECT
                s.name,
                IFNULL(SUM(f.amount_paid), 0) AS paid,
                MAX(s.total_fee) AS total_fee
            FROM `tabStudent` s
            LEFT JOIN `tabFee Payment` f
                ON s.name = f.student AND f.docstatus = 1
            GROUP BY s.name
            HAVING paid >= total_fee
        ) AS t
    """)[0][0]


@frappe.whitelist()
def get_partial_students():
	return frappe.db.sql("""
        SELECT COUNT(*) FROM (
            SELECT
                s.name,
                IFNULL(SUM(f.amount_paid), 0) AS paid,
                MAX(s.total_fee) AS total_fee
            FROM `tabStudent` s
            LEFT JOIN `tabFee Payment` f
                ON s.name = f.student AND f.docstatus = 1
            GROUP BY s.name
            HAVING paid > 0 AND paid < total_fee
        ) AS t
    """)[0][0]


@frappe.whitelist()
def get_unpaid_students():
	return frappe.db.sql("""
        SELECT COUNT(*) FROM (
            SELECT
                s.name,
                IFNULL(SUM(f.amount_paid), 0) AS paid
            FROM `tabStudent` s
            LEFT JOIN `tabFee Payment` f
                ON s.name = f.student AND f.docstatus = 1
            GROUP BY s.name
            HAVING paid = 0
        ) AS t
    """)[0][0]


@frappe.whitelist()
def get_courses_by_program(program: str):
	print("from the backend")

	return frappe.get_list("Course", filters={"program": program}, pluck="course_name")
