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
        "label": "Primary Loan Purpose",
        "input_type": "select",
        "options": ["Wedding", "Business Expansion", "Vehicle Purchase", "Home Renovation", "Debt Consolidation", "Medical Emergency"],
        "default": "Wedding",
        "weight": 6.0,
        "impact": "O1, O3",
        "why_we_ask": "Sets baseline loan product classification, default risk tier, and maximum allowable tenure bounds."
    },
    "target_loan_amount": {
        "id": "M02",
        "tier": "Mandatory",
        "category": "Universal",
        "label": "Target Loan Amount (₹)",
        "input_type": "number",
        "default": 800000,
        "min": 10000,
        "step": 10000,
        "weight": 6.0,
        "impact": "O1, O2",
        "why_we_ask": "Sets the requested principal to test against safe borrowing headroom and evaluate affordability."
    },
    "tenure_months": {
        "id": "M03",
        "tier": "Mandatory",
        "category": "Universal",
        "label": "Preferred Repayment Tenure (Months)",
        "input_type": "select",
        "options": [12, 24, 36, 48, 60, 84, 120],
        "default": 48,
        "weight": 6.0,
        "impact": "O4",
        "why_we_ask": "Defines the monthly amortization schedule and determines total interest drag over the life of the loan."
    },
    "employment_type": {
        "id": "M04",
        "tier": "Mandatory",
        "category": "Universal",
        "label": "Primary Employment Structure",
        "input_type": "select",
        "options": ["Salaried", "Self-Employed / MSME", "Informal / Gig Economy"],
        "default": "Salaried",
        "weight": 6.0,
        "impact": "Branching, O2",
        "why_we_ask": "Determines the regulatory bank FOIR benchmark (40% to 55%) and activates category-specific underwriting rules."
    },
    "net_income": {
        "id": "M05",
        "tier": "Mandatory",
        "category": "Universal",
        "label": "Net Monthly In-Hand Income (₹)",
        "input_type": "number",
        "default": 110000,
        "min": 5000,
        "step": 5000,
        "weight": 6.0,
        "impact": "O2, O4",
        "why_we_ask": "The baseline denominator for all debt-to-income limits and personal disposable cash flow math."
    },
    "existing_emi": {
        "id": "M06",
        "tier": "Mandatory",
        "category": "Universal",
        "label": "Total Existing Monthly Loan EMIs (₹)",
        "input_type": "number",
        "default": 14000,
        "min": 0,
        "step": 1000,
        "weight": 6.0,
        "impact": "O2, O4",
        "why_we_ask": "Directly deducted from your income to quantify how much debt headroom remains before hitting risk limits."
    },
    "rent": {
        "id": "M07",
        "tier": "Mandatory",
        "category": "Universal",
        "label": "Monthly Rent / Housing Outflow (₹)",
        "input_type": "number",
        "default": 28000,
        "min": 0,
        "step": 1000,
        "weight": 6.0,
        "impact": "O2, O4",
        "why_we_ask": "Fixed non-negotiable shelter costs deducted directly in real cash flow math (which bank gross formulas ignore)."
    },
    "living_expenses": {
        "id": "M08",
        "tier": "Mandatory",
        "category": "Universal",
        "label": "Essential Monthly Living Costs (₹)",
        "input_type": "number",
        "default": 25000,
        "min": 1000,
        "step": 1000,
        "weight": 6.0,
        "impact": "O2, O4",
        "why_we_ask": "The non-negotiable floor for groceries, healthcare, and utilities needed to protect you from insolvency."
    },
    "cibil": {
        "id": "M09",
        "tier": "Mandatory",
        "category": "Universal",
        "label": "Credit Score (CIBIL)",
        "input_type": "select",
        "options": ["750+", "700–749", "Below 700", "Unknown / Unscored"],
        "default": "750+",
        "weight": 6.0,
        "impact": "O3",
        "why_we_ask": "750+ qualifies for prime corporate rate discounts; unknown widens the interest spread without treating you as a defaulter."
    },
    "age": {
        "id": "M10",
        "tier": "Mandatory",
        "category": "Universal",
        "label": "Borrower Age (Years)",
        "input_type": "number",
        "default": 29,
        "min": 18,
        "max": 75,
        "step": 1,
        "weight": 6.0,
        "impact": "O2, O4",
        "why_we_ask": "Caps loan tenure against the standard 60-year retirement boundary to ensure debts do not carry into retirement."
    },

    # =========================================================================
    # SALARIED VARIABLE QUESTIONS (S01 - S18, 60% -> 95%)
    # =========================================================================
    "employer_tier": {
        "id": "S01",
        "tier": "Variable",
        "category": "Salaried",
        "label": "Employer Corporate Classification",
        "input_type": "select",
        "options": ["Listed Tier-1 Corporate/MNC", "Mid-Market Private Firm", "Early-Stage Startup", "Government / PSU"],
        "default": "Listed Tier-1 Corporate/MNC",
        "weight": 3.0,
        "impact": "O2, O3",
        "why_we_ask": "Tier-1/PSU unlocks the lowest prime corporate spreads and raises allowable FOIR up to 55%."
    },
    "job_vintage_years": {
        "id": "S02",
        "tier": "Variable",
        "category": "Salaried",
        "label": "Continuous Years with Current Employer",
        "input_type": "number",
        "default": 5.0,
        "min": 0.0,
        "step": 0.5,
        "weight": 2.5,
        "impact": "O3",
        "why_we_ask": "Over 3 years at the same firm proves job stability, narrowing rate spreads; <1 year adds a job-hopping risk penalty."
    },
    "career_vintage_years": {
        "id": "S03",
        "tier": "Variable",
        "category": "Salaried",
        "label": "Total Career Experience (Years)",
        "input_type": "number",
        "default": 6.0,
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
        "label": "Salary Deposit Method",
        "input_type": "select",
        "options": ["Direct Bank Transfer (NEFT/RTGS)", "Cash / Cheque"],
        "default": "Direct Bank Transfer (NEFT/RTGS)",
        "weight": 2.0,
        "impact": "O2",
        "why_we_ask": "Digital bank credits validate 100% of income; cash salaries suffer a 25% underwriting haircut."
    },
    "variable_bonus_share_pct": {
        "id": "S05",
        "tier": "Variable",
        "category": "Salaried",
        "label": "Variable Pay / Bonus Share of Total CTC (%)",
        "input_type": "number",
        "default": 0,
        "min": 0,
        "max": 100,
        "step": 5,
        "weight": 2.0,
        "impact": "O2, O4",
        "why_we_ask": "If bonuses exceed 20% of pay, monthly safe capacity is discounted by 15% to protect against bonus volatility."
    },
    "on_notice_or_probation": {
        "id": "S06",
        "tier": "Variable",
        "category": "Salaried",
        "label": "Currently on Probation or Serving Notice Period?",
        "input_type": "select",
        "options": ["No", "Yes"],
        "default": "No",
        "weight": 2.0,
        "impact": "O1, O3",
        "why_we_ask": "Notice period flags impending income discontinuity, adding a 1.5% spread and capping borrowing to 6 months' pay."
    },
    "liquid_savings_months": {
        "id": "S07",
        "tier": "Variable",
        "category": "Salaried",
        "label": "Liquid Savings Runway (Months of Expenses)",
        "input_type": "number",
        "default": 8.0,
        "min": 0.0,
        "step": 1.0,
        "weight": 2.5,
        "impact": "O4",
        "why_we_ask": "Holding 6+ months of living costs drops required emergency buffer from 10% to 5%, expanding safe borrowing headroom."
    },
    "cc_utilization_pct": {
        "id": "S08",
        "tier": "Variable",
        "category": "Salaried",
        "label": "Revolving Credit Card Limit Utilization (%)",
        "input_type": "number",
        "default": 15,
        "min": 0,
        "max": 100,
        "step": 5,
        "weight": 2.0,
        "impact": "O3",
        "why_we_ask": "Utilizing >50% of card limits signals cash stretch and adds 0.50% risk spread; <20% earns prime discounts."
    },
    "credit_inquiries_90d": {
        "id": "S09",
        "tier": "Variable",
        "category": "Salaried",
        "label": "Credit Inquiries in Last 90 Days",
        "input_type": "number",
        "default": 0,
        "min": 0,
        "step": 1,
        "weight": 1.5,
        "impact": "O3",
        "why_we_ask": "Over 3 recent inquiries signals credit hunger, widening the upper interest rate band by +1.0%."
    },
    "quoted_bank_rate": {
        "id": "S10",
        "tier": "Variable",
        "category": "Salaried",
        "label": "Bank's Quoted Pre-Approved Rate (%, Optional)",
        "input_type": "number",
        "default": 0.0,
        "min": 0.0,
        "step": 0.25,
        "weight": 3.0,
        "impact": "Negotiation Card",
        "why_we_ask": "Benchmarks the bank's actual quote against fair regulatory pricing on the Negotiation Card."
    },
    "quoted_processing_fee_pct": {
        "id": "S11",
        "tier": "Variable",
        "category": "Salaried",
        "label": "Quoted Processing Fee (%)",
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
        "label": "Remaining Months on Existing Car/Personal Debt",
        "input_type": "number",
        "default": 24,
        "min": 0,
        "step": 1,
        "weight": 1.5,
        "impact": "O2, O4",
        "why_we_ask": "If existing loans finish within 12 months, future cash headroom expands, giving you greater long-term safety."
    },
    "has_large_upcoming_outlay": {
        "id": "S13",
        "tier": "Variable",
        "category": "Salaried",
        "label": "Major Planned Expenses in Next 12 Months?",
        "input_type": "select",
        "options": ["No", "Yes"],
        "default": "No",
        "weight": 1.5,
        "impact": "O4",
        "why_we_ask": "Planned capital outlays are deducted from emergency reserves, lowering your safe borrowing ceiling."
    },
    "co_applicant_income": {
        "id": "S14",
        "tier": "Variable",
        "category": "Salaried",
        "label": "Co-Applicant / Spouse Net Income (₹/month)",
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
        "label": "Active Home Loan with Tax Deductions?",
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
        "label": "Employee Provident Fund (EPF) Balance > ₹3,00,000?",
        "input_type": "select",
        "options": ["Yes", "No"],
        "default": "Yes",
        "weight": 1.5,
        "impact": "O4, Stress",
        "why_we_ask": "Serves as an emergency distress backstop, reducing vulnerability during macroeconomic shocks."
    },
    "has_health_insurance": {
        "id": "S17",
        "tier": "Variable",
        "category": "Salaried",
        "label": "Employer Comprehensive Health Insurance?",
        "input_type": "select",
        "options": ["Yes", "No"],
        "default": "Yes",
        "weight": 1.0,
        "impact": "O4",
        "why_we_ask": "Comprehensive medical coverage reduces the cash emergency reserve deduction in the safe cash formula."
    },
    "unsecured_loan_count": {
        "id": "S18",
        "tier": "Variable",
        "category": "Salaried",
        "label": "Count of Active Unsecured Personal Loans",
        "input_type": "number",
        "default": 0,
        "min": 0,
        "step": 1,
        "weight": 1.5,
        "impact": "O3",
        "why_we_ask": "Holding more than 2 active personal loans triggers multi-loan leverage spread penalties (+1.0%)."
    },

    # =========================================================================
    # SELF-EMPLOYED / MSME VARIABLES (B01 - B18, 60% -> 95%)
    # =========================================================================
    "itr_profit_annual": {
        "id": "B01",
        "tier": "Variable",
        "category": "Self-Employed / MSME",
        "label": "Net Taxable Profit on Latest Filed ITR (₹/year)",
        "input_type": "number",
        "default": 420000,
        "min": 0,
        "step": 25000,
        "weight": 3.0,
        "impact": "O2",
        "why_we_ask": "Sets the hard ceiling for traditional unsecured banking credit; low reported ITR triggers loan rejections."
    },
    "itr_filing_years": {
        "id": "B02",
        "tier": "Variable",
        "category": "Self-Employed / MSME",
        "label": "Consecutive Years of Filed Business ITRs",
        "input_type": "number",
        "default": 3,
        "min": 0,
        "step": 1,
        "weight": 2.0,
        "impact": "O3",
        "why_we_ask": "Three or more years of filed ITRs proves enterprise stability, cutting lending spreads by 0.75%."
    },
    "gross_monthly_cash_intake": {
        "id": "B03",
        "tier": "Variable",
        "category": "Self-Employed / MSME",
        "label": "Gross Monthly Business Cash Intake (₹)",
        "input_type": "number",
        "default": 85000,
        "min": 10000,
        "step": 5000,
        "weight": 2.5,
        "impact": "O2, O4",
        "why_we_ask": "Captures real operating liquidity to calculate your true debt-servicing capacity rather than artificial tax numbers."
    },
    "has_unencumbered_property": {
        "id": "B04",
        "tier": "Variable",
        "category": "Self-Employed / MSME",
        "label": "Own Debt-Free Commercial Shop or Residential Property?",
        "input_type": "select",
        "options": ["Yes", "No"],
        "default": "Yes",
        "weight": 3.5,
        "impact": "O1, O3 (Product Pivot)",
        "why_we_ask": "Critical Product Pivot: switches your loan from predatory 18%+ unsecured lines to 9.75%–10.5% LAP."
    },
    "property_market_value": {
        "id": "B05",
        "tier": "Variable",
        "category": "Self-Employed / MSME",
        "label": "Conservative Market Value of Unencumbered Property (₹)",
        "input_type": "number",
        "default": 4500000,
        "min": 0,
        "step": 100000,
        "weight": 2.5,
        "impact": "O2",
        "why_we_ask": "Determines maximum LAP sanction capacity using standard conservative 50%–55% Loan-to-Value (LTV)."
    },
    "title_deed_clarity": {
        "id": "B06",
        "tier": "Variable",
        "category": "Self-Employed / MSME",
        "label": "Registered Title Deed Clear & in Your Name?",
        "input_type": "select",
        "options": ["Yes", "No"],
        "default": "Yes",
        "weight": 2.0,
        "impact": "O3",
        "why_we_ask": "Clear registered property title narrows the LAP spread; unpartitioned titles widen interest uncertainty."
    },
    "business_vintage_years": {
        "id": "B07",
        "tier": "Variable",
        "category": "Self-Employed / MSME",
        "label": "Continuous Years Enterprise Has Operated at Location",
        "input_type": "number",
        "default": 14,
        "min": 0,
        "step": 1,
        "weight": 2.0,
        "impact": "O3",
        "why_we_ask": "Five or more years of local shop vintage eliminates relocation risk, earning rate reductions of 0.50%."
    },
    "business_premises_ownership": {
        "id": "B08",
        "tier": "Variable",
        "category": "Self-Employed / MSME",
        "label": "Business Premises Ownership Type",
        "input_type": "select",
        "options": ["Owned (No Rent)", "Rented / Commercial Lease"],
        "default": "Owned (No Rent)",
        "weight": 1.5,
        "impact": "O2, O4",
        "why_we_ask": "An owned store eliminates rental overhead, permanently protecting operating profit margins."
    },
    "seasonal_variance_high": {
        "id": "B09",
        "tier": "Variable",
        "category": "Self-Employed / MSME",
        "label": "Does Monthly Revenue Fluctuate by >35% Across Seasons?",
        "input_type": "select",
        "options": ["Yes (Monsoon Drop)", "No (Consistent)"],
        "default": "Yes (Monsoon Drop)",
        "weight": 4.0,
        "impact": "O4",
        "why_we_ask": "High seasonality anchors your safe EMI strictly to the lowest trough month so you never default during monsoon."
    },
    "co_applicant_income_msme": {
        "id": "B10",
        "tier": "Variable",
        "category": "Self-Employed / MSME",
        "label": "Earning Spouse / Co-Applicant Monthly Income (₹)",
        "input_type": "number",
        "default": 18000,
        "min": 0,
        "step": 2000,
        "weight": 4.0,
        "impact": "O2, O4",
        "why_we_ask": "Adds secondary steady household earnings (e.g. teaching salary) to cushion merchant cash flow."
    },
    "commercial_vehicle_assets": {
        "id": "B11",
        "tier": "Variable",
        "category": "Self-Employed / MSME",
        "label": "Own Commercial Delivery Vehicles Free of Debt?",
        "input_type": "select",
        "options": ["Yes", "No"],
        "default": "No",
        "weight": 1.5,
        "impact": "O3",
        "why_we_ask": "Provides movable asset backing, qualifying you for lower equipment finance spreads."
    },
    "supplier_payment_terms": {
        "id": "B12",
        "tier": "Variable",
        "category": "Self-Employed / MSME",
        "label": "Supplier Payment Terms",
        "input_type": "select",
        "options": ["Immediate Cash Only", "15–30 Days Credit", "60+ Days"],
        "default": "Immediate Cash Only",
        "weight": 1.5,
        "impact": "O4",
        "why_we_ask": "Immediate cash-only suppliers require higher cash cushions, reducing safe borrowing headroom."
    },
    "customer_receivables_days": {
        "id": "B13",
        "tier": "Variable",
        "category": "Self-Employed / MSME",
        "label": "Customer Credit Locked in Unpaid Dues (Days)",
        "input_type": "number",
        "default": 30,
        "min": 0,
        "step": 5,
        "weight": 1.5,
        "impact": "O2, O4",
        "why_we_ask": "Over 45 days of uncollected customer credit applies a 10% haircut on monthly operating cash."
    },
    "average_bank_balance": {
        "id": "B14",
        "tier": "Variable",
        "category": "Self-Employed / MSME",
        "label": "Average Daily Bank Balance (ABB, ₹)",
        "input_type": "number",
        "default": 50000,
        "min": 0,
        "step": 5000,
        "weight": 2.0,
        "impact": "O3",
        "why_we_ask": "Maintaining a healthy daily credit balance in current accounts cuts lending spreads by up to 1.0%."
    },
    "unsecured_mca_portion_pct": {
        "id": "B15",
        "tier": "Variable",
        "category": "Self-Employed / MSME",
        "label": "Share of Current Debt in Merchant Cash Advances / Apps (%)",
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
        "id": "B16",
        "tier": "Variable",
        "category": "Self-Employed / MSME",
        "label": "Projected Net Monthly Margin from New Stock Line (₹)",
        "input_type": "number",
        "default": 15000,
        "min": 0,
        "step": 2000,
        "weight": 1.5,
        "impact": "O2, O4",
        "why_we_ask": "Incremental profits generated by new stock are credited toward future safe repayment capacity."
    },
    "statutory_gst_disputes": {
        "id": "B17",
        "tier": "Variable",
        "category": "Self-Employed / MSME",
        "label": "Any Pending Tax or Municipal Legal Demands?",
        "input_type": "select",
        "options": ["No", "Yes"],
        "default": "No",
        "weight": 1.0,
        "impact": "O3",
        "why_we_ask": "Active tax disputes widen loan spreads by 1.50% and bar access to prime institutional lenders."
    },
    "annual_gstr3b_turnover": {
        "id": "B18",
        "tier": "Variable",
        "category": "Self-Employed / MSME",
        "label": "Annual Gross GSTR-3B Turnover (₹, Optional)",
        "input_type": "number",
        "default": 0,
        "min": 0,
        "step": 50000,
        "weight": 2.0,
        "impact": "O2",
        "why_we_ask": "Verifiable GST filings unlock surrogate bank credit lines up to 10%–15% of annual turnover."
    },

    # =========================================================================
    # INFORMAL / GIG ECONOMY VARIABLES (I01 - I18, 60% -> 95%)
    # =========================================================================
    "payment_bounces_6m": {
        "id": "I01",
        "tier": "Variable",
        "category": "Informal / Gig Economy",
        "label": "Auto-Debit / EMI Bounces in the Last 6 Months",
        "input_type": "number",
        "default": 1,
        "min": 0,
        "step": 1,
        "weight": 3.5,
        "impact": "O1 (Kill-Switch)",
        "why_we_ask": "Mandatory Kill-Switch: Any active bounce in 6 months indicates acute default distress, triggering Don't Borrow."
    },
    "active_app_loan_count": {
        "id": "I02",
        "tier": "Variable",
        "category": "Informal / Gig Economy",
        "label": "Count of Active Instant Digital Loan Apps",
        "input_type": "number",
        "default": 3,
        "min": 0,
        "step": 1,
        "weight": 3.0,
        "impact": "O1, O2",
        "why_we_ask": "Identifies high-frequency digital leverage and activates mandatory debt consolidation rules."
    },
    "app_loan_balance_total": {
        "id": "I03",
        "tier": "Variable",
        "category": "Informal / Gig Economy",
        "label": "Total Outstanding Digital App Loan Debt (₹)",
        "input_type": "number",
        "default": 35000,
        "min": 0,
        "step": 5000,
        "weight": 3.0,
        "impact": "O1, O2",
        "why_we_ask": "Quantifies the exact predatory debt that must be cleared before taking on any new credit."
    },
    "app_loan_apr": {
        "id": "I04",
        "tier": "Variable",
        "category": "Informal / Gig Economy",
        "label": "Highest Interest Rate Charged by Digital Apps (% APR)",
        "input_type": "number",
        "default": 36.0,
        "min": 0.0,
        "step": 1.0,
        "weight": 3.0,
        "impact": "O1, O3",
        "why_we_ask": "Interest above 24% triggers our predatory debt rule, blocking new borrowing until high-cost apps are cleared."
    },
    "productive_income_boost": {
        "id": "I05",
        "tier": "Variable",
        "category": "Informal / Gig Economy",
        "label": "Projected Monthly Income Boost from New Asset (₹)",
        "input_type": "number",
        "default": 3500,
        "min": 0,
        "step": 500,
        "weight": 3.5,
        "impact": "O2, O4",
        "why_we_ask": "Incremental earnings (e.g. EV fuel savings) are credited toward future safe loan repayment capacity."
    },
    "payout_mode": {
        "id": "I06",
        "tier": "Variable",
        "category": "Informal / Gig Economy",
        "label": "Platform Payout Mode",
        "input_type": "select",
        "options": ["Digital App Payouts (UPI/Bank)", "Unrecorded Cash In Hand"],
        "default": "Digital App Payouts (UPI/Bank)",
        "weight": 3.0,
        "impact": "O3",
        "why_we_ask": "Verifiable digital platform payouts unlock priority sector commercial EV rates (11%–13%) over personal loans."
    },
    "platform_active_days_monthly": {
        "id": "I07",
        "tier": "Variable",
        "category": "Informal / Gig Economy",
        "label": "Active Delivery / Work Days Per Month",
        "input_type": "number",
        "default": 24,
        "min": 0,
        "max": 31,
        "step": 1,
        "weight": 3.0,
        "impact": "O2",
        "why_we_ask": "24 or more days validates full-time earnings; under 15 days triggers a 20% volatility haircut."
    },
    "household_adult_earners": {
        "id": "I08",
        "tier": "Variable",
        "category": "Informal / Gig Economy",
        "label": "Count of Adult Earning Members in Household",
        "input_type": "number",
        "default": 1,
        "min": 1,
        "step": 1,
        "weight": 1.5,
        "impact": "O4",
        "why_we_ask": "Quantifies income redundancy: single-earner households face greater vulnerability to medical or job shocks."
    },
    "spouse_employment_status": {
        "id": "I09",
        "tier": "Variable",
        "category": "Informal / Gig Economy",
        "label": "Spouse Employment Status",
        "input_type": "select",
        "options": ["Employed / Earning", "Seeking Work", "Long-Term Unemployed (6+ mos)"],
        "default": "Long-Term Unemployed (6+ mos)",
        "weight": 2.0,
        "impact": "O4, Stress",
        "why_we_ask": "A long-term unemployed spouse increases the stress shock factor from 20% to 30% of income."
    },
    "dependent_children_count": {
        "id": "I10",
        "tier": "Variable",
        "category": "Informal / Gig Economy",
        "label": "Number of Dependent Children",
        "input_type": "number",
        "default": 2,
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
        "label": "Secondary Home Trade (e.g., Home Tailoring)",
        "input_type": "select",
        "options": ["Yes (Active Secondary Income)", "No"],
        "default": "Yes (Active Secondary Income)",
        "weight": 1.5,
        "impact": "O4",
        "why_we_ask": "Diversified household earnings cushion potential downtime from vehicle repairs or platform drops."
    },
    "liquid_emergency_cash_gold": {
        "id": "I12",
        "tier": "Variable",
        "category": "Informal / Gig Economy",
        "label": "Liquid Emergency Cash or Gold Held (₹)",
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
        "label": "Financing a Commercial Electric Vehicle (EV)?",
        "input_type": "select",
        "options": ["Yes (Replaces Petrol Scooter)", "No"],
        "default": "Yes (Replaces Petrol Scooter)",
        "weight": 2.0,
        "impact": "O3, O4",
        "why_we_ask": "EV adoption saves ~₹3,500/month in petrol costs, which is directly credited toward servicing the vehicle installment."
    },
    "informal_moneylender_debt": {
        "id": "I14",
        "tier": "Variable",
        "category": "Informal / Gig Economy",
        "label": "Owe Debt to Informal Daily/Weekly Lenders?",
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
        "label": "Commercial Driver Badge / Clean Registration?",
        "input_type": "select",
        "options": ["Yes", "No"],
        "default": "Yes",
        "weight": 1.5,
        "impact": "O3",
        "why_we_ask": "Commercial badge unlocks asset-hypothecated financing and clean state priority sector subsidies."
    },
    "phone_emi_active": {
        "id": "I16",
        "tier": "Variable",
        "category": "Informal / Gig Economy",
        "label": "Currently Paying Smartphone Installment?",
        "input_type": "select",
        "options": ["Yes", "No"],
        "default": "Yes",
        "weight": 1.0,
        "impact": "O4",
        "why_we_ask": "Smartphone installments must be prioritized: default halts mobile app access and stops all delivery income."
    },
    "medical_emergency_12m": {
        "id": "I17",
        "tier": "Variable",
        "category": "Informal / Gig Economy",
        "label": "Incurred Uninsured Medical Emergency in Past Year?",
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
        "label": "Registered SHG / JLG Group Member?",
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
    Always includes the 10 Universal Mandatory questions.
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
        elif ("self" in cat_lower or "msme" in cat_lower) and q["category"] == "Self-Employed / MSME":
            active_questions.append(q_copy)
        elif ("informal" in cat_lower or "gig" in cat_lower) and q["category"] == "Informal / Gig Economy":
            active_questions.append(q_copy)

    return active_questions


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
        if v is not None and v != "" and v != "Please select...":
            mandatory_answered += 1

    score = (mandatory_answered / 10.0) * 60.0

    if mandatory_answered == 10:
        for key, val in answered_profile.items():
            if key in MASTER_QUESTIONS:
                q = MASTER_QUESTIONS[key]
                if q["tier"] == "Variable":
                    # Check category match
                    if ("salaried" in cat_lower and q["category"] == "Salaried") or \
                       (("self" in cat_lower or "msme" in cat_lower) and q["category"] == "Self-Employed / MSME") or \
                       (("informal" in cat_lower or "gig" in cat_lower) and q["category"] == "Informal / Gig Economy"):
                        # Check if answered with non-trivial value
                        if val is not None and val != "" and val != "Please select...":
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
