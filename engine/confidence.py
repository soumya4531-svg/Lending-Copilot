"""
engine/confidence.py
Master Question Matrix, Adaptive Category Branching, Info Descriptions ("Why We Ask This"),
and Live Confidence Score Progression Engine (60.0% to 95.0%).
"""

from typing import Dict, Any, List

MASTER_QUESTIONS: Dict[str, Dict[str, Any]] = {
    # =========================================================================
    # UNIVERSAL MANDATORY QUESTIONS (M01 - M10, Base 60.0%)
    # =========================================================================
    "loan_purpose": {
        "id": "M01",
        "tier": "Mandatory",
        "category": "Universal",
        "label": "What do you need the loan for?",
        "input_type": "select",
        "options": ["Personal needs", "Wedding", "Business", "Vehicle", "Home", "Education", "Medical expenses", "Debt Consolidation", "Other"],
        "default": "Personal needs",
        "weight": 6.0,
        "impact": "O1, O3",
        "why_we_ask": "Helps determine the right loan type and what repayment period lenders allow."
    },
    "target_loan_amount": {
        "id": "M02",
        "tier": "Mandatory",
        "category": "Universal",
        "label": "How much do you want to borrow?",
        "hint": "The loan amount you need.",
        "input_type": "number",
        "default": 800000,
        "min": 10000,
        "step": 10000,
        "weight": 6.0,
        "impact": "O1, O2",
        "why_we_ask": "The loan amount you need, so we can test whether the payments fit your monthly budget."
    },
    "tenure_months": {
        "id": "M03",
        "tier": "Mandatory",
        "category": "Universal",
        "label": "How many months will you take to repay?",
        "input_type": "select",
        "options": [12, 24, 36, 48, 60, 72, 84, 120],
        "default": 48,
        "weight": 6.0,
        "impact": "O4",
        "why_we_ask": "Sets how many months you will spread repayments over and how much total interest you will pay."
    },
    "employment_type": {
        "id": "M04",
        "tier": "Mandatory",
        "category": "Universal",
        "label": "What is your main source of income?",
        "input_type": "select",
        "options": ["Salaried job", "Self-employed", "Business", "Freelance / Contract work", "Other"],
        "default": "Salaried job",
        "weight": 6.0,
        "impact": "Branching, O2",
        "why_we_ask": "Lenders price salaried jobs, businesses, and freelance income differently."
    },
    "net_income": {
        "id": "M05",
        "tier": "Mandatory",
        "category": "Universal",
        "label": "What is your monthly take-home income?",
        "hint": "The amount you receive after deductions.",
        "input_type": "number",
        "default": 110000,
        "min": 5000,
        "step": 5000,
        "weight": 6.0,
        "impact": "O2, O4",
        "why_we_ask": "The baseline for how much debt you can comfortably afford to pay each month."
    },
    "existing_emi": {
        "id": "M06",
        "tier": "Mandatory",
        "category": "Universal",
        "label": "Other loan payments each month",
        "hint": "Include all your current loan EMIs.",
        "input_type": "number",
        "default": 14000,
        "min": 0,
        "step": 1000,
        "weight": 6.0,
        "impact": "O2, O4",
        "why_we_ask": "We subtract your existing loan payments so a new loan doesn't overstretch your budget."
    },
    "rent": {
        "id": "M07",
        "tier": "Mandatory",
        "category": "Universal",
        "label": "Rent or housing payment each month",
        "input_type": "number",
        "default": 28000,
        "min": 0,
        "step": 1000,
        "weight": 6.0,
        "impact": "O2, O4",
        "why_we_ask": "Your regular shelter cost. Bank formulas often ignore this, but it affects your real affordability."
    },
    "living_expenses": {
        "id": "M08",
        "tier": "Mandatory",
        "category": "Universal",
        "label": "Essential expenses each month",
        "hint": "Food, bills, travel and other necessary costs.",
        "input_type": "number",
        "default": 25000,
        "min": 1000,
        "step": 1000,
        "weight": 6.0,
        "impact": "O2, O4",
        "why_we_ask": "Money needed for food, groceries, travel and household bills so you never face a cash shortage."
    },
    "cibil": {
        "id": "M09",
        "tier": "Mandatory",
        "category": "Universal",
        "label": "What is your CIBIL score?",
        "input_type": "select",
        "options": ["800+", "750–799", "700–749", "600–699", "Below 600", "I don't know"],
        "default": "750–799",
        "weight": 6.0,
        "impact": "O3",
        "why_we_ask": "A higher score qualifies for lower rates. If you don't know, we show a fair, honest estimated range."
    },
    "age": {
        "id": "M10",
        "tier": "Mandatory",
        "category": "Universal",
        "label": "How old are you?",
        "input_type": "number",
        "default": 29,
        "min": 18,
        "max": 75,
        "step": 1,
        "weight": 6.0,
        "impact": "O2, O4",
        "why_we_ask": "Helps ensure your repayment schedule finishes comfortably before retirement age."
    },

    # =========================================================================
    # SALARIED VARIABLE QUESTIONS (S01 - S18, 60% -> 95%)
    # =========================================================================
    "employer_tier": {
        "id": "S01",
        "tier": "Variable",
        "category": "Salaried",
        "label": "What type of company do you work for?",
        "input_type": "select",
        "options": ["Listed Tier-1 Corporate/MNC", "Government / PSU", "Mid-Market Private Firm", "Early-Stage Startup"],
        "default": "Listed Tier-1 Corporate/MNC",
        "weight": 3.0,
        "impact": "O2, O3",
        "why_we_ask": "Tier-1 / PSU unlocks lower interest rates and raises allowable FOIR up to 55%."
    },
    "job_vintage_years": {
        "id": "S02",
        "tier": "Variable",
        "category": "Salaried",
        "label": "How many years have you been at your current job?",
        "input_type": "number",
        "default": 3.0,
        "min": 0.0,
        "step": 0.5,
        "weight": 2.5,
        "impact": "O3",
        "why_we_ask": "Over 3 years at the same job proves stability, lowering interest rate spreads."
    },
    "career_vintage_years": {
        "id": "S03",
        "tier": "Variable",
        "category": "Salaried",
        "label": "Total years of overall work experience",
        "input_type": "number",
        "default": 5.0,
        "min": 0.0,
        "step": 1.0,
        "weight": 2.0,
        "impact": "O2, O4",
        "why_we_ask": "More than 5 years unlocks 60–72 month repayment terms; early careers are capped at 36 months."
    },
    "salary_credit_mode": {
        "id": "S04",
        "tier": "Variable",
        "category": "Salaried",
        "label": "How is your salary paid into your account?",
        "input_type": "select",
        "options": ["Direct Bank Transfer (NEFT/RTGS)", "Cash / Cheque"],
        "default": "Direct Bank Transfer (NEFT/RTGS)",
        "weight": 2.0,
        "impact": "O2",
        "why_we_ask": "Bank transfers validate 100% of income; cash salary takes a 25% underwriting haircut."
    },
    "variable_bonus_share_pct": {
        "id": "S05",
        "tier": "Variable",
        "category": "Salaried",
        "label": "Roughly what % of your total pay is variable or bonus?",
        "input_type": "number",
        "default": 0,
        "min": 0,
        "max": 100,
        "step": 5,
        "weight": 2.0,
        "impact": "O2, O4",
        "why_we_ask": "If bonuses exceed 20% of CTC, monthly safe capacity is discounted by 15% to buffer volatility."
    },
    "on_notice_or_probation": {
        "id": "S06",
        "tier": "Variable",
        "category": "Salaried",
        "label": "Are you currently on probation or serving notice?",
        "input_type": "select",
        "options": ["No", "Yes"],
        "default": "No",
        "weight": 2.0,
        "impact": "O1, O3",
        "why_we_ask": "Serving notice flags risk of income gap, adding 1.50% rate spread and capping principal to 6 months' salary."
    },
    "liquid_savings_months": {
        "id": "S07",
        "tier": "Variable",
        "category": "Salaried",
        "label": "How many months of expenses do you have in savings?",
        "input_type": "number",
        "default": 3.0,
        "min": 0.0,
        "step": 1.0,
        "weight": 2.5,
        "impact": "O4",
        "why_we_ask": "Having 6+ months of living costs reduces emergency reserve from 10% to 5%, expanding safe borrowing limit."
    },
    "cc_utilization_pct": {
        "id": "S08",
        "tier": "Variable",
        "category": "Salaried",
        "label": "Roughly what % of your credit card limit do you use?",
        "input_type": "number",
        "default": 20,
        "min": 0,
        "max": 100,
        "step": 5,
        "weight": 2.0,
        "impact": "O3",
        "why_we_ask": "Using over 50% of card limits signals cash stretch (+0.50% spread); under 20% lowers rates."
    },
    "credit_inquiries_90d": {
        "id": "S09",
        "tier": "Variable",
        "category": "Salaried",
        "label": "Loan or card applications made in the last 90 days",
        "input_type": "number",
        "default": 0,
        "min": 0,
        "step": 1,
        "weight": 1.5,
        "impact": "O3",
        "why_we_ask": "Over 3 recent inquiries signals credit hunger, widening your interest rate band."
    },
    "quoted_bank_rate": {
        "id": "S10",
        "tier": "Variable",
        "category": "Salaried",
        "label": "Did a bank already quote you an interest rate? (%, Optional)",
        "input_type": "number",
        "default": 0.0,
        "min": 0.0,
        "step": 0.25,
        "weight": 3.0,
        "impact": "Negotiation Card",
        "why_we_ask": "Benchmarks the bank's quote against fair regulatory pricing on the Negotiation Card."
    },
    "quoted_processing_fee_pct": {
        "id": "S11",
        "tier": "Variable",
        "category": "Salaried",
        "label": "What processing fee did the bank quote? (%)",
        "input_type": "number",
        "default": 1.0,
        "min": 0.0,
        "step": 0.25,
        "weight": 2.0,
        "impact": "O3, APR",
        "why_we_ask": "Factored with 18% GST into our IRR solver to disclose the true all-in APR cost of borrowing."
    },
    "largest_loan_remaining_mos": {
        "id": "S12",
        "tier": "Variable",
        "category": "Salaried",
        "label": "Months left to pay on your biggest existing loan",
        "input_type": "number",
        "default": 12,
        "min": 0,
        "step": 1,
        "weight": 1.5,
        "impact": "O2, O4",
        "why_we_ask": "If existing loans finish within 12 months, future monthly headroom expands, giving you greater safety."
    },
    "has_large_upcoming_outlay": {
        "id": "S13",
        "tier": "Variable",
        "category": "Salaried",
        "label": "Any major big expenses planned in the next 12 months?",
        "input_type": "select",
        "options": ["No", "Yes"],
        "default": "No",
        "weight": 1.5,
        "impact": "O4",
        "why_we_ask": "Planned one-off capital needs require higher cash reserves, lowering safe borrowing limit."
    },
    "co_applicant_income": {
        "id": "S14",
        "tier": "Variable",
        "category": "Salaried",
        "label": "Spouse or co-applicant monthly take-home income (₹)",
        "input_type": "number",
        "default": 0,
        "min": 0,
        "step": 5000,
        "weight": 2.0,
        "impact": "O2, O4",
        "why_we_ask": "Combines verified family income, raising both allowable bank FOIR and safe borrowing capacity."
    },
    "home_loan_tax_benefit": {
        "id": "S15",
        "tier": "Variable",
        "category": "Salaried",
        "label": "Do you claim tax deductions on an existing home loan?",
        "input_type": "select",
        "options": ["No", "Yes"],
        "default": "No",
        "weight": 1.5,
        "impact": "O4",
        "why_we_ask": "Credits back ~₹3,000–₹7,000 in monthly tax savings into your actual disposable cash surplus."
    },
    "epf_balance_above_3l": {
        "id": "S16",
        "tier": "Variable",
        "category": "Salaried",
        "label": "Is your Provident Fund (EPF) balance above ₹3 Lakhs?",
        "input_type": "select",
        "options": ["No", "Yes"],
        "default": "No",
        "weight": 1.5,
        "impact": "O4, Stress",
        "why_we_ask": "Serves as an emergency distress cushion, reducing vulnerability during economic shocks."
    },
    "has_health_insurance": {
        "id": "S17",
        "tier": "Variable",
        "category": "Salaried",
        "label": "Do you have comprehensive health insurance?",
        "input_type": "select",
        "options": ["No", "Yes"],
        "default": "No",
        "weight": 1.0,
        "impact": "O4",
        "why_we_ask": "Comprehensive medical coverage lowers required monthly emergency cash deductions."
    },
    "unsecured_loan_count": {
        "id": "S18",
        "tier": "Variable",
        "category": "Salaried",
        "label": "How many personal loans are you currently paying off?",
        "input_type": "number",
        "default": 0,
        "min": 0,
        "step": 1,
        "weight": 1.5,
        "impact": "O3",
        "why_we_ask": "Having more than 2 active personal loans adds a 1.0% multi-loan leverage penalty."
    },

    # =========================================================================
    # SELF-EMPLOYED / MSME VARIABLES (B01 - B18, 60% -> 95%)
    # =========================================================================
    "itr_profit_annual": {
        "id": "B01",
        "tier": "Variable",
        "category": "Self-Employed / MSME",
        "label": "Annual net profit reported on your latest ITR (₹)",
        "input_type": "number",
        "default": 0,
        "min": 0,
        "step": 25000,
        "weight": 3.0,
        "impact": "O2",
        "why_we_ask": "Sets the hard ceiling for traditional unsecured banking credit; low reported ITR triggers loan caps."
    },
    "itr_filing_years": {
        "id": "B02",
        "tier": "Variable",
        "category": "Self-Employed / MSME",
        "label": "How many continuous years have you filed business ITRs?",
        "input_type": "number",
        "default": 3,
        "min": 0,
        "step": 1,
        "weight": 2.0,
        "impact": "O3",
        "why_we_ask": "Three or more years of filed ITRs proves stability, cutting lending spreads by 0.75%."
    },
    "gross_monthly_cash_intake": {
        "id": "B03",
        "tier": "Variable",
        "category": "Self-Employed / MSME",
        "label": "Average monthly cash and UPI sales intake (₹)",
        "input_type": "number",
        "default": 0,
        "min": 0,
        "step": 10000,
        "weight": 2.5,
        "impact": "O2, O4",
        "why_we_ask": "Evaluates real operating cash flow to benchmark safe borrowing capacity."
    },
    "has_unencumbered_property": {
        "id": "B04",
        "tier": "Variable",
        "category": "Self-Employed / MSME",
        "label": "Do you own a property or shop with no loan on it?",
        "input_type": "select",
        "options": ["No", "Yes"],
        "default": "No",
        "weight": 3.5,
        "impact": "O1, O3 (Product Pivot)",
        "why_we_ask": "Critical Product Pivot: switches your loan from 18%+ unsecured lines to 9.5%–11% LAP."
    },
    "property_market_value": {
        "id": "B05",
        "tier": "Variable",
        "category": "Self-Employed / MSME",
        "label": "Conservative market value of this loan-free property (₹)",
        "input_type": "number",
        "default": 0,
        "min": 0,
        "step": 100000,
        "weight": 2.5,
        "impact": "O2",
        "why_we_ask": "Determines maximum LAP sanction capacity using standard conservative 50%–60% Loan-to-Value (LTV)."
    },
    "title_deed_clarity": {
        "id": "B06",
        "tier": "Variable",
        "category": "Self-Employed / MSME",
        "label": "Is the property title deed clear and in your name?",
        "input_type": "select",
        "options": ["Yes", "No"],
        "default": "Yes",
        "weight": 2.0,
        "impact": "O3",
        "why_we_ask": "Clear registered property title narrows the LAP spread; unclear title widens interest rate uncertainty."
    },
    "business_vintage_years": {
        "id": "B07",
        "tier": "Variable",
        "category": "Self-Employed / MSME",
        "label": "How many years has your business operated at this location?",
        "input_type": "number",
        "default": 5,
        "min": 0,
        "step": 1,
        "weight": 2.0,
        "impact": "O3",
        "why_we_ask": "Five or more years of local shop vintage eliminates relocation risk, cutting rate spreads by 0.50%."
    },
    "business_premises_ownership": {
        "id": "B08",
        "tier": "Variable",
        "category": "Self-Employed / MSME",
        "label": "Do you own or rent your business shop/office?",
        "input_type": "select",
        "options": ["Owned (No Rent)", "Rented / Commercial Lease"],
        "default": "Owned (No Rent)",
        "weight": 1.5,
        "impact": "O2, O4",
        "why_we_ask": "An owned store eliminates rental overhead, permanently protecting operating profit margins."
    },
    "annual_gstr3b_turnover": {
        "id": "B09",
        "tier": "Variable",
        "category": "Self-Employed / MSME",
        "label": "Annual business turnover reported on GST (GSTR-3B, ₹)",
        "input_type": "number",
        "default": 0,
        "min": 0,
        "step": 50000,
        "weight": 2.0,
        "impact": "O2",
        "why_we_ask": "Unlocks GST surrogate credit lines sanctioning up to 10%–15% of verified turnover."
    },
    "seasonal_variance_high": {
        "id": "B10",
        "tier": "Variable",
        "category": "Self-Employed / MSME",
        "label": "Does monthly sales drop by >35% during slow seasons?",
        "input_type": "select",
        "options": ["No (Consistent)", "Yes (Seasonal Drops)"],
        "default": "No (Consistent)",
        "weight": 1.5,
        "impact": "O4",
        "why_we_ask": "If revenue drops >35% in low season, anchors safe EMI to the trough month so you never default."
    },
    "co_applicant_income_msme": {
        "id": "B11",
        "tier": "Variable",
        "category": "Self-Employed / MSME",
        "label": "Other monthly family or spouse income supporting household (₹)",
        "input_type": "number",
        "default": 0,
        "min": 0,
        "step": 2000,
        "weight": 2.0,
        "impact": "O2, O4",
        "why_we_ask": "Adds verified secondary family cash flow to debt-servicing limits."
    },
    "commercial_vehicle_assets": {
        "id": "B12",
        "tier": "Variable",
        "category": "Self-Employed / MSME",
        "label": "Do you own commercial vehicles (delivery vans, autos) free of debt?",
        "input_type": "select",
        "options": ["No", "Yes"],
        "default": "No",
        "weight": 1.5,
        "impact": "O3",
        "why_we_ask": "Provides secondary movable asset security, reducing equipment rate spreads."
    },
    "supplier_payment_terms": {
        "id": "B13",
        "tier": "Variable",
        "category": "Self-Employed / MSME",
        "label": "How do you pay your main suppliers?",
        "input_type": "select",
        "options": ["15–30 Days Credit", "Immediate Cash Only", "60+ Days Credit"],
        "default": "15–30 Days Credit",
        "weight": 1.5,
        "impact": "O4",
        "why_we_ask": "Immediate cash-only suppliers require higher cash cushions, reducing safe borrowing headroom."
    },
    "customer_receivables_days": {
        "id": "B14",
        "tier": "Variable",
        "category": "Self-Employed / MSME",
        "label": "Average days customers take to pay credit dues",
        "input_type": "number",
        "default": 30,
        "min": 0,
        "step": 5,
        "weight": 1.5,
        "impact": "O2, O4",
        "why_we_ask": "Over 45 days of uncollected customer credit applies a 10% haircut on monthly operating cash."
    },
    "average_bank_balance": {
        "id": "B15",
        "tier": "Variable",
        "category": "Self-Employed / MSME",
        "label": "Average daily bank account balance (ABB, ₹)",
        "input_type": "number",
        "default": 0,
        "min": 0,
        "step": 5000,
        "weight": 2.0,
        "impact": "O3",
        "why_we_ask": "Maintaining a healthy daily credit balance in current accounts cuts lending spreads by up to 1.0%."
    },
    "unsecured_mca_portion_pct": {
        "id": "B16",
        "tier": "Variable",
        "category": "Self-Employed / MSME",
        "label": "Roughly what % of current debt is daily/app merchant loans?",
        "input_type": "number",
        "default": 0,
        "min": 0,
        "max": 100,
        "step": 5,
        "weight": 1.5,
        "impact": "O1, O4",
        "why_we_ask": "High short-term merchant advance debt flags severe cash stretch, prompting a Borrow Less warning."
    },
    "expansion_margin_boost": {
        "id": "B17",
        "tier": "Variable",
        "category": "Self-Employed / MSME",
        "label": "Expected extra monthly profit this loan will generate (₹)",
        "input_type": "number",
        "default": 0,
        "min": 0,
        "step": 2000,
        "weight": 1.5,
        "impact": "O2, O4",
        "why_we_ask": "Incremental earnings from new stock/equipment are credited toward future safe repayment capacity."
    },
    "statutory_gst_disputes": {
        "id": "B18",
        "tier": "Variable",
        "category": "Self-Employed / MSME",
        "label": "Any pending tax notices or GST legal disputes?",
        "input_type": "select",
        "options": ["No", "Yes"],
        "default": "No",
        "weight": 1.0,
        "impact": "O3",
        "why_we_ask": "Active tax disputes widen loan spreads by 1.50% and bar access to prime institutional lenders."
    },

    # =========================================================================
    # INFORMAL / GIG ECONOMY VARIABLES (I01 - I18, 60% -> 95%)
    # =========================================================================
    "payment_bounces_6m": {
        "id": "I01",
        "tier": "Variable",
        "category": "Informal / Gig Economy",
        "label": "Missed or bounced loan payments in the last 6 months",
        "input_type": "number",
        "default": 0,
        "min": 0,
        "step": 1,
        "weight": 3.5,
        "impact": "O1 (Kill-Switch)",
        "why_we_ask": "Mandatory Kill-Switch: Any active bounce in 6 months indicates default distress, triggering Don't Borrow."
    },
    "active_app_loan_count": {
        "id": "I02",
        "tier": "Variable",
        "category": "Informal / Gig Economy",
        "label": "How many instant loan apps do you currently have loans with?",
        "input_type": "number",
        "default": 0,
        "min": 0,
        "step": 1,
        "weight": 2.5,
        "impact": "O1, O2",
        "why_we_ask": "Identifies short-term digital leverage and triggers mandatory debt consolidation rules."
    },
    "app_loan_balance_total": {
        "id": "I03",
        "tier": "Variable",
        "category": "Informal / Gig Economy",
        "label": "Total balance left to clear across all digital loan apps (₹)",
        "input_type": "number",
        "default": 0,
        "min": 0,
        "step": 5000,
        "weight": 2.5,
        "impact": "O1, O2",
        "why_we_ask": "Quantifies the predatory debt that must be cleared before taking on any new credit."
    },
    "app_loan_apr": {
        "id": "I04",
        "tier": "Variable",
        "category": "Informal / Gig Economy",
        "label": "Highest annual interest rate on your app loans (% APR)",
        "input_type": "number",
        "default": 0.0,
        "min": 0.0,
        "step": 1.0,
        "weight": 2.5,
        "impact": "O1, O3",
        "why_we_ask": "Interest above 24% triggers our predatory debt policy, blocking non-essential debt."
    },
    "productive_income_boost": {
        "id": "I05",
        "tier": "Variable",
        "category": "Informal / Gig Economy",
        "label": "Extra monthly income this tool/vehicle will help you earn (₹)",
        "input_type": "number",
        "default": 0,
        "min": 0,
        "step": 500,
        "weight": 3.0,
        "impact": "O2, O4",
        "why_we_ask": "Incremental earnings (e.g. EV fuel savings) are credited toward future safe loan repayment capacity."
    },
    "payout_mode": {
        "id": "I06",
        "tier": "Variable",
        "category": "Informal / Gig Economy",
        "label": "How do you receive your work payouts?",
        "input_type": "select",
        "options": ["Digital App / Bank Transfer", "Unrecorded Cash In Hand"],
        "default": "Digital App / Bank Transfer",
        "weight": 2.5,
        "impact": "O3",
        "why_we_ask": "Verifiable digital platform payouts unlock priority sector commercial EV rates (11%–13%) over personal loans."
    },
    "platform_active_days_monthly": {
        "id": "I07",
        "tier": "Variable",
        "category": "Informal / Gig Economy",
        "label": "How many days per month do you actively work on trips/orders?",
        "input_type": "number",
        "default": 24,
        "min": 0,
        "max": 31,
        "step": 1,
        "weight": 2.0,
        "impact": "O2",
        "why_we_ask": "24 or more days validates full-time earnings; under 15 days triggers a 20% volatility haircut."
    },
    "household_adult_earners": {
        "id": "I08",
        "tier": "Variable",
        "category": "Informal / Gig Economy",
        "label": "How many adults in your household earn an income?",
        "input_type": "number",
        "default": 1,
        "min": 1,
        "step": 1,
        "weight": 1.5,
        "impact": "O4",
        "why_we_ask": "Quantifies income redundancy: single-earner households face greater vulnerability to shocks."
    },
    "spouse_employment_status": {
        "id": "I09",
        "tier": "Variable",
        "category": "Informal / Gig Economy",
        "label": "Spouse's current work status",
        "input_type": "select",
        "options": ["Employed / Earning", "Homemaker / Not Seeking Work", "Long-Term Unemployed (6+ mos)"],
        "default": "Homemaker / Not Seeking Work",
        "weight": 2.0,
        "impact": "O4, Stress",
        "why_we_ask": "A long-term unemployed spouse increases the stress shock factor from 20% to 30% of income."
    },
    "dependent_children_count": {
        "id": "I10",
        "tier": "Variable",
        "category": "Informal / Gig Economy",
        "label": "Number of dependent children living with you",
        "input_type": "number",
        "default": 0,
        "min": 0,
        "step": 1,
        "weight": 1.5,
        "impact": "O4",
        "why_we_ask": "Each dependent child adds ₹3,000 to the non-negotiable household living floor."
    },
    "secondary_trade_income": {
        "id": "I11",
        "tier": "Variable",
        "category": "Informal / Gig Economy",
        "label": "Do you or your family have a side trade (tailoring, repairs, etc.)?",
        "input_type": "select",
        "options": ["No", "Yes (Active Side Income)"],
        "default": "No",
        "weight": 1.5,
        "impact": "O4",
        "why_we_ask": "Diversified household earnings cushion potential downtime from vehicle repairs or platform drops."
    },
    "liquid_emergency_cash_gold": {
        "id": "I12",
        "tier": "Variable",
        "category": "Informal / Gig Economy",
        "label": "Emergency cash or gold savings you can sell in crisis (₹)",
        "input_type": "number",
        "default": 0,
        "min": 0,
        "step": 1000,
        "weight": 2.0,
        "impact": "O4",
        "why_we_ask": "Zero emergency cash triggers an explicit warning: any lost delivery day causes an immediate loan default."
    },
    "is_ev_vehicle": {
        "id": "I13",
        "tier": "Variable",
        "category": "Informal / Gig Economy",
        "label": "Is this loan for an Electric Vehicle (EV) that saves on fuel?",
        "input_type": "select",
        "options": ["No", "Yes (Replaces Petrol Scooter)"],
        "default": "No",
        "weight": 2.0,
        "impact": "O3, O4",
        "why_we_ask": "EV adoption saves ~₹3,500/month in petrol costs, which is directly credited toward servicing the vehicle installment."
    },
    "informal_moneylender_debt": {
        "id": "I14",
        "tier": "Variable",
        "category": "Informal / Gig Economy",
        "label": "Do you owe money to local daily/weekly cash moneylenders?",
        "input_type": "select",
        "options": ["No", "Yes"],
        "default": "No",
        "weight": 1.5,
        "impact": "O1, O4",
        "why_we_ask": "Informal moneylender debt represents extreme financial distress and lowers maximum allowable FOIR to 25%."
    },
    "has_commercial_driving_badge": {
        "id": "I15",
        "tier": "Variable",
        "category": "Informal / Gig Economy",
        "label": "Do you have a commercial driver badge or commercial license?",
        "input_type": "select",
        "options": ["No", "Yes"],
        "default": "No",
        "weight": 1.5,
        "impact": "O3",
        "why_we_ask": "Commercial badge unlocks asset-hypothecated financing and clean state priority sector subsidies."
    },
    "phone_emi_active": {
        "id": "I16",
        "tier": "Variable",
        "category": "Informal / Gig Economy",
        "label": "Are you currently paying off a mobile phone on EMI?",
        "input_type": "select",
        "options": ["No", "Yes"],
        "default": "No",
        "weight": 1.0,
        "impact": "O4",
        "why_we_ask": "Smartphone installments must be prioritized: default halts mobile app access and stops all delivery income."
    },
    "medical_emergency_12m": {
        "id": "I17",
        "tier": "Variable",
        "category": "Informal / Gig Economy",
        "label": "Did your family face a major unpaid hospital bill in the past year?",
        "input_type": "select",
        "options": ["No", "Yes"],
        "default": "No",
        "weight": 1.0,
        "impact": "O4",
        "why_we_ask": "Past uninsured medical expenses widen the uncertainty spread on your safe repayment capacity."
    },
    "shg_jlg_member": {
        "id": "I18",
        "tier": "Variable",
        "category": "Informal / Gig Economy",
        "label": "Are you a member of a Self-Help Group (SHG / JLG)?",
        "input_type": "select",
        "options": ["No", "Yes"],
        "default": "No",
        "weight": 1.0,
        "impact": "O3",
        "why_we_ask": "Active Self-Help Group membership unlocks low-cost microfinance options capped at RBI guidelines (18%–22%)."
    }
}


