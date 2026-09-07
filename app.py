"""
Borrower Copilot (app.py)
Know your safe borrowing limit before you apply for a loan.
Mirrored UI Design, Simplified Conversational Language & Deterministic Underwriting Engine.
Zero-Database, Zero-API, Pure Client-Side Privacy.
"""

import os
import base64
import time
import streamlit as st
import streamlit.components.v1 as components
from engine.underwriting import run_full_underwriting, calculate_pmt
from engine.confidence import (
    compute_confidence_score,
    get_spread_half_width,
    get_questions_for_category,
    get_variable_questions_for_category,
    MASTER_QUESTIONS,
)
from engine.explanations import generate_all_explanations
from engine.negotiation import build_negotiation_card

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Borrower Copilot — Know your safe borrowing limit",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Helper to load images as base64 data URLs for seamless rendering in Streamlit
def load_img_b64(rel_path: str) -> str:
    abs_path = os.path.join(os.path.dirname(__file__), rel_path)
    if os.path.exists(abs_path):
        with open(abs_path, "rb") as f:
            data = f.read()
        return f"data:image/png;base64,{base64.b64encode(data).decode('utf-8')}"
    return ""

img_consultation = load_img_b64("assets/advisor-consultation.png")
img_tablet = load_img_b64("assets/advisor-tablet.png")

# -----------------------------------------------------------------------------
# MIRRORED CSS DESIGN SYSTEM
# -----------------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root {
  --bg: #ffffff;
  --bg-soft: #f7f2f0;
  --bg-soft-2: #f3ecef;
  --fg: #241a22;
  --fg-muted: #6e6169;
  --fg-faint: #978c90;
  --brand: #4b2440;
  --brand-dark: #341830;
  --brand-soft: #f1e6ed;
  --border: #e6dfe0;
  --good: #2e7d5b;
  --good-soft: #e7f3ec;
  --warn: #ad3e33;
  --warn-soft: #fbeae7;
  --radius-lg: 16px;
  --radius-md: 10px;
  --radius-sm: 6px;
  --measure: 1120px;
  --ease: cubic-bezier(0.2, 0.7, 0.3, 1);
  --fs-h1: clamp(2rem, 4vw, 2.9rem);
  --fs-h2: clamp(1.5rem, 2.6vw, 2rem);
  --fs-h3: 1.2rem;
  --fs-body: 1.02rem;
  --fs-meta: 0.86rem;
}

/* Base Canvas Overrides */
html, body, .stApp, div[data-testid="stAppViewContainer"] {
  margin: 0;
  font-family: "Poppins", system-ui, sans-serif !important;
  color: var(--fg) !important;
  background-color: var(--bg) !important;
  font-size: var(--fs-body);
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
}

header[data-testid="stHeader"] {
  display: none !important;
}

.main .block-container {
  max-width: var(--measure) !important;
  margin: 0 auto !important;
  padding: 0 clamp(1.25rem, 4vw, 2.5rem) 4rem clamp(1.25rem, 4vw, 2.5rem) !important;
}

.mono, .mono-font {
  font-family: "JetBrains Mono", monospace !important;
}

h1, h2, h3, h4 {
  font-family: "Poppins", sans-serif !important;
  font-weight: 600 !important;
  line-height: 1.22 !important;
  color: var(--fg) !important;
  letter-spacing: -0.01em !important;
}

p {
  margin: 0;
}

/* Topbar */
.topbar {
  border-bottom: 1px solid var(--border);
  margin-bottom: 1.5rem;
}
.topbar-wrap {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 1.35rem;
  padding-bottom: 1.35rem;
}
.brandmark {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  font-weight: 600;
  font-size: 1.05rem;
  color: var(--fg);
}
.brandmark .dot {
  width: 9px;
  height: 9px;
  border-radius: 50%;
  background: var(--brand);
  display: inline-block;
}
.topbar .status {
  font-size: var(--fs-meta);
  color: var(--fg-muted);
}
.topbar .status b {
  color: var(--brand);
  font-weight: 600;
}

/* Hero Section */
.hero {
  padding: clamp(1rem, 4vw, 2.5rem) 0 clamp(1.5rem, 3vw, 2rem);
}
.hero-inner {
  max-width: 720px;
}
.eyebrow {
  font-size: var(--fs-meta);
  color: var(--brand);
  font-weight: 600;
  margin-bottom: 0.9rem;
  display: block;
}
.hero h1 {
  font-size: var(--fs-h1);
  margin-bottom: 1.1rem;
}
.hero .lede {
  font-size: 1.12rem;
  color: var(--fg-muted);
  max-width: 56ch;
  line-height: 1.6;
}
.trust-line {
  margin-top: 1.4rem;
  font-size: var(--fs-meta);
  color: var(--fg-faint);
}

.signals {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 0;
  margin-top: 2.4rem;
  border-top: 1px solid var(--border);
}
.signals div {
  padding: 1.1rem 1.2rem 1.1rem 0;
  border-right: 1px solid var(--border);
}
.signals div:last-child {
  border-right: none;
}
.signals .k {
  font-family: "JetBrains Mono", monospace;
  font-size: 0.78rem;
  color: var(--brand);
  display: block;
  margin-bottom: 0.35rem;
}
.signals .v {
  font-size: 0.92rem;
  color: var(--fg-muted);
}

@media (max-width: 820px) {
  .signals {
    grid-template-columns: repeat(2, 1fr);
  }
  .signals div {
    border-right: 1px solid var(--border);
  }
  .signals div:nth-child(2n) {
    border-right: none;
  }
}

/* Photo Blocks */
.photo-block {
  padding: clamp(1.5rem, 4vw, 2.5rem) 0;
}
.photo-card {
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  overflow: hidden;
  background: var(--bg-soft);
}
.photo-card img {
  display: block;
  width: 100%;
  max-height: 420px;
  object-fit: cover;
  object-position: center 25%;
}
.photo-caption {
  padding: 1.1rem 1.4rem;
  font-size: 0.95rem;
  color: var(--fg-muted);
  font-style: italic;
  border-top: 1px solid var(--border);
}

/* Floating & Sticky Accuracy Meter */
div[data-testid="stElementContainer"]:has(.accuracy-dock) {
  position: -webkit-sticky !important;
  position: sticky !important;
  top: 0.75rem !important;
  z-index: 99999 !important;
}

