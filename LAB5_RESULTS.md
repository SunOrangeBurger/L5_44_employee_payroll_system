# Lab 5 results

Original revision: 49e763f20d58c14f27d451f95c75ee996fa18af6

Pylint: 5.32/10 -> 10.00/10. Bandit: 5 findings (2 high, 1 medium, 2 low) -> 0. Flake8: 7 findings -> 0. Regression tests: 8 passed.

Run from this directory after installing requirements.txt:

```text
python employee_payroll_system.py
python -m pylint --persistent=n employee_payroll_system.py
python -m bandit -r employee_payroll_system.py
python -m flake8 employee_payroll_system.py
python -m unittest -v test_employee_payroll_system.py
```

The README mentions an input prompt; the supplied source has none. Its fixed demo was run instead. Reflection questions were omitted at the student's request.

API changes: processSalary is renamed process_salary; compute_net_salary now accepts a numeric deduction, uses the employee's tax rate and rounds to two decimals. Invalid mutations return False; invalid deductions raise ValueError; unknown salary lookup raises KeyError. Export uses JSON. Amounts must be non-boolean numbers from 0 to 1e12. SHA-256 IDs are not credentials. This educational program keeps mutable in-memory balances and floating-point arithmetic; a production payroll system would require stronger accounting and persistence controls.

Original source and before/after command logs are in evidence/. Only employee_payroll_system.py is the target for the three static analyzers. No suppressions were added. No remote push was performed.
