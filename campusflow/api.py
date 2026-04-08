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

@frappe.whitelist(allow_guest=True)
def get_attendance(student):
    records = frappe.get_all(
        "Attendance Detail",
        filters={"student": student},
        fields=["status"]
    )

    total = len(records)
    present = len([r for r in records if r.status == "Present"])
    absent = len([r for r in records if r.status == "Absent"])

    return {
        "total_classes": total,
        "present": present,
        "absent": absent,
        "percentage": (present / total * 100) if total > 0 else 0
    }

@frappe.whitelist(allow_guest=True)
def get_student_details(student):
    doc = frappe.get_doc("Student", student)

    return {
        "student_id": doc.name,
        "student_name": doc.student_name,
        "program": doc.program,
        "contact": doc.contact_number,
        "parent": doc.parent_name,
        "total_fee": doc.total_fee
    }

@frappe.whitelist(allow_guest=True)
def get_dashboard_stats():

    students = frappe.get_all("Student", fields=["name", "total_fee"])

    payments = frappe.get_all(
        "Fee Payment",
        filters={"docstatus": 1},
        fields=["student", "amount_paid"]
    )

    payment_map = {}

    for p in payments:
        payment_map.setdefault(p.student, 0)
        payment_map[p.student] += p.amount_paid

    total_students = len(students)
    total_collected = 0
    fully_paid = partially_paid = unpaid = 0
    total_fee = 0

    for s in students:
        paid = payment_map.get(s.name, 0)
        total_collected += paid
        total_fee += s.total_fee or 0

        if paid == 0:
            unpaid += 1
        elif paid < (s.total_fee or 0):
            partially_paid += 1
        else:
            fully_paid += 1

    pending = total_fee - total_collected

    return {
        "total_students": total_students,
        "total_collected": total_collected,
        "pending": pending,
        "fully_paid": fully_paid,
        "partially_paid": partially_paid,
        "unpaid": unpaid
    }