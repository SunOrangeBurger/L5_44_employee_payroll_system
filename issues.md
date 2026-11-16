# Lab 5 - Documented Issues

Line numbers refer to evidence/original_employee_payroll_system.py. Tool severity is retained; manual severities are contextual assessments.

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---|---|---|
| High: Weak employee hash | Security / Bandit B324 | 47 | MD5 is unsuitable for security-sensitive hashing. | Use SHA-256; clarify that an employee-ID hash is not an authentication credential. |
| High: Shell command injection | Security / Bandit B605 | 58 | The export filename is concatenated into a shell command. | Remove os.system and print the confirmation directly. |
| High (manual): Secret embedded and printed | Security / manual review | 62, 70 | A master secret is stored in source and disclosed in the demo output. | Remove the unused secret and its print statement. A real deployed secret would need rotation. |
| Medium: Arbitrary code execution | Security / B307, W0123 | 40-43 | eval executes arbitrary Python supplied as a deduction expression. | Replace expression strings with a validated numeric post-tax deduction and stored tax rate. |
| Medium (manual): Penalty validation missing | Correctness / manual review | 23-27 | Negative penalties increase salary; excessive penalties make it negative. Unknown IDs are silently ignored. | Validate numeric amounts and employee IDs, reject overdraws, and return an explicit success flag. |
| Medium (manual): Invalid bonus amounts | Correctness / manual review | 15-20 | NaN, infinity and boolean bonuses can bypass the original negative-only check. | Accept only non-boolean numbers in the documented range 0 through 1e12; validate the updated balance. |
| Low: Exceptions swallowed | Reliability / B110, W0702 | 24-27 | A bare except hides every error and gives callers no result. | Use explicit validation rather than a blanket exception handler. |
| Low: Predictable short token | Security / Bandit B311 | 50-51 | random.randint offers just 9,000 token values and is not a cryptographic generator. | Generate 32 random bytes with secrets.token_hex(32). |
| Low: Shared default log and rounding | Correctness / W0102 + manual | 15, 19 | The default list persists between calls and %d truncates fractional bonuses. | Use None by default, append only to a supplied log, and format amounts to two decimals. |
| Low: Unmanaged export file | Reliability / W1514, R1732 | 54-57 | File closure is not guaranteed on a write error; encoding is implicit. | Use a with block, UTF-8, and structured JSON output. |
| Low: Style and import side effects | Maintainability / Pylint, Flake8, manual | 6, 15, 30-37, 73 | Unused names, missing docstrings, camelCase and import-time demo execution reduce clarity. | Remove dead code, document functions, use process_salary and guard main. |
