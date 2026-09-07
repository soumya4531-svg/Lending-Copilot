"""
Borrower Copilot (app.py)
Pre-Lender Underwriting Self-Assessment for Indian Retail Borrowers.
Lokta Design System: Imperial Plum (#4B2440), Warm Canvas (#FBF9FA), Poppins & JetBrains Mono.
Zero-Database, Zero-API, Pure Deterministic Client Architecture.
"""

import streamlit as st
import streamlit.components.v1 as components
from engine.underwriting import run_full_underwriting, calculate_pmt
from engine.confidence import (
    compute_confidence_score,
    get_spread_half_width,
    get_questions_for_category,
    MASTER_QUESTIONS,
)
from engine.explanations import generate_all_explanations
from engine.negotiation import build_negotiation_card

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION & LOKTA STYLING
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Borrower Copilot | Lokta",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Robust Lokta CSS ensuring crisp contrast in both light and dark browser modes
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,400;0,500;0,600;0,700;1,400&family=JetBrains+Mono:wght@400;500;600&family=Newsreader:ital,opsz,wght@0,6..72,500;1,6..72,500&display=swap');

/* Force canvas & root background */
html, body, .stApp, div[data-testid="stAppViewContainer"], div[data-testid="stHeader"] {
  font-family: 'Poppins', -apple-system, BlinkMacSystemFont, sans-serif !important;
  background-color: #FBF9FA !important;
  color: #221A20 !important;
}

/* Sidebar styling */
div[data-testid="stSidebar"] {
  background-color: #F3EEF1 !important;
  border-right: 1px solid #E2D9DE !important;
}

/* Base text elements */
p, span, label, div, h1, h2, h3, h4, h5, h6, th, td {
  color: #221A20;
}

h1, h2, h3, h4 {
  font-family: 'Poppins', sans-serif !important;
  font-weight: 600 !important;
  color: #4B2440 !important;
  letter-spacing: -0.02em !important;
}

.mono-font {
  font-family: 'JetBrains Mono', monospace !important;
  font-variant-numeric: tabular-nums !important;
}

/* Form input widgets */
div[data-baseweb="input"], div[data-baseweb="select"] {
  background-color: #FFFFFF !important;
  border: 1px solid #E2D9DE !important;
  border-radius: 6px !important;
}

div[data-baseweb="input"] input, div[data-baseweb="select"] div {
  color: #221A20 !important;
  background-color: #FFFFFF !important;
}

/* Lokta Pill Badge */
.lokta-pill {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 600;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  background-color: #EFE3EA;
  color: #4B2440;
  border: 1px solid #E2D9DE;
}

/* Sticky Questionnaire Accuracy Dock */
div[data-testid="element-container"]:has(.sticky-accuracy-dock),
div[data-testid="stMarkdownContainer"]:has(.sticky-accuracy-dock) {
  display: contents !important;
}

.sticky-accuracy-dock {
  position: -webkit-sticky;
  position: sticky;
  top: 3.5rem;
  z-index: 999;
  background: rgba(251, 249, 250, 0.96) !important;
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid #E2D9DE;
  border-radius: 10px;
  padding: 0.75rem 1rem 0.65rem;
  margin-bottom: 1.2rem;
  box-shadow: 0 4px 14px rgba(75, 36, 64, 0.08);
}

div[data-testid="column"] {
  overflow: visible !important;
}

/* Standby Empty State Card */
.standby-card {
  background-color: #FFFFFF;
  border: 2px dashed #D3C4CD;
  border-radius: 12px;
  padding: 2.5rem 1.8rem;
  text-align: center;
  margin-top: 1rem;
}

/* Two-Fold Output Card */
.output-card {
  background-color: #F3EEF1;
  border: 1px solid #E2D9DE;
  border-left: 4px solid #4B2440;
  border-radius: 8px;
  padding: 1.25rem 1.4rem;
  margin-bottom: 1.2rem;
  box-shadow: 0 1px 3px rgba(34, 26, 32, 0.04);
}

.output-card-danger {
  border-left-color: #8C1D24;
  background-color: #FDF2F2;
}

.output-card-success {
  border-left-color: #1B5E3F;
  background-color: #F0F9F4;
}

.output-card-warn {
  border-left-color: #8A4B12;
  background-color: #FEF9F3;
}

.fold-1-metric {
  font-family: 'JetBrains Mono', monospace;
  font-size: 1.55rem;
  font-weight: 600;
  color: #221A20;
  line-height: 1.2;
  margin: 0.3rem 0;
}

.fold-2-why {
  font-size: 0.88rem;
  color: #4A3E47;
  line-height: 1.5;
  margin-top: 0.6rem;
  padding-top: 0.6rem;
  border-top: 1px solid #E2D9DE;
  font-style: normal;
}

.which-to-use-badge {
  display: inline-block;
  font-weight: 600;
  font-size: 0.85rem;
  padding: 0.3rem 0.75rem;
  border-radius: 4px;
  background-color: #4B2440;
  color: #FBF9FA;
  margin-top: 0.4rem;
}

/* Mobile Negotiation Card (Stays in high-contrast dark terminal theme) */
.negotiation-terminal {
  background-color: #17121A !important;
  color: #EEE6EA !important;
  border: 1px solid #33293A;
  border-radius: 10px;
  padding: 1.5rem;
  margin-top: 1.5rem;
  box-shadow: 0 4px 16px rgba(23, 18, 26, 0.15);
}

.negotiation-terminal * {
  color: #EEE6EA !important;
}

.terminal-header {
  border-bottom: 1px solid #33293A;
  padding-bottom: 0.75rem;
  margin-bottom: 1.25rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.terminal-title {
  font-size: 0.85rem;
  font-family: 'JetBrains Mono', monospace !important;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: #CFA5C1 !important;
  font-weight: 600;
}

.terminal-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background-color: #4EBA88;
  display: inline-block;
  margin-right: 6px;
}

.script-box {
  background-color: #2A1F2C !important;
  border-left: 3px solid #CFA5C1;
  padding: 1rem 1.25rem;
  border-radius: 4px;
  font-size: 0.95rem;
  line-height: 1.6;
  color: #FFFFFF !important;
  margin: 1rem 0;
  font-style: italic;
}

.script-box * {
  color: #FFFFFF !important;
}

/* Info Tooltip Box */
.info-desc-box {
  background-color: #EFE3EA;
  border-left: 3px solid #4B2440;
  padding: 0.45rem 0.75rem;
  border-radius: 4px;
  font-size: 0.8rem;
  color: #4B2440 !important;
  margin-bottom: 0.75rem;
  line-height: 1.4;
}

