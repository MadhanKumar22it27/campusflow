import frappe
def process_fee_background(student):
    frappe.logger().info(f"Processing fee for {student}")

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
        filters={"student": student, "docstatus": 1},
        fields=["amount_paid"]
    )

    total = sum([p.amount_paid for p in payments])

    return {
        "student": student,
        "total_paid": total,
        "payment_count": len(payments)
    }

@frappe.whitelist()
def get_pending_fees():
    total_fee = frappe.db.sql("""
        SELECT SUM(total_fee) FROM `tabFee Structure`
    """)[0][0] or 0

    paid = frappe.db.sql("""
        SELECT SUM(amount_paid) 
        FROM `tabFee Payment` 
        WHERE docstatus = 1
    """)[0][0] or 0

    pending = total_fee - paid

    # prevent negative values
    if pending < 0:
        pending = 0

    return {
        "value": pending,
        "fieldtype": "Currency"
    }