.accuracy-dock {
  position: relative !important;
  z-index: 99999 !important;
  background: rgba(255, 255, 255, 0.96) !important;
  backdrop-filter: blur(12px) !important;
  -webkit-backdrop-filter: blur(12px) !important;
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 0.9rem 1.25rem;
  margin-bottom: 1.5rem;
  box-shadow: 0 8px 24px -4px rgba(75, 36, 64, 0.16), 0 2px 6px rgba(0, 0, 0, 0.06) !important;
  transition: box-shadow 0.2s ease;
}
.acc-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.4rem;
}
.acc-title {
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--brand);
}
.acc-badge {
  font-size: 0.76rem;
  font-weight: 600;
  padding: 0.2rem 0.65rem;
  border-radius: 99px;
  font-family: "JetBrains Mono", monospace;
}
.acc-bar-bg {
  width: 100%;
  height: 7px;
  background-color: var(--border);
  border-radius: 99px;
  overflow: hidden;
  margin-bottom: 0.4rem;
}
.acc-bar-fill {
  height: 100%;
  background: linear-gradient(90deg, #ad3e33, #4b2440, #2e7d5b);
  border-radius: 99px;
  transition: width 0.3s ease;
}
.acc-desc {
  font-size: 0.82rem;
  color: var(--fg-muted);
  line-height: 1.4;
}

/* Card Shell */
.card {
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: clamp(1.5rem, 3vw, 2.25rem);
  margin-bottom: 2rem;
}

.step {
  margin-top: 1.2rem;
  margin-bottom: 1.8rem;
}
.step-head {
  display: flex;
  align-items: baseline;
  gap: 0.7rem;
  margin-bottom: 0.4rem;
}
.step-num {
  font-family: "JetBrains Mono", monospace;
  font-size: 0.85rem;
  color: var(--brand);
  border: 1px solid var(--brand-soft);
  background: var(--brand-soft);
  border-radius: 99px;
  width: 1.9rem;
  height: 1.9rem;
  display: flex;
  align-items: center;
  justify-content: center;
  flex: none;
}
.step-head h3 {
  font-size: var(--fs-h3);
}
.step-sub {
  color: var(--fg-muted);
  font-size: 0.92rem;
  margin: 0.15rem 0 1.2rem 2.6rem;
}

.field-hint {
  font-size: 0.82rem;
  color: var(--fg-faint);
  margin-top: -0.35rem;
  margin-bottom: 0.6rem;
}

/* Form inputs styling */
div[data-baseweb="input"], div[data-baseweb="select"] {
  border: 1px solid var(--border) !important;
  border-radius: var(--radius-sm) !important;
  background: var(--bg) !important;
}
div[data-baseweb="input"]:focus-within, div[data-baseweb="select"]:focus-within {
  border-color: var(--brand) !important;
}
div[data-baseweb="input"] input, div[data-baseweb="select"] * {
  font-family: "Poppins", sans-serif !important;
  color: var(--fg) !important;
  font-size: 0.98rem !important;
}

/* Form button styling */
button[kind="primaryFormSubmit"], button[kind="primary"] {
  background: var(--brand) !important;
  color: #ffffff !important;
  font-family: "Poppins", sans-serif !important;
  font-weight: 600 !important;
  font-size: 1rem !important;
  padding: 0.95rem 2.2rem !important;
  border-radius: 99px !important;
  border: 1px solid transparent !important;
  cursor: pointer !important;
  box-shadow: 0 4px 14px rgba(75, 36, 64, 0.2) !important;
  transition: transform 0.12s var(--ease), background 0.15s var(--ease) !important;
}
button[kind="primaryFormSubmit"]:hover, button[kind="primary"]:hover {
  background: var(--brand-dark) !important;
}
button[kind="primaryFormSubmit"]:active, button[kind="primary"]:active {
  transform: scale(0.98) !important;
}

button[kind="secondary"] {
  background: transparent !important;
  color: var(--brand) !important;
  border: 1px solid var(--border) !important;
  border-radius: 99px !important;
  font-family: "Poppins", sans-serif !important;
  font-weight: 600 !important;
  padding: 0.75rem 1.6rem !important;
}
button[kind="secondary"]:hover {
  border-color: var(--brand) !important;
}

.cta-row {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.6rem;
  margin-top: 1.5rem;
  text-align: center;
}
.cta-sub {
  font-size: 0.85rem;
  color: var(--fg-faint);
}

/* Section Headings */
.section-label {
  font-size: var(--fs-meta);
  color: var(--brand);
  font-weight: 600;
  margin-bottom: 0.5rem;
  display: block;
}
.section-head h2 {
  margin-bottom: 0.5rem;
}
.section-head p {
  color: var(--fg-muted);
  max-width: 62ch;
}

/* Verdict Banners */
#results-section, .verdict {
  scroll-margin-top: 95px !important;
}
#form-section {
  scroll-margin-top: 25px !important;
}
.verdict {
  border-radius: var(--radius-lg);
  padding: clamp(1.5rem, 3vw, 2rem);
  display: flex;
  align-items: flex-start;
  gap: 1.1rem;
  border: 1px solid var(--border);
  margin-bottom: 1.5rem;
}
.verdict.borrow {
  background: var(--good-soft);
  border-color: #cfe7da;
}
.verdict.less {
  background: var(--brand-soft);
  border-color: #e3cfda;
}
.verdict.no {
  background: var(--warn-soft);
  border-color: #f0d3ce;
}
.verdict .mark {
  font-size: 1.8rem;
  line-height: 1;
  flex: none;
  margin-top: 0.1rem;
}
.verdict h2 {
  font-size: 1.4rem;
  margin-bottom: 0.4rem;
}
.verdict.borrow h2 {
  color: var(--good) !important;
}
.verdict.less h2 {
  color: var(--brand) !important;
}
.verdict.no h2 {
  color: var(--warn) !important;
}
.verdict p {
  color: var(--fg);
  font-size: 0.98rem;
  line-height: 1.6;
}

/* Result Cards Grid */
.result-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.25rem;
  margin-top: 1.25rem;
  margin-bottom: 1.5rem;
}
@media (max-width: 760px) {
  .result-grid {
    grid-template-columns: 1fr;
  }
}
.result-card {
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 1.5rem;
  background: var(--bg);
}
.result-card h3 {
  font-size: 1.05rem;
  margin-bottom: 1rem;
}
.figure-row {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  padding: 0.65rem 0;
  border-bottom: 1px solid var(--border);
}
.figure-row:last-of-type {
  border-bottom: none;
}
.figure-row .label {
  color: var(--fg-muted);
  font-size: 0.92rem;
}
.figure-row .value {
  font-family: "JetBrains Mono", monospace;
  font-weight: 600;
  font-size: 1.05rem;
}
.figure-row .value.big {
  font-size: 1.25rem;
  color: var(--brand);
}

.callout {
  margin-top: 1rem;
  padding: 0.9rem 1rem;
  background: var(--bg-soft);
  border-radius: var(--radius-sm);
  font-size: 0.88rem;
  color: var(--fg-muted);
  line-height: 1.5;
}
.callout b {
  color: var(--fg);
}

.pill-note {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  font-size: 0.85rem;
  font-weight: 500;
  padding: 0.4rem 0.8rem;
  border-radius: 99px;
  margin-top: 0.6rem;
}
.pill-note.ok {
  background: var(--good-soft);
  color: var(--good);
}
.pill-note.bad {
  background: var(--warn-soft);
  color: var(--warn);
}

/* Compare Table */
.compare-wrap {
  overflow-x: auto;
  margin-top: 1rem;
}
table.compare {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.9rem;
  min-width: 480px;
}
table.compare th, table.compare td {
  padding: 0.7rem 0.6rem;
  text-align: left;
  border-bottom: 1px solid var(--border);
}
table.compare th {
  color: var(--fg-muted);
  font-weight: 500;
  font-size: 0.82rem;
}
table.compare td.mono, table.compare th.mono {
  font-family: "JetBrains Mono", monospace;
}
table.compare tr.current td {
  background: var(--brand-soft);
  font-weight: 600;
}
table.compare tr.current td:first-child {
  border-top-left-radius: var(--radius-sm);
  border-bottom-left-radius: var(--radius-sm);
}
table.compare tr.current td:last-child {
  border-top-right-radius: var(--radius-sm);
  border-bottom-right-radius: var(--radius-sm);
}

/* Loan Negotiation Card */
.negotiation {
  margin-top: 1.5rem;
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: clamp(1.5rem, 3vw, 2.25rem);
  background: var(--bg-soft);
}
.negotiation h3 {
  font-size: 1.2rem;
  margin-bottom: 1.2rem;
}
.neg-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
}
@media (max-width: 760px) {
  .neg-grid {
    grid-template-columns: 1fr;
  }
}
.neg-block h4 {
  font-size: 0.86rem;
  color: var(--brand);
  font-weight: 600;
  margin-bottom: 0.6rem;
}
.neg-block ul {
  margin: 0;
  padding-left: 1.2rem;
}
.neg-block li {
  margin-bottom: 0.45rem;
  font-size: 0.92rem;
  line-height: 1.5;
}
.script-box {
  margin-top: 1.4rem;
  background: var(--bg);
  border: 1px dashed var(--border);
  border-radius: var(--radius-md);
  padding: 1.15rem 1.35rem;
  font-size: 0.95rem;
  font-style: italic;
  color: var(--fg);
  line-height: 1.6;
}