.info-desc-box * {
  color: #4B2440 !important;
}

/* Buttons */
.stButton button {
  border-radius: 9999px !important;
  font-weight: 500 !important;
  transition: all 0.2s ease-in-out !important;
}

/* Primary Button (Calculate My Borrowing Assessment) - Force Pure Crisp White Text */
button[kind="primary"],
button[kind="primary"] *,
button[kind="primary"] p,
button[kind="primary"] span,
button[kind="primary"] div,
div[data-testid="stBaseButton-primary"] button,
div[data-testid="stBaseButton-primary"] button * {
  color: #FFFFFF !important;
  fill: #FFFFFF !important;
}

button[kind="primary"],
div[data-testid="stBaseButton-primary"] button {
  background-color: #4B2440 !important;
  border: 1px solid #381B30 !important;
  border-radius: 9999px !important;
  font-weight: 600 !important;
  letter-spacing: 0.02em !important;
  box-shadow: 0 4px 14px rgba(75, 36, 64, 0.25) !important;
}

button[kind="primary"]:hover,
div[data-testid="stBaseButton-primary"] button:hover {
  background-color: #381B30 !important;
  border-color: #241120 !important;
  box-shadow: 0 6px 18px rgba(75, 36, 64, 0.35) !important;
}

button[kind="primary"]:hover *,
div[data-testid="stBaseButton-primary"] button:hover * {
  color: #FFFFFF !important;
}