def get_questions_for_category(category: str) -> List[Dict[str, Any]]:
    """
    Returns the list of question definitions matching the user's category track.
    Always includes the 10 Universal Mandatory questions followed by the 18 sector questions.
    """
    cat_lower = (category or "salaried").lower()
    active_questions = []

    for key, q in MASTER_QUESTIONS.items():
        q_copy = dict(q)
        q_copy["key"] = key
        if q["tier"] == "Mandatory":
            active_questions.append(q_copy)
        elif "salaried" in cat_lower and q["category"] == "Salaried":
            active_questions.append(q_copy)
        elif ("self" in cat_lower or "msme" in cat_lower or "business" in cat_lower) and q["category"] == "Self-Employed / MSME":
            active_questions.append(q_copy)
        elif ("informal" in cat_lower or "gig" in cat_lower or "freelance" in cat_lower or "other" in cat_lower) and q["category"] == "Informal / Gig Economy":
            active_questions.append(q_copy)

    return active_questions


def get_variable_questions_for_category(category: str) -> List[Dict[str, Any]]:
    """
    Returns precisely the 18 optional variable questions for the given category track.
    """
    all_qs = get_questions_for_category(category)
    return [q for q in all_qs if q.get("tier") == "Variable"]


def compute_confidence_score(answered_profile: Dict[str, Any], category: str) -> float:
    """
    Computes live confidence score:
    - Answers across the 10 Mandatory questions build up to 60.0% base confidence (6.0% each).
    - Completing all 10 Mandatory questions yields 60.0% base confidence.
    - Each answered category variable adds its specific weight above 60.0%.
    - Strict cap at 95.0% (Rule 2: Self-reported data lacks third-party bureau APIs).
    """
    cat_lower = (category or "").lower()

    mandatory_keys = [
        "loan_purpose", "target_loan_amount", "tenure_months", "employment_type",
        "net_income", "existing_emi", "rent", "living_expenses", "cibil", "age"
    ]
    mandatory_answered = 0
    for k in mandatory_keys:
        v = answered_profile.get(k)
        if v is not None and v != "" and v != "Select one" and v != "Please select...":
            mandatory_answered += 1

    score = (mandatory_answered / 10.0) * 60.0

    if mandatory_answered == 10:
        for key, val in answered_profile.items():
            if key in MASTER_QUESTIONS:
                q = MASTER_QUESTIONS[key]
                if q["tier"] == "Variable":
                    # Check category match
                    is_match = False
                    if "salaried" in cat_lower and q["category"] == "Salaried":
                        is_match = True
                    elif ("self" in cat_lower or "msme" in cat_lower or "business" in cat_lower) and q["category"] == "Self-Employed / MSME":
                        is_match = True
                    elif ("informal" in cat_lower or "gig" in cat_lower or "freelance" in cat_lower or "other" in cat_lower) and q["category"] == "Informal / Gig Economy":
                        is_match = True

                    if is_match:
                        # Check if answered with non-trivial value
                        if val is not None and val != "" and val != "Select one" and val != "Please select...":
                            score += float(q["weight"])

    return round(min(95.0, max(0.0, score)), 1)



def get_spread_half_width(confidence_score: float) -> float:
    """
    Contracts the rate uncertainty spread symmetrically as confidence increases:
    Spread half-width is ±2.35% at 60.0% confidence, contracting to ±0.35% at 95.0% confidence.
    """
    clamped_conf = min(95.0, max(60.0, confidence_score))
    ratio = (clamped_conf - 60.0) / 35.0  # 0.0 to 1.0
    half_width = 2.0 * (1.0 - ratio) + 0.35
    return round(half_width, 2)