/* No-Borrow Card */
.no-borrow-card {
  border: 1px solid #f0d3ce;
  background: var(--warn-soft);
  border-radius: var(--radius-lg);
  padding: clamp(1.5rem, 3vw, 2rem);
  margin-top: 1.25rem;
}
.no-borrow-card h3 {
  color: var(--warn) !important;
  margin-bottom: 0.7rem;
}
.no-borrow-card ol {
  margin: 0.8rem 0 0;
  padding-left: 1.3rem;
}
.no-borrow-card li {
  margin-bottom: 0.45rem;
  font-size: 0.92rem;
}

/* Persona Test Cards */
.persona-card {
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 1.1rem;
  min-height: 165px;
  margin-bottom: 0.8rem;
}
.persona-card b {
  color: var(--brand);
  font-size: 1rem;
}
.persona-card .meta {
  font-size: 0.75rem;
  color: var(--fg-muted);
  text-transform: uppercase;
  font-weight: 600;
  margin-bottom: 0.4rem;
  display: block;
}
.persona-card p {
  font-size: 0.85rem;
  color: var(--fg);
  line-height: 1.45;
}

/* Footer */
footer {
  border-top: 1px solid var(--border);
  margin-top: 3rem;
  padding: 2.2rem 0;
}
footer .fine {
  font-size: 0.82rem;
  color: var(--fg-faint);
  max-width: 80ch;
  line-height: 1.6;
}
footer .fine + .fine {
  margin-top: 0.6rem;
}
footer .foot-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  flex-wrap: wrap;
  gap: 0.6rem;
}

div[data-testid="stExpander"] {
  background: var(--bg) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius-md) !important;
  margin-top: 1rem;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# BENCHMARK PERSONA PROFILES
# -----------------------------------------------------------------------------
PERSONAS = {
    "priya": {
        "name": "Priya, 29 (Salaried MNC Professional)",
        "desc": "29 yrs, Bengaluru. Software engineer at Tier-1 MNC. Net ₹1,10,000/mo. Car loan ₹14k/mo. CIBIL 780. Wants ₹8L personal loan for wedding.",
        "data": {
            "loan_purpose": "Personal needs",
            "target_loan_amount": 800000,
            "tenure_months": 48,
            "employment_type": "Salaried job",
            "net_income": 110000,
            "existing_emi": 14000,
            "rent": 28000,
            "living_expenses": 25000,
            "cibil": "750–799",
            "age": 29,
            "employer_tier": "Listed Tier-1 Corporate/MNC",
            "job_vintage_years": 5.0,
            "career_vintage_years": 6.0,
            "salary_credit_mode": "Direct Bank Transfer (NEFT/RTGS)",
            "variable_bonus_share_pct": 10,
            "on_notice_or_probation": "No",
            "liquid_savings_months": 8.0,
            "cc_utilization_pct": 15,
            "credit_inquiries_90d": 0,
            "quoted_bank_rate": 13.5,
            "quoted_processing_fee_pct": 1.0,
            "largest_loan_remaining_mos": 24,
            "has_large_upcoming_outlay": "No",
            "co_applicant_income": 0,
            "home_loan_tax_benefit": "No",
            "epf_balance_above_3l": "Yes",
            "has_health_insurance": "Yes",
            "unsecured_loan_count": 0
        }
    },
    "ravi": {
        "name": "Ravi, 42 (Kirana Store Owner / Business)",
        "desc": "42 yrs, Mysuru. Kirana owner for 14 yrs. Cash income ₹85k/mo, ITR ₹4.2L/yr. Owns ₹45L unencumbered shop premises. Unscored. Wants ₹15L for stock/vehicle.",
        "data": {
            "loan_purpose": "Business",
            "target_loan_amount": 1500000,
            "tenure_months": 84,
            "employment_type": "Self-employed",
            "net_income": 85000,
            "existing_emi": 0,
            "rent": 0,
            "living_expenses": 28000,
            "cibil": "I don't know",
            "age": 42,
            "itr_profit_annual": 420000,
            "itr_filing_years": 3,
            "gross_monthly_cash_intake": 85000,
            "has_unencumbered_property": "Yes",
            "property_market_value": 4500000,
            "title_deed_clarity": "Yes",
            "business_vintage_years": 14,
            "business_premises_ownership": "Owned (No Rent)",
            "seasonal_variance_high": "Yes (Monsoon Drop)",
            "co_applicant_income_msme": 18000,
            "commercial_vehicle_assets": "No",
            "supplier_payment_terms": "Immediate Cash Only",
            "customer_receivables_days": 30,
            "average_bank_balance": 50000,
            "unsecured_mca_portion_pct": 0,
            "expansion_margin_boost": 15000,
            "statutory_gst_disputes": "No",
            "annual_gstr3b_turnover": 3600000
        }
    },
    "anita": {
        "name": "Anita, 35 (Delivery Fleet Partner)",
        "desc": "35 yrs, Hubballi. Delivery fleet rider & tailoring. Net ₹28k/mo, 2 kids, husband unemployed. 3 app loans totaling ₹35k at 36% APR. 1 bounce last month. Wants ₹1.5L for electric scooter.",
        "data": {
            "loan_purpose": "Vehicle",
            "target_loan_amount": 150000,
            "tenure_months": 24,
            "employment_type": "Freelance / Contract work",
            "net_income": 28000,
            "existing_emi": 1500,
            "rent": 5000,
            "living_expenses": 18000,
            "cibil": "Below 600",
            "age": 35,
            "payment_bounces_6m": 1,
            "active_app_loan_count": 3,
            "app_loan_balance_total": 35000,
            "app_loan_apr": 36.0,
            "productive_income_boost": 3500,
            "payout_mode": "Digital App Payouts (UPI/Bank)",
            "platform_active_days_monthly": 24,
            "household_adult_earners": 1,
            "spouse_employment_status": "Long-Term Unemployed (6+ mos)",
            "dependent_children_count": 2,
            "secondary_trade_income": "Yes (Active Secondary Income)",
            "liquid_emergency_cash_gold": 0,
            "is_ev_vehicle": "Yes (Replaces Petrol Scooter)",
            "informal_moneylender_debt": "No",
            "has_commercial_driving_badge": "Yes",
            "phone_emi_active": "Yes",
            "medical_emergency_12m": "No",
            "shg_jlg_member": "No"
        }
    }
}

# -----------------------------------------------------------------------------
# SESSION STATE INITIALIZATION
# -----------------------------------------------------------------------------
if "profile" not in st.session_state:
    st.session_state.profile = {}
    st.session_state.active_profile_label = "Not started"
    st.session_state.has_calculated = False

if "calculated_data" not in st.session_state:
    st.session_state.calculated_data = None

if "form_version" not in st.session_state:
    st.session_state.form_version = 0

if "scroll_to" not in st.session_state:
    st.session_state.scroll_to = None

if "scroll_trigger" not in st.session_state:
    st.session_state.scroll_trigger = 0

if "last_executed_scroll_trigger" not in st.session_state:
    st.session_state.last_executed_scroll_trigger = -1

