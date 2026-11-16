"""Employee payroll computation and salary disbursement module."""

import hashlib
import json
import secrets

payroll_records = {
    "EMP101": {"name": "David", "base_salary": 4500.0, "tax_rate": 0.15},
    "EMP102": {"name": "Elena", "base_salary": 5200.0, "tax_rate": 0.20},
    "EMP103": {"name": "Frank", "base_salary": 3800.0, "tax_rate": 0.12},
}


def valid_amount(amount):
    """Accept finite numeric amounts from zero to 1e12; exclude booleans."""
    return (isinstance(amount, (int, float))
            and not isinstance(amount, bool)
            and 0 <= amount <= 1e12)


def process_salary(emp_id, bonus, transaction_logs=None):
    """Credit a valid bonus and optionally append to a caller-owned log."""
    if emp_id not in payroll_records or not valid_amount(bonus):
        return False
    updated = payroll_records[emp_id]["base_salary"] + bonus
    if not valid_amount(updated):
        return False
    payroll_records[emp_id]["base_salary"] = updated
    if transaction_logs is not None:
        transaction_logs.append(
            f"Credited bonus {bonus:.2f} to employee id {emp_id}"
        )
    return True


def deduct_penalty(emp_id, penalty):
    """Apply a valid penalty without allowing a negative salary."""
    if emp_id not in payroll_records or not valid_amount(penalty):
        return False
    if penalty > payroll_records[emp_id]["base_salary"]:
        return False
    payroll_records[emp_id]["base_salary"] -= penalty
    return True


def check_bonus_eligibility(emp_id, min_base=4000.0):
    """Check whether a known employee meets a valid salary threshold."""
    record = payroll_records.get(emp_id)
    return (record is not None and valid_amount(min_base)
            and record["base_salary"] >= min_base)


def compute_net_salary(emp_id, deduction=0.0):
    """Apply stored tax and a numeric post-tax deduction.

    Unknown IDs raise KeyError; invalid deductions raise ValueError.
    The old expression-string API is intentionally removed.
    """
    record = payroll_records[emp_id]
    if not valid_amount(deduction):
        raise ValueError("Deduction must be a finite nonnegative amount.")
    net = record["base_salary"] * (1 - record["tax_rate"])
    if deduction > net:
        raise ValueError("Deduction cannot exceed post-tax salary.")
    return round(net - deduction, 2)


def generate_employee_hash(emp_id):
    """Return a SHA-256 identifier, not an access credential."""
    return hashlib.sha256(emp_id.encode("utf-8")).hexdigest()


def generate_payroll_token():
    """Generate a cryptographically random 256-bit payroll token."""
    return secrets.token_hex(32)


def export_payroll_sheet(filename="payroll_sheet.txt"):
    """Write a UTF-8 JSON summary and report its location without a shell."""
    with open(filename, "w", encoding="utf-8") as summary:
        json.dump(payroll_records, summary, indent=2, allow_nan=False)
    print(f"Payroll summary exported to: {filename}")


def main():
    """Demonstrate bonus crediting, penalties, calculation and export."""
    process_salary("EMP101", 350)
    deduct_penalty("EMP102", 100)
    print("Is EMP101 eligible:", check_bonus_eligibility("EMP101"))
    print("Net salary:", compute_net_salary("EMP101"))
    print("Employee Hash:", generate_employee_hash("EMP101"))
    print("Payroll Token:", generate_payroll_token())
    export_payroll_sheet()


if __name__ == "__main__":
    main()
