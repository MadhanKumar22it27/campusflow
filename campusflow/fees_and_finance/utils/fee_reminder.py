import frappe
from frappe.utils import nowdate


def enqueue_fee_reminders():
	frappe.enqueue("campusflow.fees.utils.fee_reminder.send_fee_reminders", queue="long")


# def send_fee_reminders():
#     fees = frappe.get_all(
#         "Fee Payment",
#         filters={
#             "docstatus": 1,
#             "status": ["!=", "Paid"],
#             "remaining_amount": [">", 0]
#         },
#         fields=[
#             "name",
#             "student",
#             "remaining_amount",
#             "last_reminder_date"
#         ]
#     )

#     print("Running Fee Reminder Job...")
#     for fee in fees:
#         if fee.last_reminder_date == nowdate():
#             continue

#         student = frappe.get_doc("Student", fee.student)

#         email = student.get("parent_email_id")

#         if not email:
#             continue

#         frappe.sendmail(
#             recipients=[email],
#             subject="Fee Payment Reminder",
#             message=f"""
#             Dear Parent,

#             This is a reminder that the fee payment is still pending.

#             Remaining Amount: ₹{fee.remaining_amount}

#             Kindly complete the payment at the earliest.

#             Regards,
#             CampusFlow
#             """
#         )

#         frappe.db.set_value(
#             "Fee Payment",
#             fee.name,
#             "last_reminder_date",
#             nowdate()
#         )


def send_fee_reminders():
	print(" Function triggered")

	fees = frappe.get_all(
		"Fee Payment", filters={"docstatus": 1, "status": ["!=", "Paid"]}, fields=["name", "student"]
	)

	print(f" Found {len(fees)} records")

	for fee in fees:
		print(f"Processing {fee.name}")

		student = frappe.db.get_value("Student", fee.student, ["parent_email_id", "user_id"], as_dict=True)

		if not student:
			print(" Student not found")
			continue

		email = student.get("parent_email_id")

		if not email:
			print(f" No email for student {fee.student}")
			continue

		try:
			frappe.sendmail(
				recipients=[email],
				subject="Fee Reminder",
				message=f"Pending fee for student {fee.student}",
				delayed=False,
			)

			print(f" Email sent to {email}")

		except Exception as e:
			print(f" Failed to send email: {e}")