def prep_math_profile(raw_profile: dict) -> dict:
    """Normalizes raw profile inputs for deterministic underwriting."""
    mp = {k: v for k, v in raw_profile.items() if v is not None and v != "" and v != "Select one"}

    # Map employment type to engine categories
    emp = str(mp.get("employment_type") or mp.get("incomeSource", "")).lower()
    if "salaried" in emp:
        mp["employment_type"] = "Salaried"
    elif "self" in emp or "business" in emp:
        mp["employment_type"] = "Self-Employed / MSME"
    else:
        mp["employment_type"] = "Informal / Gig Economy"

    # Map CIBIL options
    cib = str(mp.get("cibil", "")).lower()
    if "800" in cib or "750" in cib:
        mp["cibil"] = "750+"
    elif "700" in cib:
        mp["cibil"] = "700–749"
    elif "600" in cib or "500" in cib or "below" in cib:
        mp["cibil"] = "Below 700"
    elif "unknown" in cib or "don't" in cib or "dont" in cib:
        mp["cibil"] = "Unknown / Unscored"

    if mp.get("has_unencumbered_property") in ["Yes", True, "yes"]:
        mp["has_unencumbered_property"] = True
    if mp.get("seasonal_variance_high") in ["Yes", "Yes (Monsoon Drop)", True, "yes"]:
        mp["seasonal_variance_high"] = True
    if mp.get("is_ev_vehicle") in ["Yes", "Yes (Replaces Petrol Scooter)", True, "yes"]:
        mp["is_ev_vehicle"] = True

    return mp

def trigger_redirect(destination: str = "results"):
    st.session_state.scroll_to = destination
    st.session_state.scroll_trigger = st.session_state.get("scroll_trigger", 0) + 1

def apply_persona(key: str):
    """Loads a benchmark borrower persona and calculates results immediately."""
    st.session_state.form_version = st.session_state.get("form_version", 0) + 1
    fv = st.session_state.form_version

    # Clear previous widget keys so widgets re-initialize with fresh values
    for k in list(st.session_state.keys()):
        if k.startswith("field_"):
            del st.session_state[k]

    if key in PERSONAS:
        data = dict(PERSONAS[key]["data"])
        st.session_state.profile = dict(data)
        st.session_state.active_profile_label = PERSONAS[key]["name"]

        math_profile = prep_math_profile(data)
        results = run_full_underwriting(math_profile)
        explanations = generate_all_explanations(math_profile, results)
        card = build_negotiation_card(math_profile, results)
        st.session_state.calculated_data = {
            "results": results,
            "explanations": explanations,
            "card": card,
            "profile_snapshot": dict(math_profile),
            "label": PERSONAS[key]["name"]
        }
        st.session_state.has_calculated = True
        trigger_redirect("results")
    else:
        # Reset to empty state
        st.session_state.profile = {}
        st.session_state.active_profile_label = "Not started"
        st.session_state.has_calculated = False
        st.session_state.calculated_data = None
        trigger_redirect("form")

# -----------------------------------------------------------------------------
# TOPBAR
# -----------------------------------------------------------------------------
profile_status_text = st.session_state.active_profile_label if st.session_state.get("active_profile_label") and st.session_state.active_profile_label != "Not started" else ""
status_desc = f"Profile: <b>{profile_status_text}</b> · " if profile_status_text else ""

