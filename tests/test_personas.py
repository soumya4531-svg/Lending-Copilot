"""
tests/test_personas.py
Automated Verification Suite for the Three Canonical Personas:
1. Priya (Salaried MNC, Bengaluru)
2. Ravi (Self-Employed Kirana, Mysuru)
3. Anita (Informal Delivery Fleet, Hubballi)
Plus verification of Rule 2 (Confidence Scaling), Rule 3 (Unknown is Never Zero), and Rule 4 (Every Number Has a Why).
"""

import unittest
from engine.underwriting import (
    calculate_pmt,
    calculate_present_value,
    solve_all_in_apr,
    run_full_underwriting,
)
from engine.confidence import compute_confidence_score, get_spread_half_width
from engine.explanations import generate_all_explanations
from engine.negotiation import build_negotiation_card


class TestBorrowerCopilot(unittest.TestCase):

    def test_pmt_and_pv_consistency(self):
        """Validates that PMT and PV calculations are mathematical inverses."""
        principal = 800000.0
        rate = 11.0
        tenure = 48
        emi = calculate_pmt(rate, tenure, principal)
        self.assertAlmostEqual(emi, 20690.0, delta=100.0)

        recovered_principal = calculate_present_value(rate, tenure, emi)
        self.assertAlmostEqual(recovered_principal, principal, delta=1000.0)

    def test_all_in_apr_with_fees_and_gst(self):
        """Validates that All-In APR captures processing fees + 18% GST and exceeds nominal rate."""
        principal = 800000.0
        tenure = 48
        emi = calculate_pmt(11.0, tenure, principal)
        # 1.0% processing fee + 18% GST = 1.18% fee drag
        apr = solve_all_in_apr(principal, emi, tenure, processing_fee_pct=1.0)
        self.assertGreater(apr, 11.0)
        self.assertAlmostEqual(apr, 11.65, delta=0.25)

    def test_persona_1_priya_salaried(self):
        """
        Priya, 29, Bengaluru · Salaried Tier-1 MNC:
        Net Income: ₹1,10,000/mo, Car loan: ₹14,000/mo, Rent: ₹28,000, Living: ₹25,000,
        CIBIL: 780, Loan Wanted: ₹8,00,000 for wedding over 48 months.
        Expected: Verdict = BORROW, Prime Corporate Personal Loan, APR ~11.65%.
        """
        profile = {
            "employment_type": "Salaried",
            "net_income": 110000,
            "target_loan_amount": 800000,
            "tenure_months": 48,
            "existing_emi": 14000,
            "rent": 28000,
            "living_expenses": 25000,
            "cibil": "750+",
            "age": 29,
            "employer_tier": "Listed Tier-1 Corporate/MNC",
            "job_vintage_years": 5.0,
            "liquid_savings_months": 8.0,
            "quoted_processing_fee_pct": 1.0
        }

        calc = run_full_underwriting(profile)
        explanations = generate_all_explanations(profile, calc)
        card = build_negotiation_card(profile, calc)

        # Assertions
        self.assertEqual(calc["verdict"], "BORROW")
        self.assertIn("Prime", calc["target_product"])
        self.assertTrue(10.0 <= calc["rate_min"] <= 11.5)
        self.assertAlmostEqual(calc["all_in_apr"], 11.65, delta=0.5)
        self.assertGreater(calc["borrower_safe_limit"], 800000)
        self.assertTrue(calc["stress_results"]["passes_stress"])
        self.assertIn("safe limit", explanations["which_limit_recommendation"].lower())
        self.assertTrue(len(card["leverage_points"]) >= 2)
        self.assertTrue(len(card["traps_to_reject"]) >= 2)

    def test_persona_2_ravi_self_employed_lap_pivot(self):
        """
        Ravi, 42, Mysuru · Self-Employed Kirana:
        Cash income: ₹85,000/mo, ITR: ₹4,20,000/yr, Owns shop: ₹45,00,000 unencumbered,
        CIBIL: Unscored, Living: ₹28,000, Rent: ₹0, Wants: ₹15,00,000 over 84 months.
        Expected: Product Pivot to LAP (9.75%–10.50%), Verdict = BORROW.
        """
        profile = {
            "employment_type": "Self-Employed / MSME",
            "net_income": 85000,
            "target_loan_amount": 1500000,
            "tenure_months": 84,
            "existing_emi": 0,
            "rent": 0,
            "living_expenses": 28000,
            "cibil": "Unknown / Unscored",
            "age": 42,
            "has_unencumbered_property": True,
            "property_market_value": 4500000,
            "co_applicant_income_msme": 18000,
            "seasonal_variance_high": True,
            "business_vintage_years": 14
        }

        calc = run_full_underwriting(profile)
        explanations = generate_all_explanations(profile, calc)
        card = build_negotiation_card(profile, calc)

        # Assertions
        self.assertEqual(calc["verdict"], "BORROW")
        self.assertTrue(calc["is_lap"])
        self.assertIn("Property", calc["target_product"])
        # Unlocked LAP rates of ~9.25% - 10.75% instead of 18%+
        self.assertTrue(calc["rate_min"] <= 10.5)
        self.assertGreaterEqual(calc["lender_max_principal"], 1500000)
        self.assertIn("LAP", explanations["rate_why"])
        self.assertIn("unencumbered", card["spoken_script"].lower())

    def test_persona_3_anita_informal_killswitch(self):
        """
        Anita, 35, Hubballi · Informal Delivery Fleet:
        Net: ₹28,000/mo, Phone EMI: ₹1,500, Living: ₹18,000, Rent: ₹5,000,
        1 auto-debit bounce in last 6m, 3 app loans totaling ₹35k at 36% APR.
        Wants: ₹1,50,000 for commercial EV scooter.
        Expected: Verdict = DON'T BORROW (Kill-Switch Active).
        """
        profile = {
            "employment_type": "Informal / Gig Economy",
            "net_income": 28000,
            "target_loan_amount": 150000,
            "tenure_months": 24,
            "existing_emi": 1500,
            "rent": 5000,
            "living_expenses": 18000,
            "cibil": "Below 700",
            "age": 35,
            "payment_bounces_6m": 1,
            "active_app_loan_count": 3,
            "app_loan_balance_total": 35000,
            "app_loan_apr": 36.0,
            "is_ev_vehicle": True,
            "productive_income_boost": 3500
        }

        calc = run_full_underwriting(profile)
        explanations = generate_all_explanations(profile, calc)
        card = build_negotiation_card(profile, calc)

        # Assertions
        self.assertEqual(calc["verdict"], "DON'T BORROW")
        self.assertEqual(calc["lender_max_principal"], 0.0)
        self.assertEqual(calc["borrower_safe_limit"], 0.0)
        self.assertIn("bounce", explanations["verdict_why"].lower())
        self.assertIn("consolidation", card["spoken_script"].lower())

    def test_rule_unknown_never_zero(self):
        """Rule 3: Unknown CIBIL score must not default to 0/300; it widens the band symmetrically."""
        profile = {
            "employment_type": "Salaried",
            "net_income": 100000,
            "target_loan_amount": 500000,
            "tenure_months": 36,
            "cibil": "Unknown / Unscored"
        }
        calc = run_full_underwriting(profile)
        self.assertTrue(calc["is_cibil_unknown"])
        # Should be a wide band, not a subprime penalty
        self.assertGreaterEqual(calc["rate_max"] - calc["rate_min"], 1.5)

    def test_rule_confidence_progression(self):
        """Rule 2: Confidence starts at 60.0% for mandatory and increases up to 95.0%."""
        profile_mandatory_only = {
            "loan_purpose": "Wedding",
            "target_loan_amount": 800000,
            "tenure_months": 48,
            "employment_type": "Salaried",
            "net_income": 110000,
            "existing_emi": 14000,
            "rent": 28000,
            "living_expenses": 25000,
            "cibil": "750+",
            "age": 29
        }
        conf_base = compute_confidence_score(profile_mandatory_only, "Salaried")
        self.assertEqual(conf_base, 60.0)

        # Add salaried variables
        profile_with_vars = dict(profile_mandatory_only)
        profile_with_vars["employer_tier"] = "Listed Tier-1 Corporate/MNC"
        profile_with_vars["job_vintage_years"] = 5.0
        profile_with_vars["liquid_savings_months"] = 8.0
        conf_higher = compute_confidence_score(profile_with_vars, "Salaried")
        self.assertGreater(conf_higher, 65.0)

        # Spread contracts
        width_base = get_spread_half_width(conf_base)
        width_higher = get_spread_half_width(conf_higher)
        self.assertLess(width_higher, width_base)


if __name__ == "__main__":
    unittest.main()
