import frappe
from frappe.utils import getdate, nowdate


def check_low_attendance():
	print("Checking attendance...")

	threshold = frappe.db.get_single_value("CampusFlow Settings", "attendance_threshold") or 75

	students = frappe.get_all("Student", pluck="name")

	for student in students:
		records = frappe.get_all("Attendance Detail", filters={"student": student}, fields=["status"])

		total = len(records)
		present = len([r for r in records if r.status == "Present"])

		if total == 0:
			continue

		percentage = (present / total) * 100

		print(f"{student} → {percentage:.2f}%")

		if percentage < threshold:
			send_alert(student, percentage)


def send_alert(student, percentage):
	student_doc = frappe.get_doc("Student", student)

	email = student_doc.get("parent_email_id")

	if not email:
		print(f"No email for {student}")
		return

	frappe.sendmail(
		recipients=[email],
		subject="Low Attendance Alert",
		message=f"""
        Dear Parent,

        Your child's attendance has dropped to {percentage:.2f}%.

        Please ensure regular attendance.

        Regards,
        CampusFlow
        """,
	)

	print(f"Alert sent for {student}")