/* Clean Expander */
div[data-testid="stExpander"] {
  background-color: #FFFFFF !important;
  border: 1px solid #E2D9DE !important;
  border-radius: 8px !important;
}
div[data-testid="stExpander"] summary {
  color: #4B2440 !important;
  font-weight: 600 !important;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# PRESET PERSONAS
# -----------------------------------------------------------------------------
PERSONAS = {
    "priya": {
        "name": "Priya (Salaried MNC Professional)",
        "desc": "29 yrs, Bengaluru. Software engineer at Tier-1 MNC. Net ₹1,10,000/mo. Car loan ₹14k/mo. CIBIL 780. Wants ₹8L personal loan for a wedding.",
        "data": {
            "loan_purpose": "Wedding",
            "target_loan_amount": 800000,
            "tenure_months": 48,
            "employment_type": "Salaried",
            "net_income": 110000,
            "existing_emi": 14000,
            "rent": 28000,
            "living_expenses": 25000,
            "cibil": "750+",
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
        "name": "Ravi (Kirana Store Owner / MSME)",
        "desc": "42 yrs, Mysuru. Kirana owner for 14 yrs. Cash income ₹85k/mo, ITR ₹4.2L/yr. Owns ₹45L unencumbered shop premises. Unscored. Wife earns ₹18k teaching. Wants ₹15L for stock/vehicle.",
        "data": {
            "loan_purpose": "Business Expansion",
            "target_loan_amount": 1500000,
            "tenure_months": 84,
            "employment_type": "Self-Employed / MSME",
            "net_income": 85000,
            "existing_emi": 0,
            "rent": 0,
            "living_expenses": 28000,
            "cibil": "Unknown / Unscored",
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
        "name": "Anita (Informal Delivery Partner)",
        "desc": "35 yrs, Hubballi. Delivery fleet rider & tailoring. Net ₹28k/mo, 2 kids, husband unemployed. 3 app loans totaling ₹35k at 36% APR. 1 bounce last month. Wants ₹1.5L for electric scooter.",
        "data": {
            "loan_purpose": "Vehicle Purchase",
            "target_loan_amount": 150000,
            "tenure_months": 24,
            "employment_type": "Informal / Gig Economy",
            "net_income": 28000,
            "existing_emi": 1500,
            "rent": 5000,
            "living_expenses": 18000,
            "cibil": "Below 700",
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
# SESSION STATE INITIALIZATION: STARTS COMPLETELY UNFILLED
# -----------------------------------------------------------------------------
NEUTRAL_EMPTY_PROFILE = {}

if "profile" not in st.session_state:
    st.session_state.profile = {}
    st.session_state.active_profile_label = "Unfilled Self-Assessment"
    st.session_state.has_calculated = False

if "just_calculated" not in st.session_state:
    st.session_state.just_calculated = False

if "scroll_trigger_count" not in st.session_state:
    st.session_state.scroll_trigger_count = 0

if "calculated_data" not in st.session_state:
    st.session_state.calculated_data = None

if "show_info_keys" not in st.session_state:
    st.session_state.show_info_keys = {}

if "form_version" not in st.session_state:
    st.session_state.form_version = 0

def prep_math_profile(raw_profile: dict) -> dict:
    """Prepares and normalizes raw profile inputs for underwriting mathematical calculations."""
    math_profile = {k: v for k, v in raw_profile.items() if v is not None and v != "" and v != "Please select..."}
    if math_profile.get("has_unencumbered_property") == "Yes":
        math_profile["has_unencumbered_property"] = True
    if math_profile.get("seasonal_variance_high") == "Yes (Monsoon Drop)":
        math_profile["seasonal_variance_high"] = True
    if math_profile.get("is_ev_vehicle") == "Yes (Replaces Petrol Scooter)":
        math_profile["is_ev_vehicle"] = True
    return math_profile

def apply_persona(persona_key: str):
    """Loads a persona and sets widget values & calculated results immediately."""
    # Increment form_version so that all widget keys refresh cleanly and completely
    st.session_state.form_version = st.session_state.get("form_version", 0) + 1
    fv = st.session_state.form_version

    # Clean up old widget keys from session_state
    for k in list(st.session_state.keys()):
        if k.startswith("field_"):
            del st.session_state[k]

    if persona_key in PERSONAS:
        data = dict(PERSONAS[persona_key]["data"])
        st.session_state.profile = dict(data)
        st.session_state.active_profile_label = PERSONAS[persona_key]["name"]
        st.session_state["current_active_category"] = data.get("employment_type")
        
        # Populate widget keys so inputs immediately reflect persona values
        for k, v in data.items():
            st.session_state[f"field_{k}_{fv}"] = v

        # Calculate results immediately for the benchmark persona
        math_profile = prep_math_profile(data)
        results = run_full_underwriting(math_profile)
        explanations = generate_all_explanations(math_profile, results)
        card = build_negotiation_card(math_profile, results)
        st.session_state.calculated_data = {
            "results": results,
            "explanations": explanations,
            "card": card,
            "profile_snapshot": dict(math_profile),
            "label": PERSONAS[persona_key]["name"]
        }
        st.session_state.has_calculated = True
        st.session_state.just_calculated = True
        st.session_state.scroll_trigger_count = st.session_state.get("scroll_trigger_count", 0) + 1
    else:
        # Reset to neutral unfilled form
        st.session_state.profile = {}
        st.session_state.active_profile_label = "Unfilled Self-Assessment"
        st.session_state.has_calculated = False
        st.session_state.just_calculated = False
        st.session_state.calculated_data = None
        st.session_state["current_active_category"] = None
        st.session_state.show_info_keys = {}

def sync_active_profile_from_widgets():
    """Captures all currently entered values directly from Streamlit widget state."""
    fv = st.session_state.get("form_version", 0)
    for k in MASTER_QUESTIONS.keys():
        w_key = f"field_{k}_{fv}"
        if w_key in st.session_state:
            val = st.session_state[w_key]
            if val is not None and val != "" and val != "Please select...":
                st.session_state.profile[k] = val
            elif k in st.session_state.profile and (val is None or val == "" or val == "Please select..."):
                del st.session_state.profile[k]

# Sync widgets to profile at the start of execution
sync_active_profile_from_widgets()

# Detect dynamic category change
fv = st.session_state.get("form_version", 0)
new_detected_category = st.session_state.profile.get("employment_type") or st.session_state.get(f"field_employment_type_{fv}")
prev_tracked_category = st.session_state.get("current_active_category")

if new_detected_category and prev_tracked_category and new_detected_category != prev_tracked_category:
    # User switched employment structure! Clear previous category's variable inputs only
    for q_k, q_v in MASTER_QUESTIONS.items():
        if q_v.get("tier") == "Variable":
            st.session_state.profile.pop(q_k, None)
            st.session_state.pop(f"field_{q_k}_{fv}", None)

if new_detected_category:
    st.session_state["current_active_category"] = new_detected_category



# -----------------------------------------------------------------------------
# HEADER & HERO
# -----------------------------------------------------------------------------
col_header_left, col_header_right = st.columns([3, 1])

with col_header_left:
    st.markdown("<h1 style='margin-top:0.4rem; margin-bottom:0.2rem;'>Borrower <em>Copilot</em></h1>", unsafe_allow_html=True)
    st.markdown(
        "<p style='color:#6E6069; font-size:1.02rem; max-width:44rem; margin-bottom:1.1rem;'>"
        "Before you walk into a lender, answer four questions with deterministic institutional math: "
        "<b>Should I borrow? How much am I eligible for? What is a fair rate? What EMI is safe?</b> "
        "Then hand them a one-page Negotiation Card."
        "</p>",
        unsafe_allow_html=True
    )

with col_header_right:
    st.markdown(
        "<div style='background:#F3EEF1; padding:0.9rem; border-radius:8px; border:1px solid #E2D9DE; font-size:0.82rem;'>"
        "<b>Zero-Bureau Pull</b><br>"
        "<span style='color:#6E6069;'>Runs 100% locally from your self-reported inputs. No logins or stored data.</span>"
        "</div>",
        unsafe_allow_html=True
    )

# -----------------------------------------------------------------------------
# TOP ACTION & STATUS BAR
# -----------------------------------------------------------------------------
top_status_col, top_btn_col = st.columns([3, 1])

with top_status_col:
    if st.session_state.has_calculated:
        st.markdown(
            f"<div style='margin-top:0.25rem; font-size:0.84rem; color:#1B5E3F; background:#F0F9F4; border:1px solid #D1E7DD; padding:0.45rem 0.85rem; border-radius:6px; display:inline-block; font-weight:500;'>"
            f"🟢 Active Assessment: <b>{st.session_state.active_profile_label}</b> · Calculated & Live"
            f"</div>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"<div style='margin-top:0.25rem; font-size:0.84rem; color:#8A4B12; background:#FEF9F3; border:1px solid #FCE5D2; padding:0.45rem 0.85rem; border-radius:6px; display:inline-block; font-weight:500;'>"
            f"⚪ Status: <b>Neutral / Unfilled Form</b> · Enter your details on the left, then click 'Calculate My Borrowing Assessment' below."
            f"</div>",
            unsafe_allow_html=True
        )

with top_btn_col:
    if st.button("🔄 Start Fresh", use_container_width=True, help="Reset to an unfilled neutral form"):
        apply_persona("clean")
        st.rerun()

st.markdown("<hr style='border:0; border-top:1px solid #E2D9DE; margin:1.2rem 0;'>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# MAIN LAYOUT: LEFT (ADAPTIVE QUESTION WIZARD) | RIGHT (RESULTS DASHBOARD)
# -----------------------------------------------------------------------------
col_inputs, col_outputs = st.columns([5, 6], gap="large")

# =============================================================================
# LEFT COLUMN: ADAPTIVE QUESTIONNAIRE WIZARD
# =============================================================================
def on_employment_type_change():
    """Immediately synchronizes category switch and purges stale variable answers from previous sector."""
    fv = st.session_state.get("form_version", 0)
    new_cat = st.session_state.get(f"field_employment_type_{fv}")
    if new_cat and new_cat != "Please select...":
        st.session_state.profile["employment_type"] = new_cat
    elif "employment_type" in st.session_state.profile:
        del st.session_state.profile["employment_type"]
    
    # Purge stale variable questions from previous track, keeping all 10 mandatory fields intact
    for q_k, q_v in MASTER_QUESTIONS.items():
        if q_v.get("tier") == "Variable":
            st.session_state.profile.pop(q_k, None)
            st.session_state.pop(f"field_{q_k}_{fv}", None)
            
    st.session_state["current_active_category"] = new_cat

with col_inputs:
    # 1. Live Confidence Progression Bar
    fv = st.session_state.get("form_version", 0)
    curr_category = st.session_state.profile.get("employment_type") or st.session_state.get(f"field_employment_type_{fv}")
    conf_score = compute_confidence_score(st.session_state.profile, curr_category or "")
    spread_width = get_spread_half_width(conf_score)

    # Determine badge color, text, and description based on confidence score
    if conf_score < 60.0:
        badge_bg = "#FEF9F3"
        badge_color = "#8A4B12"
        badge_border = "#FCE5D2"
        badge_text = "⚡ Incomplete"
        status_desc = "Answer the mandatory questions below to reach baseline 60% confidence."
    elif conf_score < 70.0:
        badge_bg = "#F3EEF1"
        badge_color = "#4B2440"
        badge_border = "#E2D9DE"
        badge_text = f"±{spread_width:.2f}% spread"
        status_desc = f"Base Assessment (60% Confidence) · Uncertainty spread: ±{spread_width:.2f}%. Answer optional questions below to tighten bands to 95%."
    else:
        badge_bg = "#F0F9F4"
        badge_color = "#1B5E3F"
        badge_border = "#D1E7DD"
        badge_text = f"🎯 ±{spread_width:.2f}% Calibrated"
        status_desc = f"Calibrated Profile ({conf_score:.1f}% Confidence) · Uncertainty spread tightened to ±{spread_width:.2f}%."

    st.markdown(f"""
    <div class="sticky-accuracy-dock">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.35rem;">
        <div style="font-size: 0.95rem; font-weight: 700; color: #4B2440; letter-spacing: -0.01em;">
          🎯 Assessment Accuracy: <span style="font-family: 'JetBrains Mono', monospace; font-size: 1.05rem;">{conf_score:.1f}%</span>
        </div>
        <div style="font-size: 0.74rem; font-weight: 600; padding: 0.2rem 0.6rem; border-radius: 9999px; background: {badge_bg}; color: {badge_color}; border: 1px solid {badge_border};">
          {badge_text}
        </div>
      </div>
      <div style="width: 100%; height: 7px; background-color: #E2D9DE; border-radius: 9999px; overflow: hidden; margin-bottom: 0.35rem;">
        <div style="width: {conf_score}%; height: 100%; background: linear-gradient(90deg, #8A4B12, #4B2440); border-radius: 9999px; transition: width 0.3s ease;"></div>
      </div>
      <div style="font-size: 0.76rem; color: #6E6069; line-height: 1.35;">
        {status_desc}
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Dynamic pinning script for Option A sticky dock
    components.html(
        """
        <script>
        (function() {
          try {
            const doc = window.parent.document;
            const mainScroll = doc.querySelector('section.stMain') || doc.querySelector('div[data-testid="stAppViewContainer"]') || window.parent;
            
            function updateSticky() {
              try {
                const dock = doc.querySelector('.sticky-accuracy-dock');
                if (!dock) return;
                const col = dock.closest('div[data-testid="stColumn"]') || dock.closest('div[data-testid="column"]');
                if (!col) return;

                let spacer = doc.getElementById('sticky-dock-spacer');
                if (!spacer) {
                  spacer = doc.createElement('div');
                  spacer.id = 'sticky-dock-spacer';
                  spacer.style.display = 'none';
                  dock.parentNode.insertBefore(spacer, dock);
                }

                const colRect = col.getBoundingClientRect();
                if (colRect.top < 60) {
                  spacer.style.display = 'block';
                  spacer.style.height = dock.offsetHeight + 'px';
                  spacer.style.marginBottom = '1.2rem';
                  dock.style.position = 'fixed';
                  dock.style.top = '58px';
                  dock.style.left = colRect.left + 'px';
                  dock.style.width = colRect.width + 'px';
                  dock.style.zIndex = '9999';
                } else {
                  spacer.style.display = 'none';
                  dock.style.position = 'relative';
                  dock.style.top = '0px';
                  dock.style.left = '0px';
                  dock.style.width = '100%';
                  dock.style.zIndex = '1';
                }
              } catch(e) {
                console.error('Sticky update error:', e);
              }
            }

            // Attach capture-phase listener to guarantee capturing scroll on any container
            window.parent.removeEventListener('scroll', updateSticky, true);
            window.parent.addEventListener('scroll', updateSticky, true);
            window.parent.addEventListener('resize', updateSticky, true);
            doc.addEventListener('scroll', updateSticky, true);

            updateSticky();
            setTimeout(updateSticky, 50);
            setTimeout(updateSticky, 150);
            setTimeout(updateSticky, 400);
          } catch(err) {
            console.error('Sticky dock init error:', err);
          }
        })();
        </script>
        """,
        height=0,
        width=0
    )

    # 2. Field Renderer with Strict Type Normalization & Info Toggle
    def render_field(key: str, q_def: dict):
        label = q_def["label"]
        q_id = q_def["id"]
        why_text = q_def.get("why_we_ask", "")
        input_type = q_def["input_type"]
        fv = st.session_state.get("form_version", 0)
        w_key = f"field_{key}_{fv}"
        
        # Read from session_state widget key first, then fallback to profile
        val = st.session_state.get(w_key, st.session_state.profile.get(key, None))

        # Label + Info Button Row
        c_lbl, c_btn = st.columns([5, 1])
        with c_lbl:
            st.markdown(f"**{q_id}. {label}**")
        with c_btn:
            btn_key = f"info_btn_{key}_{fv}"
            if st.button("ℹ️", key=btn_key, help="Click to see why we ask this question"):
                st.session_state.show_info_keys[key] = not st.session_state.show_info_keys.get(key, False)

        # Render information description box if toggled
        if st.session_state.show_info_keys.get(key, False):
            st.markdown(f'<div class="info-desc-box">💡 <b>Why we ask this:</b> {why_text}</div>', unsafe_allow_html=True)

        has_widget_state = w_key in st.session_state

        # Number input with strict type matching & placeholder
        if input_type == "number":
            is_float_field = (
                isinstance(q_def.get("step"), float) or
                isinstance(q_def.get("min"), float) or
                isinstance(q_def.get("default"), float) or
                (isinstance(val, float) and not float(val).is_integer())
            )

            placeholder_txt = f"e.g. {q_def.get('default', '')}"

            if is_float_field:
                step_val = float(q_def.get("step", 1.0))
                min_val = float(q_def.get("min", 0.0))
                max_val = float(q_def["max"]) if "max" in q_def else None
                
                num_kwargs = {
                    "label": f"Input {q_id}",
                    "min_value": min_val,
                    "max_value": max_val,
                    "step": step_val,
                    "format": "%.2f" if step_val < 1.0 else "%.1f",
                    "placeholder": placeholder_txt,
                    "label_visibility": "collapsed",
                    "key": w_key
                }
                if not has_widget_state:
                    cur_val = None
                    if val is not None and val != "":
                        try:
                            cur_val = float(val)
                        except (ValueError, TypeError):
                            cur_val = None
                    num_kwargs["value"] = cur_val

                new_val = st.number_input(**num_kwargs)
                if new_val is not None:
                    st.session_state.profile[key] = new_val
                elif key in st.session_state.profile and val is None:
                    del st.session_state.profile[key]

            else:
                step_val = int(q_def.get("step", 1))
                min_val = int(q_def.get("min", 0))
                max_val = int(q_def["max"]) if "max" in q_def else None
                
                num_kwargs = {
                    "label": f"Input {q_id}",
                    "min_value": min_val,
                    "max_value": max_val,
                    "step": step_val,
                    "format": "%d",
                    "placeholder": placeholder_txt,
                    "label_visibility": "collapsed",
                    "key": w_key
                }
                if not has_widget_state:
                    cur_val = None
                    if val is not None and val != "":
                        try:
                            cur_val = int(round(float(val)))
                        except (ValueError, TypeError):
                            cur_val = None
                    num_kwargs["value"] = cur_val

                new_val = st.number_input(**num_kwargs)
                if new_val is not None:
                    st.session_state.profile[key] = new_val
                elif key in st.session_state.profile and val is None:
                    del st.session_state.profile[key]

        elif input_type == "select":
            opts = q_def.get("options", [])
            str_opts = [str(o) for o in opts]
            
            cb = on_employment_type_change if key == "employment_type" else None

            sel_kwargs = {
                "label": f"Select {q_id}",
                "options": opts,
                "placeholder": "Please select...",
                "label_visibility": "collapsed",
                "key": w_key,
                "on_change": cb
            }
            if not has_widget_state:
                idx = None
                if val is not None and val != "" and val != "Please select...":
                    str_val = str(val)
                    if str_val in str_opts:
                        idx = str_opts.index(str_val)
                    elif val in opts:
                        idx = opts.index(val)
                sel_kwargs["index"] = idx

            new_val = st.selectbox(**sel_kwargs)
            if new_val is not None and new_val != "Please select...":
                st.session_state.profile[key] = new_val
            elif key in st.session_state.profile and val is None:
                del st.session_state.profile[key]

    # Render M01 - M10
    st.markdown("#### Tier 1: Universal Mandatory (10 Questions)")
    st.markdown("<p style='color:#6E6069; font-size:0.82rem; margin-top:-0.5rem;'>Required to initialize regulatory FOIR and residual cash flow math.</p>", unsafe_allow_html=True)

    mandatory_keys = [
        "loan_purpose", "target_loan_amount", "tenure_months", "employment_type",
        "net_income", "existing_emi", "rent", "living_expenses", "cibil", "age"
    ]
    for m_key in mandatory_keys:
        if m_key in MASTER_QUESTIONS:
            render_field(m_key, MASTER_QUESTIONS[m_key])

    # 3. Adaptive Variable Form - Dynamically rendered for the active employment category
    st.markdown("<hr style='border:0; border-top:1px solid #E2D9DE; margin:1.5rem 0;'>", unsafe_allow_html=True)
    
    # Re-evaluate curr_category dynamically so it immediately reflects any changes made to M04
    fv = st.session_state.get("form_version", 0)
    curr_category = st.session_state.profile.get("employment_type") or st.session_state.get(f"field_employment_type_{fv}")
    expander_title = "📋 Got a minute to improve accuracy?"

    with st.expander(expander_title, expanded=False):
        if not curr_category:
            st.markdown(
                """
                <div style='background:#F3EEF1; border:1px dashed #CFA5C1; border-radius:8px; padding:1.2rem; text-align:center; color:#6E6069;'>
                  <div style='font-size:1.5rem; margin-bottom:0.3rem;'>📋</div>
                  <p style='font-size:0.88rem; margin:0.2rem auto 0.6rem; max-width:28rem; line-height:1.5; color:#5A4D55;'>
                    You can answer a few quick optional questions to make your borrowing assessment even more accurate and help secure a tighter interest rate.
                  </p>
                  <div style='font-size:0.84rem; color:#8A4B12; font-weight:500;'>
                    👉 Please select your <b>Primary Employment Structure (M04)</b> in Tier 1 above to reveal questions tailored for you.
                  </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"<p style='color:#6E6069; font-size:0.84rem; margin-bottom:0.8rem;'>"
                f"💡 <b>Optional questions for {curr_category}:</b> Answering these quick questions helps improve assessment accuracy and sharpen your borrowing limits and fair rate band."
                f"</p>",
                unsafe_allow_html=True
            )
            active_q_list = get_questions_for_category(curr_category)
            variable_qs = [q for q in active_q_list if q["tier"] == "Variable"]
            for v_q in variable_qs:
                render_field(v_q["key"], v_q)


    # 4. PRIMARY SUBMISSION BUTTON (Explicit user action to fetch & update results)
    st.markdown("<br>", unsafe_allow_html=True)
    calc_button = st.button(
        "⚖️ Calculate My Borrowing Assessment",
        type="primary",
        use_container_width=True,
        help="Run deterministic underwriting on your entered figures"
    )

    if calc_button:
        sync_active_profile_from_widgets()
        
        mandatory_checklist = [
            ("loan_purpose", "M01. Primary Loan Purpose"),
            ("target_loan_amount", "M02. Target Loan Amount (₹)"),
            ("tenure_months", "M03. Preferred Repayment Tenure"),
            ("employment_type", "M04. Primary Employment Structure"),
            ("net_income", "M05. Net Monthly In-Hand Income (₹)"),
            ("existing_emi", "M06. Total Existing Monthly Loan EMIs (₹)"),
            ("rent", "M07. Monthly Rent / Housing Outflow (₹)"),
            ("living_expenses", "M08. Essential Monthly Living Costs (₹)"),
            ("cibil", "M09. Credit Score (CIBIL)"),
            ("age", "M10. Borrower Age (Years)"),
        ]
        
        missing = []
        for m_k, m_lbl in mandatory_checklist:
            m_v = st.session_state.profile.get(m_k)
            if m_v is None or m_v == "" or m_v == "Please select...":
                missing.append(m_lbl)
            elif m_k in ["target_loan_amount", "net_income", "living_expenses", "age"]:
                try:
                    if float(m_v) <= 0:
                        missing.append(f"{m_lbl} (must be > 0)")
                except (ValueError, TypeError):
                    missing.append(m_lbl)

        if missing:
            st.error("⚠️ **Please complete all 10 Mandatory Questions before calculating:**\n\n" + "\n".join([f"• **{item}**" for item in missing]))
        else:
            math_profile = prep_math_profile(st.session_state.profile)
            results = run_full_underwriting(math_profile)
            explanations = generate_all_explanations(math_profile, results)
            card = build_negotiation_card(math_profile, results)
            
            st.session_state.calculated_data = {
                "results": results,
                "explanations": explanations,
                "card": card,
                "profile_snapshot": dict(math_profile),
                "label": "Custom Calculated Assessment"
            }
            st.session_state.has_calculated = True
            st.session_state.just_calculated = True
            st.session_state.scroll_trigger_count = st.session_state.get("scroll_trigger_count", 0) + 1
            st.session_state.active_profile_label = "Custom Calculated Assessment"
            st.rerun()


# =============================================================================
# RIGHT COLUMN: UNDERWRITING RESULTS & NEGOTIATION CARD
# =============================================================================
with col_outputs:
    # Invisible anchor for smooth scrolling right to results
    st.markdown('<div id="results-top" style="position:relative; top:-20px;"></div>', unsafe_allow_html=True)
    
    # Auto-scroll to results on calculate - executes every single time even if results are identical
    if st.session_state.get("just_calculated", False):
        scroll_counter = st.session_state.get("scroll_trigger_count", 0)
        components.html(
            f"""
            <!-- scroll_seq_{scroll_counter} -->
            <script>
            function executeScroll() {{
                try {{
                    const doc = window.parent.document;
                    const resultsEl = doc.getElementById('results-top');
                    if (resultsEl) {{
                        resultsEl.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
                    }}
                    // If on wide desktop view, ensure main containers scroll up to align top of results
                    if (window.parent.innerWidth > 992) {{
                        const mainContainers = [
                            doc.querySelector('section[data-testid="stMain"]'),
                            doc.querySelector('.stMain'),
                            doc.querySelector('section.main'),
                            doc.querySelector('div[data-testid="stAppViewContainer"]'),
                            doc.documentElement,
                            doc.body
                        ];
                        for (let el of mainContainers) {{
                            if (el && el.scrollTo) {{
                                el.scrollTo({{ top: 0, behavior: 'smooth' }});
                            }}
                        }}
                    }}
                }} catch(e) {{
                    console.log('Scroll redirection error:', e);
                }}
            }}
            executeScroll();
            setTimeout(executeScroll, 100);
            setTimeout(executeScroll, 300);
            </script>
            """,
            height=0,
            width=0
        )
        st.session_state.just_calculated = False

    # Check if calculation is active or standby
    if not st.session_state.has_calculated or not st.session_state.get("calculated_data"):

        # STANDBY EMPTY STATE
        st.markdown("""
        <div class="standby-card">
          <div style="font-size: 2.8rem; margin-bottom: 0.6rem;">⚖️</div>
          <h3 style="margin-bottom: 0.4rem; color: #4B2440;">Ready to Run Your Underwriting Self-Assessment</h3>
          <p style="color: #6E6069; font-size: 0.92rem; max-width: 28rem; margin: 0 auto 1.4rem; line-height: 1.5;">
            Fill in your loan request and monthly income on the left, then click 
            <b style="color: #4B2440;">"Calculate My Borrowing Assessment"</b> to generate:
          </p>
          <div style="text-align: left; max-width: 26rem; margin: 0 auto 1.5rem; font-size: 0.86rem; color: #4A3E47; line-height: 1.8;">
            <div>• <b>Output 1: Recommendation Verdict</b> (Borrow / Borrow Less / Don't Borrow)</div>
            <div>• <b>Output 2: Maximum Limits</b> (Lender Sanction vs. Safe Capacity & which to use)</div>
            <div>• <b>Output 3: Fair Rate Band & All-In APR</b> (Including fee drag & statutory 18% GST)</div>
            <div>• <b>Output 4: Monthly Safe EMI Ceiling</b> (Stress-tested under simulated -20% shock)</div>
            <div>• <b>In-Branch Negotiation Card</b> (Target anchors, leverage points & spoken counter-script)</div>
          </div>
          <div style="border-top: 1px solid #E2D9DE; padding-top: 1rem; color: #8A4B12; font-size: 0.82rem; font-weight: 500;">
            💡 Tip: You can click "Test some personas" at the bottom to test a benchmark profile (Priya, Ravi, Anita) immediately.
          </div>
        </div>
        """, unsafe_allow_html=True)

    else:
        # RETRIEVE CALCULATED UNDERWRITING BUNDLE
        calc_bundle = st.session_state.calculated_data
        results = calc_bundle["results"]
        explanations = calc_bundle["explanations"]
        card = calc_bundle["card"]
        snapshot = calc_bundle.get("profile_snapshot", {})

        # Check if user has altered any inputs since the last calculation
        curr_math_profile = prep_math_profile(st.session_state.profile)
        is_dirty = any(
            curr_math_profile.get(k) != snapshot.get(k)
            for k in set(list(curr_math_profile.keys()) + list(snapshot.keys()))
        )

        if is_dirty:
            st.markdown(
                """
                <div style='margin-bottom:0.8rem; font-size:0.84rem; color:#8A4B12; background:#FEF9F3; border:1px solid #FCE5D2; padding:0.45rem 0.85rem; border-radius:6px; font-weight:500;'>
                  ✏️ <b>Inputs modified:</b> Click <b>'Calculate My Borrowing Assessment'</b> on the left to recalculate and refresh your results.
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown(
            f"<div style='margin-bottom:1rem; font-size:0.82rem; color:#6E6069;'>"
            f"Showing results for: <b>{calc_bundle.get('label', st.session_state.active_profile_label)}</b> · "
            f"<i>Modify any inputs on the left and click 'Calculate' to re-run.</i>"
            f"</div>",
            unsafe_allow_html=True
        )

        # -------------------------------------------------------------------------
        # OUTPUT 1: RECOMMENDATION VERDICT
        # -------------------------------------------------------------------------
        verdict = results["verdict"]
        v_class = "output-card-success" if verdict == "BORROW" else ("output-card-danger" if verdict == "DON'T BORROW" else "output-card-warn")
        v_icon = "✅" if verdict == "BORROW" else ("⛔" if verdict == "DON'T BORROW" else "⚠️")

        st.markdown(f"""
        <div class="output-card {v_class}">
          <span class="lokta-pill">Output 1 · Recommendation Verdict</span>
          <div class="fold-1-metric">{v_icon} {verdict}</div>
          <div class="fold-2-why">{explanations["verdict_why"]}</div>
        </div>
        """, unsafe_allow_html=True)

        # -------------------------------------------------------------------------
        # OUTPUT 2: MAXIMUM BORROWING CAPACITY (TWO-SIDED LIMITS)
        # -------------------------------------------------------------------------
        lender_amt = results["lender_max_principal"]
        safe_amt = results["borrower_safe_limit"]
        which_to_use = explanations["which_limit_recommendation"]

        st.markdown(f"""
        <div class="output-card">
          <span class="lokta-pill">Output 2 · Maximum Borrowing Capacity</span>
          <div style="display:flex; justify-content:space-between; flex-wrap:wrap; margin-top:0.4rem;">
            <div>
              <span style="font-size:0.75rem; color:#6E6069; text-transform:uppercase; font-weight:600;">Lender Max Sanction (FOIR):</span>
              <div class="fold-1-metric" style="font-size:1.35rem;">₹{lender_amt:,.0f}</div>
            </div>
            <div style="text-align:right;">
              <span style="font-size:0.75rem; color:#6E6069; text-transform:uppercase; font-weight:600;">Borrower Safe Limit (Cash Flow):</span>
              <div class="fold-1-metric" style="font-size:1.35rem; color:#1B5E3F;">₹{safe_amt:,.0f}</div>
            </div>
          </div>
          <div class="which-to-use-badge">💡 {which_to_use}</div>
          <div class="fold-2-why">{explanations["limits_why"]}</div>
        </div>
        """, unsafe_allow_html=True)

        # -------------------------------------------------------------------------
        # OUTPUT 3: FAIR INTEREST RATE BAND & ALL-IN APR
        # -------------------------------------------------------------------------
        rate_min = results["rate_min"]
        rate_max = results["rate_max"]
        apr = results["all_in_apr"]
        pf_pct = results["processing_fee_pct"]
        prod_name = results["target_product"]

        st.markdown(f"""
        <div class="output-card">
          <span class="lokta-pill">Output 3 · Fair Interest Rate & All-In APR</span>
          <div style="font-size:0.85rem; color:#4B2440; font-weight:600; margin-top:0.3rem;">Target Product: {prod_name}</div>
          <div style="display:flex; justify-content:space-between; align-items:baseline; margin-top:0.2rem;">
            <div class="fold-1-metric">{rate_min:.2f}% – {rate_max:.2f}%</div>
            <div style="font-family:'JetBrains Mono',monospace; font-size:1.15rem; color:#4B2440; font-weight:600;">
              All-In APR: <span style="background:#EFE3EA; padding:0.2rem 0.5rem; border-radius:4px;">{apr:.2f}%</span>
            </div>
          </div>
          <div style="font-size:0.78rem; color:#6E6069;">Nominal rate spread includes {pf_pct}% upfront processing fee + statutory 18% GST (IRR solved).</div>
          <div class="fold-2-why">{explanations["rate_why"]}</div>
        </div>
        """, unsafe_allow_html=True)

        # -------------------------------------------------------------------------
        # OUTPUT 4: MONTHLY PAYMENT CEILING & STRESS TEST
        # -------------------------------------------------------------------------
        monthly_ceiling = results["monthly_safe_ceiling"]
        stress_info = results["stress_results"]
        passes_stress = stress_info["passes_stress"]
        stress_badge = "✅ Survives 20% Income Shock" if passes_stress else "⚠️ Adjusted for Income Shock"

        st.markdown(f"""
        <div class="output-card">
          <span class="lokta-pill">Output 4 · Safe Monthly Payment Ceiling</span>
          <div style="display:flex; justify-content:space-between; align-items:center;">
            <div class="fold-1-metric">₹{monthly_ceiling:,.0f} <span style="font-size:0.85rem; color:#6E6069; font-weight:normal;">/ month</span></div>
            <span class="lokta-pill" style="font-size:0.75rem;">{stress_badge}</span>
          </div>
          <div style="font-size:0.78rem; color:#6E6069; margin-top:0.2rem;">
            Stress Scenario: Under a 20% income downturn (to ₹{stress_info['stressed_income']:,.0f}) & +2.0% rate hike, debt ratio is {stress_info['distress_ratio_pct']}% (Distress Cap: 65%).
          </div>
          <div class="fold-2-why">{explanations["ceiling_why"]}</div>
        </div>
        """, unsafe_allow_html=True)

        # -------------------------------------------------------------------------
        # TENURE TRADE-OFF COMPARISON SCHEDULE
        # -------------------------------------------------------------------------
        with st.expander("📊 View Tenure Trade-Off Schedule (24m vs 36m vs 48m vs 60m)", expanded=False):
            st.markdown("<p style='font-size:0.82rem; color:#6E6069;'>See how extending repayment tenure reduces your monthly EMI but increases total interest paid:</p>", unsafe_allow_html=True)
            tenure_rows = []
            for s in results["tenure_schedule"]:
                afford_tag = "✅ Safe" if s["is_affordable"] else "⛔ Exceeds Cap"
                tenure_rows.append({
                    "Tenure": f"{s['tenure_months']} Months",
                    "Monthly EMI": f"₹{s['monthly_emi']:,.0f}",
                    "Total Interest Paid": f"₹{s['total_interest']:,.0f}",
                    "Total Repayment": f"₹{s['total_repaid']:,.0f}",
                    "Affordability": afford_tag
                })
            st.table(tenure_rows)

        # -------------------------------------------------------------------------
        # STANDALONE MOBILE NEGOTIATION CARD
        # -------------------------------------------------------------------------
        st.markdown("""
        <div class="negotiation-terminal">
          <div class="terminal-header">
            <span class="terminal-title"><span class="terminal-dot"></span>Mobile Negotiation Card</span>
            <span style="font-size:0.75rem; color:#A99DA5; font-family:'JetBrains Mono',monospace;">IN-BRANCH CHEAT SHEET</span>
          </div>
        """, unsafe_allow_html=True)

        # 1. Target Anchors
        st.markdown(f"""
          <div style="margin-bottom:1rem;">
            <span style="font-size:0.75rem; text-transform:uppercase; letter-spacing:0.08em; color:#CFA5C1; font-weight:600;">1. Target Counter-Benchmarks</span>
            <div style="display:grid; grid-template-columns: 1fr 1fr; gap:0.5rem; margin-top:0.4rem; font-size:0.88rem;">
              <div>• <b>Target Product:</b> {card['target_product']}</div>
              <div>• <b>Fair Rate Band:</b> {card['fair_rate_band']}</div>
              <div>• <b>Hard APR Ceiling:</b> {card['all_in_apr']:.2f}%</div>
              <div>• <b>Max Safe EMI:</b> ₹{card['monthly_safe_ceiling']:,.0f}/mo</div>
            </div>
          </div>
        """, unsafe_allow_html=True)

        # 2. Borrower Leverage Points
        st.markdown("""
          <div style="margin-bottom:1rem;">
            <span style="font-size:0.75rem; text-transform:uppercase; letter-spacing:0.08em; color:#4EBA88; font-weight:600;">2. Your Leverage Points (Why You Deserve Prime Terms)</span>
            <ul style="margin-top:0.4rem; padding-left:1.2rem; font-size:0.85rem; color:#EEE6EA;">
        """, unsafe_allow_html=True)
        for lev in card["leverage_points"]:
            st.markdown(f"<li>{lev}</li>", unsafe_allow_html=True)
        st.markdown("</ul></div>", unsafe_allow_html=True)

        # 3. Bank Traps to Reject
        st.markdown("""
          <div style="margin-bottom:1rem;">
            <span style="font-size:0.75rem; text-transform:uppercase; letter-spacing:0.08em; color:#F87171; font-weight:600;">3. Bank Traps to Decline</span>
            <ul style="margin-top:0.4rem; padding-left:1.2rem; font-size:0.85rem; color:#EEE6EA;">
        """, unsafe_allow_html=True)
        for trap in card["traps_to_reject"]:
            st.markdown(f"<li>{trap}</li>", unsafe_allow_html=True)
        st.markdown("</ul></div>", unsafe_allow_html=True)

        # 4. Verbatim Spoken Counter-Script
        st.markdown("""
          <div>
            <span style="font-size:0.75rem; text-transform:uppercase; letter-spacing:0.08em; color:#CFA5C1; font-weight:600;">4. Word-For-Word In-Branch Script (Read to Loan Officer)</span>
        """, unsafe_allow_html=True)
        st.markdown(f'<div class="script-box">"{card["spoken_script"]}"</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Copy script button (copies script to clipboard)
        st.code(card["spoken_script"], language="text")

# -----------------------------------------------------------------------------
# BENCHMARK PERSONA TESTING SECTION (BOTTOM BEFORE FOOTER)
# -----------------------------------------------------------------------------
st.markdown("<hr style='border:0; border-top:1px solid #E2D9DE; margin:2.2rem 0 1.2rem;'>", unsafe_allow_html=True)

with st.expander("🧪 Test some personas", expanded=False):
    st.markdown(
        "<div style='margin-bottom:1rem;'>"
        "<b style='color:#4B2440; font-size:1.02rem;'>Benchmark Borrower Profiles</b><br>"
        "<span style='color:#6E6069; font-size:0.86rem;'>"
        "Click any benchmark profile below to automatically populate the questionnaire, execute deterministic underwriting, and inspect the resulting decisions and Negotiation Cards."
        "</span>"
        "</div>",
        unsafe_allow_html=True
    )
    b_col1, b_col2, b_col3 = st.columns(3, gap="medium")
    
    with b_col1:
        st.markdown(
            """
            <div style='background:#FFFFFF; border:1px solid #E2D9DE; border-radius:8px; padding:1.1rem; min-height:175px; margin-bottom:0.8rem;'>
              <b style='color:#4B2440; font-size:1rem;'>👤 Priya, 29</b><br>
              <span style='font-size:0.75rem; color:#6E6069; text-transform:uppercase; font-weight:600;'>Bengaluru · Salaried MNC</span>
              <p style='font-size:0.82rem; color:#4A3E47; margin:0.5rem 0 0.8rem; line-height:1.45;'>
                Software engineer at MNC. ₹1.1L/mo salary, ₹14k car loan EMI, CIBIL 780, rents at ₹28k. Wants ₹8L personal loan for wedding.
              </p>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("Load Priya's Profile", key="btn_bottom_priya", use_container_width=True):
            apply_persona("priya")
            st.rerun()

    with b_col2:
        st.markdown(
            """
            <div style='background:#FFFFFF; border:1px solid #E2D9DE; border-radius:8px; padding:1.1rem; min-height:175px; margin-bottom:0.8rem;'>
              <b style='color:#4B2440; font-size:1rem;'>🏪 Ravi, 42</b><br>
              <span style='font-size:0.75rem; color:#6E6069; text-transform:uppercase; font-weight:600;'>Mysuru · Kirana MSME</span>
              <p style='font-size:0.82rem; color:#4A3E47; margin:0.5rem 0 0.8rem; line-height:1.45;'>
                Kirana owner for 14 yrs. ₹85k cash, ITR ₹4.2L/yr. Owns unencumbered shop premises (₹45L), no CIBIL. Wants ₹15L business loan.
              </p>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("Load Ravi's Profile", key="btn_bottom_ravi", use_container_width=True):
            apply_persona("ravi")
            st.rerun()

    with b_col3:
        st.markdown(
            """
            <div style='background:#FFFFFF; border:1px solid #E2D9DE; border-radius:8px; padding:1.1rem; min-height:175px; margin-bottom:0.8rem;'>
              <b style='color:#4B2440; font-size:1rem;'>🛵 Anita, 35</b><br>
              <span style='font-size:0.75rem; color:#6E6069; text-transform:uppercase; font-weight:600;'>Hubballi · Informal Delivery</span>
              <p style='font-size:0.82rem; color:#4A3E47; margin:0.5rem 0 0.8rem; line-height:1.45;'>
                Delivery rider & tailoring. ₹28k/mo, 1 EMI bounce, 3 app loans totaling ₹35k at 36% APR. Wants ₹1.5L for electric scooter.
              </p>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("Load Anita's Profile", key="btn_bottom_anita", use_container_width=True):
            apply_persona("anita")
            st.rerun()

# -----------------------------------------------------------------------------
# FOOTER & REPOSITORY ATTRIBUTION
# -----------------------------------------------------------------------------
st.markdown("<hr style='border:0; border-top:1px solid #E2D9DE; margin:2.5rem 0 1rem;'>", unsafe_allow_html=True)
st.markdown(
    "<div style='text-align:center; font-size:0.82rem; color:#6E6069;'>"
    "<b>Lokta Borrower Copilot</b> · Deterministic Underwriting Self-Assessment · "
    "<a href='file:///c:/Users/soumy/OneDrive/Desktop/lending%20copilot/RULES.md' style='color:#4B2440;'>View RULES.md</a> · "
    "<a href='file:///c:/Users/soumy/OneDrive/Desktop/lending%20copilot/WALKTHROUGH.md' style='color:#4B2440;'>View WALKTHROUGH.md</a>"
    "</div>",
    unsafe_allow_html=True
)
