"""
tests/test_all_18_variables.py
Comprehensive verification of all 18 optional questions across Salaried, MSME, and Gig tracks:
- 10 Mandatory + 18 Variable = 28 questions total per category
- Cumulative weight progression: 60.0% -> 95.0%
- Underwriting execution with all 18 variables
"""

import unittest
from engine.confidence import (
    get_questions_for_category,
    get_variable_questions_for_category,
    compute_confidence_score,
    get_spread_half_width,
    MASTER_QUESTIONS,
)
from engine.underwriting import run_full_underwriting


class TestAll18Variables(unittest.TestCase):

    def test_question_counts(self):
        """Each track must have 10 mandatory + 18 variable questions = 28 total."""
        for cat in ["Salaried job", "Self-employed", "Business", "Freelance / Contract work", "Other"]:
            all_qs = get_questions_for_category(cat)
            var_qs = get_variable_questions_for_category(cat)
            self.assertEqual(len(all_qs), 28, f"Category {cat} should have 28 total questions")
            self.assertEqual(len(var_qs), 18, f"Category {cat} should have 18 variable questions")

    def test_cumulative_weights_sum_to_35(self):
        """Variable weights for each category must sum to exactly 35.0%."""
        for cat in ["Salaried", "Self-Employed / MSME", "Informal / Gig Economy"]:
            var_qs = [q for q in MASTER_QUESTIONS.values() if q["tier"] == "Variable" and q["category"] == cat]
            self.assertEqual(len(var_qs), 18, f"{cat} should have 18 questions in MASTER_QUESTIONS")
            total_weight = sum(q["weight"] for q in var_qs)
            self.assertAlmostEqual(total_weight, 35.0, places=1, msg=f"{cat} weights must sum to 35.0%")

    def test_salaried_full_progression_to_95(self):
        """Answering mandatory gives 60.0%; answering all 18 salaried gives 95.0%."""
        profile = {
            "loan_purpose": "Personal needs",
            "target_loan_amount": 500000,
            "tenure_months": 48,
            "employment_type": "Salaried job",
            "net_income": 90000,
            "existing_emi": 10000,
            "rent": 20000,
            "living_expenses": 20000,
            "cibil": "750–799",
            "age": 30
        }
        self.assertEqual(compute_confidence_score(profile, "Salaried job"), 60.0)

        # Answer all 18 salaried variables
        salaried_answers = {
            "employer_tier": "Listed Tier-1 Corporate/MNC",
            "job_vintage_years": 4.0,
            "career_vintage_years": 7.0,
            "salary_credit_mode": "Direct Bank Transfer (NEFT/RTGS)",
            "variable_bonus_share_pct": 10,
            "on_notice_or_probation": "No",
            "liquid_savings_months": 6.0,
            "cc_utilization_pct": 15,
            "credit_inquiries_90d": 1,
            "quoted_bank_rate": 11.25,
            "quoted_processing_fee_pct": 1.0,
            "largest_loan_remaining_mos": 18,
            "has_large_upcoming_outlay": "No",
            "co_applicant_income": 30000,
            "home_loan_tax_benefit": "No",
            "epf_balance_above_3l": "Yes",
            "has_health_insurance": "Yes",
            "unsecured_loan_count": 1
        }
        full_profile = {**profile, **salaried_answers}
        score = compute_confidence_score(full_profile, "Salaried job")
        self.assertEqual(score, 95.0)
        self.assertEqual(get_spread_half_width(score), 0.35)

        # Test underwriting run with full profile
        res = run_full_underwriting(full_profile)
        self.assertIn(res["verdict"], ["BORROW", "BORROW LESS", "DON'T BORROW"])
        self.assertGreater(res["all_in_apr"], 0)

    def test_msme_full_progression_to_95(self):
        """Answering mandatory gives 60.0%; answering all 18 MSME gives 95.0%."""
        profile = {
            "loan_purpose": "Business",
            "target_loan_amount": 1000000,
            "tenure_months": 60,
            "employment_type": "Business",
            "net_income": 120000,
            "existing_emi": 15000,
            "rent": 0,
            "living_expenses": 30000,
            "cibil": "750–799",
            "age": 38
        }
        self.assertEqual(compute_confidence_score(profile, "Business"), 60.0)

        msme_answers = {
            "itr_profit_annual": 600000,
            "itr_filing_years": 4,
            "gross_monthly_cash_intake": 150000,
            "has_unencumbered_property": "Yes",
            "property_market_value": 3500000,
            "title_deed_clarity": "Yes",
            "business_vintage_years": 8,
            "business_premises_ownership": "Owned (No Rent)",
            "annual_gstr3b_turnover": 5000000,
            "seasonal_variance_high": "No (Consistent)",
            "co_applicant_income_msme": 25000,
            "commercial_vehicle_assets": "Yes",
            "supplier_payment_terms": "15–30 Days Credit",
            "customer_receivables_days": 20,
            "average_bank_balance": 80000,
            "unsecured_mca_portion_pct": 0,
            "expansion_margin_boost": 20000,
            "statutory_gst_disputes": "No"
        }
        full_profile = {**profile, **msme_answers}
        score = compute_confidence_score(full_profile, "Business")
        self.assertEqual(score, 95.0)

        res = run_full_underwriting(full_profile)
        self.assertTrue(res["is_lap"])

    def test_gig_full_progression_to_95(self):
        """Answering mandatory gives 60.0%; answering all 18 Gig gives 95.0%."""
        profile = {
            "loan_purpose": "Vehicle",
            "target_loan_amount": 120000,
            "tenure_months": 24,
            "employment_type": "Freelance / Contract work",
            "net_income": 35000,
            "existing_emi": 2000,
            "rent": 6000,
            "living_expenses": 16000,
            "cibil": "600–699",
            "age": 28
        }
        self.assertEqual(compute_confidence_score(profile, "Freelance / Contract work"), 60.0)

        gig_answers = {
            "payment_bounces_6m": 0,
            "active_app_loan_count": 0,
            "app_loan_balance_total": 0,
            "app_loan_apr": 0.0,
            "productive_income_boost": 4000,
            "payout_mode": "Digital App / Bank Transfer",
            "platform_active_days_monthly": 26,
            "household_adult_earners": 2,
            "spouse_employment_status": "Employed / Earning",
            "dependent_children_count": 1,
            "secondary_trade_income": "Yes (Active Side Income)",
            "liquid_emergency_cash_gold": 15000,
            "is_ev_vehicle": "Yes (Replaces Petrol Scooter)",
            "informal_moneylender_debt": "No",
            "has_commercial_driving_badge": "Yes",
            "phone_emi_active": "No",
            "medical_emergency_12m": "No",
            "shg_jlg_member": "No"
        }
        full_profile = {**profile, **gig_answers}
        score = compute_confidence_score(full_profile, "Freelance / Contract work")
        self.assertEqual(score, 95.0)

        res = run_full_underwriting(full_profile)
        self.assertIn(res["verdict"], ["BORROW", "BORROW LESS"])


if __name__ == "__main__":
    unittest.main()
