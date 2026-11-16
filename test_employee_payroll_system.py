"""Behavioral regressions for the payroll repairs."""

import copy
import importlib.util
import io
import json
from contextlib import redirect_stdout
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

import employee_payroll_system as payroll


class PayrollTests(unittest.TestCase):
    """Check arithmetic, rejected inputs, isolation and file export."""

    def setUp(self):
        self.saved = copy.deepcopy(payroll.payroll_records)

    def tearDown(self):
        payroll.payroll_records.clear()
        payroll.payroll_records.update(self.saved)

    def test_demo_arithmetic(self):
        logs = []
        self.assertTrue(payroll.process_salary('EMP101', 350.25, logs))
        self.assertIn('350.25', logs[0])
        self.assertTrue(payroll.deduct_penalty('EMP102', 100))
        self.assertEqual(payroll.compute_net_salary('EMP101'), 4122.71)
        self.assertEqual(payroll.compute_net_salary('EMP102', 80), 4000)

    def test_invalid_mutations_leave_records_unchanged(self):
        for amount in (-1, float('nan'), float('inf'), True, '100', 1e13):
            with self.subTest(amount=amount):
                self.assertFalse(payroll.process_salary('EMP101', amount))
                self.assertFalse(payroll.deduct_penalty('EMP101', amount))
        self.assertFalse(payroll.deduct_penalty('EMP101', 4501))
        self.assertFalse(payroll.process_salary('UNKNOWN', 100))
        self.assertFalse(payroll.deduct_penalty('UNKNOWN', 100))
        self.assertEqual(payroll.payroll_records, self.saved)

    def test_zero_salary_and_eligibility_boundary(self):
        self.assertTrue(payroll.check_bonus_eligibility('EMP101', 4500))
        self.assertFalse(payroll.check_bonus_eligibility('EMP101', 4500.01))
        self.assertFalse(payroll.check_bonus_eligibility('UNKNOWN'))
        self.assertTrue(payroll.deduct_penalty('EMP101', 4500))
        self.assertEqual(payroll.compute_net_salary('EMP101'), 0)

    def test_expressions_and_excess_deductions_rejected(self):
        for deduction in ('base * 0.85', -1, float('nan'), 4500):
            with self.subTest(deduction=deduction):
                with self.assertRaises(ValueError):
                    payroll.compute_net_salary('EMP101', deduction)
        with self.assertRaises(KeyError):
            payroll.compute_net_salary('UNKNOWN')

    def test_independent_transaction_logs(self):
        first, second = [], []
        payroll.process_salary('EMP101', 1, first)
        payroll.process_salary('EMP101', 2)
        payroll.process_salary('EMP101', 3, second)
        self.assertEqual(len(first), 1)
        self.assertEqual(len(second), 1)
        self.assertIn('1.00', first[0])
        self.assertIn('3.00', second[0])

    def test_export_with_shell_metacharacters(self):
        with TemporaryDirectory() as folder:
            target = Path(folder) / 'payroll & summary.txt'
            with redirect_stdout(io.StringIO()):
                payroll.export_payroll_sheet(target)
            self.assertEqual(json.loads(target.read_text()), payroll.payroll_records)

    def test_identifier_and_token_formats(self):
        self.assertEqual(len(payroll.generate_employee_hash('EMP101')), 64)
        self.assertEqual(len(bytes.fromhex(payroll.generate_payroll_token())), 32)

    def test_import_has_no_demo_side_effects(self):
        spec = importlib.util.spec_from_file_location('isolated', payroll.__file__)
        module = importlib.util.module_from_spec(spec)
        capture = io.StringIO()
        with redirect_stdout(capture):
            spec.loader.exec_module(module)
        self.assertEqual(capture.getvalue(), '')
        self.assertEqual(module.payroll_records['EMP101']['base_salary'], 4500)


if __name__ == '__main__':
    unittest.main()
