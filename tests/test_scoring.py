import math
import unittest
from scripts.score_opportunities import WEIGHTS, score, decision
from scripts.calculate_profit import profit
from scripts.normalize_research import normalize
from scripts.generate_reports import report

class TestScoring(unittest.TestCase):
    def setUp(self):
        self.ratings = {key: 10 for key in WEIGHTS}
    def test_weights(self):
        self.assertEqual(sum(WEIGHTS.values()), 100)
    def test_perfect(self):
        self.assertEqual(score(self.ratings), 100)
    def test_zero(self):
        self.assertEqual(score({key: 0 for key in WEIGHTS}), 0)
    def test_missing_factor(self):
        with self.assertRaises(ValueError): score({})
    def test_invalid_ratings(self):
        for bad in (-1, 11, True, "8", math.nan, math.inf, -math.inf):
            with self.subTest(value=bad):
                with self.assertRaises(ValueError): score({**self.ratings, "buyer_demand": bad})
    def test_decision_boundaries(self):
        self.assertEqual(decision(80), "PRIORITIZE VALIDATION")
        self.assertEqual(decision(65), "TEST")
        self.assertEqual(decision(50), "WATCH")
        self.assertEqual(decision(49.99), "SKIP")
        self.assertEqual(decision(99, False), "SKIP: compliance gate")
    def test_invalid_decision(self):
        with self.assertRaises(ValueError): decision(float("nan"))
        with self.assertRaises(ValueError): decision(80, "false")
    def test_profit(self):
        self.assertLess(profit(10)["net_profit"], 10)
        self.assertAlmostEqual(profit(10, production=1, ads=0.5)["net_profit"], 7.65)
    def test_invalid_profit(self):
        for kwargs in ({"price": 0}, {"price": -1}, {"price": 10, "ads": -2}, {"price": 10, "payment_rate": float("nan")}, {"price": 10, "transaction_rate": 1.1}):
            with self.subTest(kwargs=kwargs):
                with self.assertRaises(ValueError): profit(**kwargs)
    def test_profit_overflow_rejected(self):
        for kwargs in ({"price": 1e308, "production": 1e308, "shipping": 1e308}, {"price": 1e-308, "production": 1e308}):
            with self.subTest(kwargs=kwargs):
                with self.assertRaises(ValueError): profit(**kwargs)
    def test_normalization_preserves_unknown(self):
        self.assertIsNone(normalize({"product": " Sample "})["price_usd"])
        self.assertIsNone(normalize({"product": " Sample "})["observed_at"])
        self.assertEqual(normalize({"product": " Sample "})["product"], "Sample")
    def test_normalization_rejects_invalid_fields(self):
        for item in (None, [], {"product": 123}, {"confidence": "UNVERIFIED"}):
            with self.subTest(item=item):
                with self.assertRaises(ValueError): normalize(item)
    def test_report_missing_evidence(self):
        self.assertIn("No verified evidence supplied", report({"name": "Example"}))

if __name__ == "__main__":
    unittest.main()
