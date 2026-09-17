import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.data_loader import load_data
from src.task_engine import canonical_tasks, status_for, deadline_status, source_counts

DATA = load_data(Path(__file__).resolve().parents[1] / "data" / "datapack.json")


class TestExecutiveAgent(unittest.TestCase):
    def test_canonical_task_count(self):
        self.assertEqual(len(canonical_tasks(DATA)), 5)

    def test_vendor_dedup(self):
        t = canonical_tasks(DATA)[0]
        self.assertEqual(len(t.source_ids), 7)
        self.assertEqual(source_counts(t)["emails"], 5)

    def test_vendor_overdue_on_thursday(self):
        t = canonical_tasks(DATA)[0]
        self.assertEqual(status_for(t, "2026-09-24"), "MY ACTION")
        self.assertEqual(deadline_status(t, "2026-09-24"), "OVERDUE")

    def test_campaign_dependency_resolves(self):
        t = canonical_tasks(DATA)[1]
        self.assertEqual(status_for(t, "2026-09-23"), "WAITING ON OTHERS")
        self.assertEqual(status_for(t, "2026-09-24"), "MY ACTION")
        self.assertEqual(deadline_status(t, "2026-09-24"), "DUE TODAY")

    def test_expense_report_is_waiting_then_completed(self):
        t = canonical_tasks(DATA)[2]
        self.assertEqual(status_for(t, "2026-09-22"), "WAITING ON OTHERS")
        self.assertEqual(status_for(t, "2026-09-23"), "COMPLETED")

    def test_meridian_call_completed(self):
        t = canonical_tasks(DATA)[3]
        self.assertEqual(status_for(t, "2026-09-23"), "COMPLETED")

    def test_lease_owner_is_unknown(self):
        t = canonical_tasks(DATA)[4]
        self.assertIsNone(t.action_owner)
        self.assertEqual(status_for(t, "2026-09-24"), "UNCLEAR OWNERSHIP")
        self.assertEqual(deadline_status(t, "2026-09-24"), "UPCOMING")


if __name__ == "__main__":
    unittest.main(verbosity=2)
