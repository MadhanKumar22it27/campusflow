import frappe

def create_student_on_approval(doc, method):
    if doc.status == "Approved":
        if not frappe.db.exists("Student", {"student_name": doc.applicant_name}):
            student = frappe.get_doc({
                "doctype": "Student",
                "student_name": doc.applicant_name,
                "program": doc.program,
                "parent_name": doc.parent_name,
                "contact_number": doc.contact_number
            })
            student.insert(ignore_permissions=True)

@frappe.whitelist(allow_guest=True)
def get_student_fee(student):
    payments = frappe.get_all(
        "Fee Payment",
        filters={"student": student},
        fields=["amount_paid"]
    )

    total = sum(p.amount_paid for p in payments)
    return total