st.markdown(f"""
<div class="topbar">
  <div class="topbar-wrap">
    <div class="brandmark"><span class="dot"></span>Borrower Copilot</div>
    <div class="status">{status_desc}Status: <b>{'Complete' if st.session_state.has_calculated else 'Not started'}</b></div>
  </div>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# HERO SECTION
# -----------------------------------------------------------------------------
st.markdown("""
<header class="hero">
  <div class="hero-inner">
    <span class="eyebrow">Loan borrowing guide</span>
    <h1>Complete Borrower Insight: Know Your Borrowing Limit</h1>
    <p class="lede">
      Before you walk into a lender, answer a few honest questions about your income and expenses.
      You'll get a clear number for what you can afford, a fair interest rate to ask for, and a
      one-page guide for the conversation with your bank.
    </p>
    <p class="trust-line">
      No login required · No credit check · Your results are based only on what you enter here
    </p>
  </div>

  <div class="signals">
    <div>
      <span class="k mono">01</span><span class="v">How much you can afford to borrow</span>
    </div>
    <div>
      <span class="k mono">02</span><span class="v">What monthly payment fits your budget</span>
    </div>
    <div>
      <span class="k mono">03</span><span class="v">What interest rate is reasonable for you</span>
    </div>
    <div>
      <span class="k mono">04</span><span class="v">How long you should take to repay</span>
    </div>
  </div>
</header>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# PHOTO BLOCK 1: CONSULTATION
# -----------------------------------------------------------------------------
if img_consultation:
    st.markdown(f"""
    <div class="photo-block">
      <div class="photo-card">
        <img src="{img_consultation}" alt="A loan officer talks through borrowing options with a couple, using a laptop to show the numbers." />
      </div>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# DYNAMIC FLOATING ACCURACY METER
# -----------------------------------------------------------------------------
fv = st.session_state.get("form_version", 0)

# Sync widget inputs from st.session_state into st.session_state.profile
for field in [
    "loan_purpose", "target_loan_amount", "tenure_months", "employment_type",
    "net_income", "existing_emi", "rent", "living_expenses", "cibil", "age"
]:
    k = f"field_{field}_{fv}"
    if k in st.session_state:
        val = st.session_state[k]
        if val is not None and val != "" and val != "Select one":
            st.session_state.profile[field] = val
        elif k in st.session_state and (val is None or val == "" or val == "Select one") and field in st.session_state.profile:
            del st.session_state.profile[field]

# Also sync any Step 4 optional fields if present
for k in list(st.session_state.keys()):
    if k.startswith("field_") and k.endswith(f"_{fv}"):
        raw_k = k[len("field_"):-len(f"_{fv}")]
        if raw_k not in [
            "loan_purpose", "target_loan_amount", "tenure_months", "employment_type",
            "net_income", "existing_emi", "rent", "living_expenses", "cibil", "age"
        ]:
            val = st.session_state[k]
            if val is not None and val != "" and val != "Select one":
                st.session_state.profile[raw_k] = val
            elif raw_k in st.session_state.profile and (val is None or val == "" or val == "Select one"):
                del st.session_state.profile[raw_k]

curr_cat = st.session_state.profile.get("employment_type", "")
conf_score = compute_confidence_score(st.session_state.profile, curr_cat)
spread_width = get_spread_half_width(conf_score)

if conf_score == 0.0:
    badge_bg = "var(--warn-soft)"
    badge_color = "var(--warn)"
    badge_text = "⚡ Incomplete"
    acc_msg = "Answer the basic questions in Steps 1 to 3 below to unlock your baseline 60% estimate."
elif conf_score < 60.0:
    answered_count = sum(
        1 for k in [
            "loan_purpose", "target_loan_amount", "tenure_months", "employment_type",
            "net_income", "existing_emi", "rent", "living_expenses", "cibil", "age"
        ] if st.session_state.profile.get(k) is not None and st.session_state.profile.get(k) != ""
    )
    badge_bg = "var(--warn-soft)"
    badge_color = "var(--warn)"
    badge_text = f"⚡ {answered_count}/10 answered"
    acc_msg = f"{answered_count} of 10 basic questions answered. Keep going to reach the 60% baseline estimate."
elif conf_score < 75.0:
    badge_bg = "var(--brand-soft)"
    badge_color = "var(--brand)"
    badge_text = f"±{spread_width:.2f}% spread"
    acc_msg = f"Solid baseline (60% accuracy, ±{spread_width:.2f}% spread). Answer the quick optional questions in Step 4 to tighten your rate range."
else:
    badge_bg = "var(--good-soft)"
    badge_color = "var(--good)"
    badge_text = f"🎯 ±{spread_width:.2f}% Calibrated"
    acc_msg = f"High accuracy ({conf_score:.0f}%)! Your safe limit and interest rate are tightly calibrated to your profile."

st.markdown(f"""
<div class="accuracy-dock">
  <div class="acc-header">
    <div class="acc-title">🎯 How reliable your estimate is: <span class="mono" style="font-weight:700; font-size:1.05rem;">{conf_score:.0f}%</span></div>
    <div class="acc-badge" style="background:{badge_bg}; color:{badge_color};">{badge_text}</div>
  </div>
  <div class="acc-bar-bg">
    <div class="acc-bar-fill" style="width: {conf_score}%;"></div>
  </div>
  <div class="acc-desc">{acc_msg}</div>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# FORM SECTION (THE 3 CORE STEPS + STEP 4 ACCURACY BOOSTER)
# -----------------------------------------------------------------------------
st.markdown('<div id="form-section"></div>', unsafe_allow_html=True)

with st.container(border=True):
    # STEP 1: YOUR LOAN
    st.markdown("""
    <div class="step">
      <div class="step-head">
        <span class="step-num mono">1</span>
        <h3>Your loan</h3>
      </div>
      <p class="step-sub">Tell us about the loan you're planning to take.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        purpose_opts = ["Personal needs", "Education", "Medical expenses", "Home", "Vehicle", "Business", "Other"]
        cur_p = st.session_state.profile.get("loan_purpose")
        p_idx = purpose_opts.index(cur_p) if cur_p in purpose_opts else None
        val_purpose = st.selectbox("What do you need the loan for?", options=purpose_opts, index=p_idx, placeholder="Select one...", key=f"field_loan_purpose_{fv}")

    with col2:
        cur_amt = st.session_state.profile.get("target_loan_amount")
        val_amount = st.number_input(
            "How much do you want to borrow? (₹)",
            min_value=1000,
            max_value=100000000,
            step=10000,
            value=int(cur_amt) if cur_amt is not None else None,
            placeholder="e.g. 500000",
            key=f"field_target_loan_amount_{fv}"
        )
        st.markdown('<div class="field-hint">The loan amount you need.</div>', unsafe_allow_html=True)

    col3, col4 = st.columns(2)
    with col3:
        tenure_opts = [12, 24, 36, 48, 60, 72, 84]
        cur_t = st.session_state.profile.get("tenure_months")
        t_idx = tenure_opts.index(int(cur_t)) if (cur_t is not None and int(cur_t) in tenure_opts) else None
        val_tenure = st.selectbox("How many months will you take to repay?", options=tenure_opts, format_func=lambda x: f"{x} months", index=t_idx, placeholder="Select tenure...", key=f"field_tenure_months_{fv}")

    with col4:
        inc_opts = ["Salaried job", "Self-employed", "Business", "Freelance / Contract work", "Other"]
        cur_inc = st.session_state.profile.get("employment_type")
        inc_idx = inc_opts.index(cur_inc) if cur_inc in inc_opts else None
        val_income_source = st.selectbox("What is your main source of income?", options=inc_opts, index=inc_idx, placeholder="Select one...", key=f"field_employment_type_{fv}")

    cur_inc_val = st.session_state.profile.get("net_income")
    val_income = st.number_input(
        "What is your monthly take-home income? (₹)",
        min_value=0,
        max_value=10000000,
        step=5000,
        value=int(cur_inc_val) if cur_inc_val is not None else None,
        placeholder="e.g. 75000",
        key=f"field_net_income_{fv}"
    )
    st.markdown('<div class="field-hint">The amount you receive after deductions.</div>', unsafe_allow_html=True)

    st.markdown("<hr style='border:0; border-top:1px solid var(--border); margin:1.5rem 0;'>", unsafe_allow_html=True)

    # STEP 2: YOUR MONTHLY EXPENSES
    st.markdown("""
    <div class="step">
      <div class="step-head">
        <span class="step-num mono">2</span>
        <h3>Your monthly expenses</h3>
      </div>
      <p class="step-sub">This helps us see how much you have left after your regular costs.</p>
    </div>
    """, unsafe_allow_html=True)

    col5, col6 = st.columns(2)
    with col5:
        cur_emi = st.session_state.profile.get("existing_emi")
        val_existing_emi = st.number_input(
            "Other loan payments each month (₹)",
            min_value=0,
            max_value=10000000,
            step=1000,
            value=int(cur_emi) if cur_emi is not None else None,
            placeholder="e.g. 0 if none",
            key=f"field_existing_emi_{fv}"
        )
        st.markdown('<div class="field-hint">Include all your current loan EMIs.</div>', unsafe_allow_html=True)

    with col6:
        cur_rent = st.session_state.profile.get("rent")
        val_rent = st.number_input(
            "Rent or housing payment each month (₹)",
            min_value=0,
            max_value=10000000,
            step=1000,
            value=int(cur_rent) if cur_rent is not None else None,
            placeholder="e.g. 0 if none",
            key=f"field_rent_{fv}"
        )

    cur_living = st.session_state.profile.get("living_expenses")
    val_essential = st.number_input(
        "Essential expenses each month (₹)",
        min_value=0,
        max_value=10000000,
        step=1000,
        value=int(cur_living) if cur_living is not None else None,
        placeholder="e.g. 20000",
        key=f"field_living_expenses_{fv}"
    )
    st.markdown('<div class="field-hint">Food, bills, travel and other necessary costs.</div>', unsafe_allow_html=True)

    st.markdown("<hr style='border:0; border-top:1px solid var(--border); margin:1.5rem 0;'>", unsafe_allow_html=True)

    # STEP 3: YOUR CREDIT AND AGE
    st.markdown("""
    <div class="step">
      <div class="step-head">
        <span class="step-num mono">3</span>
        <h3>Your credit and age</h3>
      </div>
      <p class="step-sub">This helps us estimate a realistic interest rate and limit.</p>
    </div>
    """, unsafe_allow_html=True)

    col7, col8 = st.columns(2)
    with col7:
        cibil_opts = ["800+", "750–799", "700–749", "600–699", "Below 600", "I don't know"]
        cur_c = st.session_state.profile.get("cibil")
        c_idx = cibil_opts.index(cur_c) if cur_c in cibil_opts else None
        val_cibil = st.selectbox("What is your CIBIL score?", options=cibil_opts, index=c_idx, placeholder="Select one...", key=f"field_cibil_{fv}")

    with col8:
        cur_age = st.session_state.profile.get("age")
        val_age = st.number_input(
            "How old are you?",
            min_value=18,
            max_value=75,
            step=1,
            value=int(cur_age) if cur_age is not None else None,
            placeholder="e.g. 30",
            key=f"field_age_{fv}"
        )

    # STEP 4: ACCURACY BOOSTER (OPTIONAL QUESTIONS TAILORED FOR EMPLOYMENT TYPE)
    st.markdown("<hr style='border:0; border-top:1px solid var(--border); margin:1.5rem 0;'>", unsafe_allow_html=True)
    with st.expander("📋 Step 4: Got a minute to make your estimate more accurate?", expanded=False):
        if val_income_source:
            var_qs = get_variable_questions_for_category(val_income_source)
            st.markdown(
                f"<p style='color:var(--fg-muted); font-size:0.9rem; margin-bottom:1rem;'>"
                f"Answering these quick optional questions for <b>{val_income_source}</b> helps tighten your rate range from ±2.35% down to ±0.35%. "
                f"All questions are completely optional — answer as many or as few as you like!"
                f"</p>",
                unsafe_allow_html=True
            )

            def render_step4_field(q, fv):
                q_key = q["key"]
                field_k = f"field_{q_key}_{fv}"
                cur_v = st.session_state.profile.get(q_key)
                label = q["label"]
                help_text = q.get("why_we_ask", "")

                if q["input_type"] == "select":
                    opts = q["options"]
                    cur_str = str(cur_v) if cur_v is not None else None
                    if cur_str in ["True", "true"] and "Yes" in opts:
                        cur_str = "Yes"
                    elif cur_str in ["False", "false"] and "No" in opts:
                        cur_str = "No"
                    idx = None
                    if cur_str:
                        for opt_i, opt in enumerate(opts):
                            if opt.lower() == cur_str.lower() or opt.lower().startswith(cur_str.lower()):
                                idx = opt_i
                                break
                    st.selectbox(label, options=opts, index=idx, placeholder="Select one...", key=field_k, help=help_text)
                else:
                    min_v = q.get("min", 0)
                    max_v = q.get("max", 100000000)
                    step_v = q.get("step", 1)
                    is_float = isinstance(step_v, float) or isinstance(min_v, float)
                    if is_float:
                        num_val = float(cur_v) if (cur_v is not None and cur_v != "") else None
                        st.number_input(label, min_value=float(min_v), max_value=float(max_v), step=float(step_v), value=num_val, placeholder=f"e.g. {q.get('default', 0)}", key=field_k, help=help_text)
                    else:
                        num_val = int(cur_v) if (cur_v is not None and cur_v != "") else None
                        st.number_input(label, min_value=int(min_v), max_value=int(max_v), step=int(step_v), value=num_val, placeholder=f"e.g. {q.get('default', 0)}", key=field_k, help=help_text)

            # Render all 18 questions in an elegant 2-column grid
            for i in range(0, len(var_qs), 2):
                col_v1, col_v2 = st.columns(2)
                with col_v1:
                    render_step4_field(var_qs[i], fv)
                if i + 1 < len(var_qs):
                    with col_v2:
                        render_step4_field(var_qs[i + 1], fv)
        else:
            st.info("💡 Select your main source of income in Step 1 to unlock personalized questions here.")

    st.markdown("""
    <p style="margin-top: 1.4rem; padding-top: 1.2rem; border-top: 1px dashed var(--border); font-size: 0.9rem; color: var(--fg-muted);">
      Want a more accurate result? You can come back and refine your income, expenses and existing loans any time — a closer estimate just needs closer numbers.
    </p>
    """, unsafe_allow_html=True)

    # CTA BUTTONS
    st.markdown('<div class="cta-row">', unsafe_allow_html=True)
    c_btn_a, c_btn_b = st.columns([3, 1])
    with c_btn_a:
        calc_submitted = st.button("Check my borrowing capacity", type="primary", use_container_width=True, key=f"btn_calc_{fv}")
    with c_btn_b:
        reset_clicked = st.button("Start fresh", type="secondary", use_container_width=True, key=f"btn_reset_{fv}")
    st.markdown('<span class="cta-sub">Takes about two minutes · nothing is saved or sent anywhere</span></div>', unsafe_allow_html=True)

    if reset_clicked:
        apply_persona("clean")
        st.rerun()

    if calc_submitted:
        # Directly sync all widget values into profile to ensure modifications are 100% reflected
        if val_purpose is not None and val_purpose != "" and val_purpose != "Select one...":
            st.session_state.profile["loan_purpose"] = val_purpose
        if val_amount is not None and val_amount != "":
            st.session_state.profile["target_loan_amount"] = val_amount
        if val_tenure is not None and val_tenure != "":
            st.session_state.profile["tenure_months"] = val_tenure
        if val_income_source is not None and val_income_source != "" and val_income_source != "Select one...":
            st.session_state.profile["employment_type"] = val_income_source
        if val_income is not None and val_income != "":
            st.session_state.profile["net_income"] = val_income
        if val_existing_emi is not None:
            st.session_state.profile["existing_emi"] = val_existing_emi
        if val_rent is not None:
            st.session_state.profile["rent"] = val_rent
        if val_essential is not None and val_essential != "":
            st.session_state.profile["living_expenses"] = val_essential
        if val_cibil is not None and val_cibil != "" and val_cibil != "Select one...":
            st.session_state.profile["cibil"] = val_cibil
        if val_age is not None and val_age != "":
            st.session_state.profile["age"] = val_age

        # Also sync any Step 4 optional fields currently in session state
        for k in list(st.session_state.keys()):
            if k.startswith("field_") and k.endswith(f"_{fv}"):
                raw_k = k[len("field_"):-len(f"_{fv}")]
                if raw_k not in [
                    "loan_purpose", "target_loan_amount", "tenure_months", "employment_type",
                    "net_income", "existing_emi", "rent", "living_expenses", "cibil", "age"
                ]:
                    v = st.session_state[k]
                    if v is not None and v != "" and v != "Select one...":
                        st.session_state.profile[raw_k] = v
                    elif raw_k in st.session_state.profile and (v is None or v == "" or v == "Select one..."):
                        del st.session_state.profile[raw_k]

        mandatory_fields = [
            ("loan_purpose", "Loan purpose (Step 1)"),
            ("target_loan_amount", "Loan amount (Step 1)"),
            ("tenure_months", "Repayment period (Step 1)"),
            ("employment_type", "Source of income (Step 1)"),
            ("net_income", "Monthly income (Step 1)"),
            ("existing_emi", "Other loan payments (Step 2)"),
            ("rent", "Rent or housing payment (Step 2)"),
            ("living_expenses", "Essential expenses (Step 2)"),
            ("cibil", "CIBIL score (Step 3)"),
            ("age", "Age (Step 3)"),
        ]
        missing = [label for key, label in mandatory_fields if st.session_state.profile.get(key) is None or st.session_state.profile.get(key) == ""]
        if missing:
            st.warning(f"⚠️ Please answer all 10 basic questions in Steps 1 to 3 before calculating your borrowing limit. Still needed: {', '.join(missing)}")
        else:
            # Execute underwriting math with latest modified data
            math_profile = prep_math_profile(st.session_state.profile)
            results = run_full_underwriting(math_profile)
            explanations = generate_all_explanations(math_profile, results)
            card = build_negotiation_card(math_profile, results)

            st.session_state.calculated_data = {
                "results": results,
                "explanations": explanations,
                "card": card,
                "profile_snapshot": dict(math_profile),
                "label": f"Loan of ₹{st.session_state.profile['target_loan_amount']:,.0f} over {st.session_state.profile['tenure_months']} months"
            }
            st.session_state.has_calculated = True
            st.session_state.active_profile_label = "Custom Borrower Profile"
            trigger_redirect("results")
            st.rerun()

# -----------------------------------------------------------------------------
# PHOTO BLOCK 2: TABLET CONSULTATION
# -----------------------------------------------------------------------------
if img_tablet:
    st.markdown(f"""
    <div class="photo-block">
      <div class="photo-card">
        <img src="{img_tablet}" alt="A bank relationship manager reviews loan terms on a tablet with a couple across the table." />
      </div>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# RESULTS SECTION
# -----------------------------------------------------------------------------
st.markdown('<div id="results-section"></div>', unsafe_allow_html=True)

if not st.session_state.has_calculated or not st.session_state.get("calculated_data"):
    # Standby Pre-Results
    st.markdown("""
    <div class="section-head" style="text-align: center; padding: 2rem 0;">
      <h2>Your results will appear here</h2>
      <p style="margin: 0.5rem auto 0; font-size: 0.95rem;">
        Fill in your details above and select <b>Check my borrowing capacity</b> to see your recommendation,
        your safe limit, a fair interest rate, and a negotiation guide you can take into the meeting.
      </p>
    </div>
    """, unsafe_allow_html=True)

else:
    # CALCULATED OUTPUTS
    calc_data = st.session_state.calculated_data
    res = calc_data["results"]
    exp = calc_data["explanations"]
    card = calc_data["card"]
    user_p = st.session_state.profile

    amt_val = user_p.get("target_loan_amount", 500000)
    tenure_val = user_p.get("tenure_months", 48)

    active_lbl = st.session_state.get("active_profile_label", "")
    profile_badge = f'<span class="pill-note ok" style="margin-left: 0.6rem; vertical-align: middle; font-size: 0.8rem;">{active_lbl}</span>' if active_lbl and active_lbl != "Not started" else ""

    st.markdown(f"""
    <span class="section-label">Your borrowing results {profile_badge}</span>
    <h2 style="margin-bottom: 1.5rem;">Results for a ₹{amt_val:,.0f} loan over {tenure_val} months</h2>
    """, unsafe_allow_html=True)

    # 1. VERDICT BANNER
    verdict = res["verdict"]
    v_class = "borrow" if verdict == "BORROW" else ("no" if verdict == "DON'T BORROW" else "less")
    v_mark = "✓" if verdict == "BORROW" else ("✕" if verdict == "DON'T BORROW" else "△")
    v_title = "Borrow" if verdict == "BORROW" else ("Don't borrow" if verdict == "DON'T BORROW" else "Borrow less")
    v_reason = exp["verdict_why"]

    st.markdown(f"""
    <div class="verdict {v_class}">
      <span class="mark">{v_mark}</span>
      <div>
        <h2>{v_title}</h2>
        <p>{v_reason}</p>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # 2. 2x2 RESULTS GRID
    lender_amt = res["lender_max_principal"]
    safe_amt = res["borrower_safe_limit"]
    rate_min = res["rate_min"]
    rate_max = res["rate_max"]
    apr = res["all_in_apr"]
    safe_emi = res["monthly_safe_ceiling"]
    req_emi = res["requested_emi"]
    prod_type = res["target_product"]
    stress = res["stress_results"]
    passes_stress = stress["passes_stress"]

    stress_pill_cls = "ok" if passes_stress else "bad"
    stress_pill_txt = "✓ Still affordable if your income falls 20% and rates rise 2%" if passes_stress else "✕ Would be tight if your income falls 20% or rates rise 2%"

    # Build tenure schedule table rows safely with ZERO leading indentation
    schedule_rows = []
    for s in res["tenure_schedule"]:
        is_cur = (s["tenure_months"] == int(tenure_val))
        row_cls = ' class="current"' if is_cur else ""
        yours_tag = " (yours)" if is_cur else ""
        schedule_rows.append(
            f'<tr{row_cls}>'
            f'<td>{s["tenure_months"]} months{yours_tag}</td>'
            f'<td class="mono">₹{s["monthly_emi"]:,.0f}</td>'
            f'<td class="mono">₹{s["total_interest"]:,.0f}</td>'
            f'<td class="mono">₹{s["total_repaid"]:,.0f}</td>'
            f'</tr>'
        )
    schedule_html = "".join(schedule_rows)

    grid_html = f"""<div class="result-grid">
<!-- Card 1: How much can you borrow? -->
<div class="result-card">
  <h3>How much can you borrow?</h3>
  <div class="figure-row">
    <span class="label">A bank may offer up to</span>
    <span class="value">₹{lender_amt:,.0f}</span>
  </div>
  <div class="figure-row">
    <span class="label">You can safely afford</span>
    <span class="value big">₹{safe_amt:,.0f}</span>
  </div>
  <div class="callout">
    Use <b>₹{safe_amt:,.0f}</b> as your safe limit. Borrowing the full amount a bank offers can leave too little room for your regular expenses and emergencies.
  </div>
</div>

<!-- Card 2: A reasonable interest rate -->
<div class="result-card">
  <h3>A reasonable interest rate</h3>
  <div class="figure-row">
    <span class="label">Loan type</span>
    <span class="value" style="font-family:'Poppins',sans-serif; font-size:0.92rem; text-align:right;">{prod_type}</span>
  </div>
  <div class="figure-row">
    <span class="label">Reasonable rate range</span>
    <span class="value">{rate_min:.2f}% – {rate_max:.2f}%</span>
  </div>
  <div class="figure-row">
    <span class="label">Estimated yearly cost</span>
    <span class="value big">{apr:.2f}%</span>
  </div>
  <div class="callout">
    <b>Why:</b> {exp["rate_why"]}
  </div>
</div>

<!-- Card 3: Monthly payment you can afford -->
<div class="result-card">
  <h3>Monthly payment you can afford</h3>
  <div class="figure-row">
    <span class="label">Safe monthly payment</span>
    <span class="value big">₹{safe_emi:,.0f}</span>
  </div>
  <div class="figure-row">
    <span class="label">Payment for your requested loan</span>
    <span class="value">₹{req_emi:,.0f} / month</span>
  </div>
  <span class="pill-note {stress_pill_cls}">{stress_pill_txt}</span>
  <div class="callout">
    <b>What we checked:</b> whether you could keep paying if your available income dropped by a fifth and the interest rate rose by 2 percentage points, on top of your existing loan payments.
  </div>
</div>

<!-- Card 4: Tenure schedule -->
<div class="result-card">
  <h3>See how the loan period changes things</h3>
  <p style="font-size:0.85rem; color:var(--fg-muted); margin-bottom:0.5rem;">
    For the amount you asked for (₹{amt_val:,.0f}), at your estimated rate.
  </p>
  <div class="compare-wrap">
    <table class="compare">
      <thead>
        <tr>
          <th>Tenure</th>
          <th class="mono">Monthly payment</th>
          <th class="mono">Total interest</th>
          <th class="mono">Total repaid</th>
        </tr>
      </thead>
      <tbody>
        {schedule_html}
      </tbody>
    </table>
  </div>
</div>
</div>"""

    st.markdown(grid_html, unsafe_allow_html=True)

    # 3. NEGOTIATION GUIDE
    reasons_html = "".join([f"<li>{r}</li>" for r in card["leverage_points"]])
    st.markdown(f"""
    <div class="negotiation">
      <span class="section-label">Loan negotiation guide</span>
      <h3>What to ask the lender for</h3>
      <div class="neg-grid">
        <div class="neg-block">
          <h4>Your targets</h4>
          <ul>
            <li>Loan type: <b>{prod_type}</b></li>
            <li>Reasonable interest rate: <b>{rate_min:.2f}% – {rate_max:.2f}%</b></li>
            <li>Highest yearly cost: <b>{apr:.2f}%</b></li>
            <li>Maximum monthly payment: <b>₹{safe_emi:,.0f}</b></li>
          </ul>
        </div>
        <div class="neg-block">
          <h4>Why you can ask for better terms</h4>
          <ul>{reasons_html}</ul>
        </div>
      </div>
      <div class="neg-block" style="margin-top: 1.3rem;">
        <h4>Before you accept</h4>
        <ul>
          <li>Ask about every fee added to the loan, including processing fees above 1% plus tax.</li>
          <li>Don't accept insurance or other add-ons unless you understand and want them.</li>
          <li>Ask whether there's a charge for repaying the loan early.</li>
          <li>Ask for the total amount you'll repay before you accept the loan.</li>
        </ul>
      </div>
      <div class="script-box">
        "{card['spoken_script']}"
      </div>
    </div>
    """, unsafe_allow_html=True)

    # 4. DEDICATED NO-BORROW CARD IF VERDICT IS DON'T BORROW
    if verdict == "DON'T BORROW":
        st.markdown("""
        <div class="no-borrow-card">
          <h3>Why we're saying don't borrow right now</h3>
          <p>
            Your current loan payments and monthly expenses leave very little room for another loan.
            Taking one on now could make your existing commitments harder to manage.
          </p>
          <p style="margin-top: 0.9rem;">
            <b>Your safe borrowing limit: ₹0</b>
          </p>
          <p style="margin-top: 1rem; font-weight: 500;">What to do first</p>
          <ol>
            <li>Clear any overdue payments.</li>
            <li>Reduce your existing debt where you can.</li>
            <li>Keep your monthly expenses under control.</li>
            <li>Build a small emergency fund before you borrow again.</li>
          </ol>
        </div>
        """, unsafe_allow_html=True)

    # 5. HONESTY ABOUT LIMITS (DISCLOSING WHERE THE APP GUESSES)
    cibil_input = user_p.get("cibil", "I don't know")
    is_unknown_cibil = ("don't know" in str(cibil_input).lower() or str(cibil_input).strip() == "")
    cibil_guess_txt = (
        "You marked your credit score as unknown. We estimated an unrated retail band (±2.0% spread) rather than penalizing you as a defaulter."
        if is_unknown_cibil else
        f"Credit score ({cibil_input}) is self-reported and unverified by a bureau API pull."
    )

    st.markdown(f"""
    <div class="callout" style="margin-top: 1.5rem; background: var(--bg-soft); border-left: 3px solid var(--fg-muted);">
      <b>🔍 Honesty about limits — Where this tool is guessing vs. calculating:</b>
      <ul style="margin: 0.5rem 0 0 1.2rem; padding: 0; font-size: 0.88rem; color: var(--fg-muted); line-height: 1.55;">
        <li><b>Exact Math:</b> Loan EMI, total interest, and all-in APR (with 18% GST fee drag) are calculated with exact rupee formulas.</li>
        <li><b>Living expenses guess:</b> Assumed constant based on your self-reported entries; unforeseen medical costs or future inflation over {tenure_val} months are not predicted.</li>
        <li><b>Credit profile estimation:</b> {cibil_guess_txt}</li>
        <li><b>Bank fee assumption:</b> We assume a standard 1.0%–1.5% bank processing fee plus 18% GST. Verify your lender's sanction letter for exact charges.</li>
        <li><b>Confidence ceiling:</b> Capped at 95% because self-reported entries have not undergone bank statement audit or physical title deed search.</li>
      </ul>
    </div>
    """, unsafe_allow_html=True)

    # Action Buttons
    c_btn1, c_btn2 = st.columns([1, 1])
    with c_btn1:
        if st.button("Edit my answers", key="btn_edit_answers", use_container_width=True):
            trigger_redirect("form")
            st.rerun()
    with c_btn2:
        if st.button("Start fresh", key="btn_start_fresh", use_container_width=True):
            apply_persona("clean")
            st.rerun()

# -----------------------------------------------------------------------------
# BENCHMARK BORROWERS TEST SECTION
# -----------------------------------------------------------------------------
st.markdown("<hr style='border:0; border-top:1px solid var(--border); margin:2.5rem 0 1.5rem;'>", unsafe_allow_html=True)
with st.expander("🧪 Try a sample borrower profile (Priya, Ravi, Anita)", expanded=True):
    st.markdown(
        "<p style='color:var(--fg-muted); font-size:0.9rem; margin-bottom:1rem;'>"
        "Click any borrower profile below to load their numbers and see their instant underwriting results:"
        "</p>",
        unsafe_allow_html=True
    )
    b1, b2, b3 = st.columns(3)
    with b1:
        st.markdown("""
        <div class="persona-card">
          <b>👤 Priya, 29</b>
          <span class="meta">Bengaluru · Salaried MNC</span>
          <p>₹1.1L/mo salary, ₹14k car loan EMI, CIBIL 780, rents at ₹28k. Wants ₹8L personal loan for a wedding.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Load Priya's Profile", key="btn_load_priya", use_container_width=True):
            apply_persona("priya")
            st.rerun()

    with b2:
        st.markdown("""
        <div class="persona-card">
          <b>🏪 Ravi, 42</b>
          <span class="meta">Mysuru · Kirana Store</span>
          <p>₹85k cash income, owns unencumbered shop premises (₹45L), unscored CIBIL. Wants ₹15L business expansion.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Load Ravi's Profile", key="btn_load_ravi", use_container_width=True):
            apply_persona("ravi")
            st.rerun()

    with b3:
        st.markdown("""
        <div class="persona-card">
          <b>🛵 Anita, 35</b>
          <span class="meta">Hubballi · Delivery Partner</span>
          <p>₹28k/mo, 1 EMI bounce, 3 app loans totaling ₹35k at 36% APR. Wants ₹1.5L for electric scooter.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Load Anita's Profile", key="btn_load_anita", use_container_width=True):
            apply_persona("anita")
            st.rerun()

# -----------------------------------------------------------------------------
# FOOTER
# -----------------------------------------------------------------------------
st.markdown("""
<footer>
  <div class="foot-row">
    <div class="brandmark"><span class="dot"></span>Borrower Copilot</div>
    <span class="mono" style="font-size: 0.82rem; color: var(--fg-faint);">Loan borrowing guide</span>
  </div>
  <p class="fine">
    This tool gives an estimate based only on what you enter. It doesn't guarantee loan approval,
    a loan amount or an interest rate from any bank or lender — actual terms vary because each
    lender applies its own rules and checks.
  </p>
  <p class="fine">
    This is a general educational estimate, not personal financial advice. For a decision specific
    to your situation, speak with your bank or a licensed financial advisor.
  </p>
</footer>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# RELIABLE AUTO-SCROLL REDIRECT DISPATCHER
# -----------------------------------------------------------------------------
curr_scroll_trigger = st.session_state.get("scroll_trigger", 0)
last_scroll_trigger = st.session_state.get("last_executed_scroll_trigger", -1)

if curr_scroll_trigger != last_scroll_trigger and st.session_state.get("scroll_to"):
    st.session_state.last_executed_scroll_trigger = curr_scroll_trigger
    target_dest = st.session_state.scroll_to
    target_selector = "results-section" if target_dest == "results" else "form-section"
    unique_nonce = f"{curr_scroll_trigger}_{int(time.time() * 1000)}"

    components.html(f"""
    <!-- Dispatcher Trigger #{curr_scroll_trigger} target={target_selector} nonce={unique_nonce} -->
    <script>
    (function() {{
      var targetId = '{target_selector}';
      var attempts = 0;
      var maxAttempts = 30;

      function tryScroll() {{
        try {{
          var pDoc = window.parent.document;
          var pWin = window.parent;
          if (!pDoc) return false;

          var target = null;
          if (targetId === 'results-section') {{
            target = pDoc.getElementById('results-section') ||
                     pDoc.querySelector('.verdict') ||
                     pDoc.querySelector('.result-grid') ||
                     pDoc.querySelector('.section-label');
          }} else {{
            target = pDoc.getElementById('form-section') ||
                     pDoc.querySelector('.step') ||
                     pDoc.querySelector('div[data-testid="stContainer"]');
          }}

          if (target) {{
            // 1. Native smooth scrollIntoView
            target.scrollIntoView({{ behavior: 'smooth', block: 'start' }});

            // 2. Scroll main container
            var main = pDoc.querySelector('section[data-testid="stMain"]') ||
                       pDoc.querySelector('.main') ||
                       pDoc.querySelector('div[data-testid="stAppViewContainer"]');

            if (main) {{
              var targetRect = target.getBoundingClientRect();
              var mainRect = main.getBoundingClientRect();
              var offset = targetRect.top - mainRect.top;
              main.scrollBy({{ top: offset - 95, behavior: 'smooth' }});
            }}

            // 3. Fallback window scroll
            if (pWin && pWin.scrollBy) {{
              var tTop = target.getBoundingClientRect().top;
              pWin.scrollBy({{ top: tTop - 95, behavior: 'smooth' }});
            }}
            return true;
          }}
        }} catch (e) {{
          console.error('Auto-scroll error:', e);
        }}
        return false;
      }}

      // Execute on immediate tick and staggered intervals
      tryScroll();
      var timer = setInterval(function() {{
        attempts++;
        if (tryScroll() || attempts >= maxAttempts) {{
          clearInterval(timer);
        }}
      }}, 40);

      setTimeout(tryScroll, 80);
      setTimeout(tryScroll, 180);
      setTimeout(tryScroll, 350);
      setTimeout(tryScroll, 600);
      setTimeout(tryScroll, 1000);
    }})();
    </script>
    """, height=0, width=0)
