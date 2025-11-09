import unittest
from app.services import roi

class TestROI(unittest.TestCase):
    def test_dead_stock(self):
        self.assertEqual(roi.calc_dead_stock_savings(5000, 0.02), 100.0)

    def test_stockouts(self):
        self.assertEqual(roi.calc_stockout_avoided_loss(8, 35.0), 280.0)

    def test_promo_bleed(self):
        self.assertEqual(roi.calc_promo_bleed_reduction(12000.0, 0.10, 0.16, 0.5), 360.0)

    def test_alerts(self):
        alerts = [{"level":"critical"},{"level":"warning"},{"level":"info"}]
        self.assertEqual(roi.calc_alert_savings(alerts), 105.0)

    def test_summary_total(self):
        s = roi.monthly_roi_summary(alerts=[{"level":"info"}])
        self.assertAlmostEqual(s["total_protected_usd"], 100.0 + 280.0 + 360.0 + 5.0, places=2)

if __name__ == '__main__':
    unittest.main()
