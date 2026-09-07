"""
engine/underwriting.py
Financial Mathematics, Ratios, Amortization, and Dual Shock Stress-Testing.
Zero external dependencies (pure Python math/typing).
"""

import math
from typing import Dict, Any, Tuple, Optional


def calculate_pmt(rate_annual_pct: float, n_months: int, principal: float) -> float:
    """
    Computes monthly installment (EMI) using standard fixed-rate amortization:
    EMI = P * r * (1 + r)^n / ((1 + r)^n - 1)
    where r = (rate_annual_pct / 100) / 12.
    """
    if principal <= 0 or n_months <= 0:
        return 0.0
    if rate_annual_pct <= 0:
        return round(principal / n_months, 2)

    r = (rate_annual_pct / 100.0) / 12.0
    factor = (1.0 + r) ** n_months
    emi = principal * r * factor / (factor - 1.0)
    return round(emi, 2)


def calculate_present_value(rate_annual_pct: float, n_months: int, emi: float) -> float:
    """
    Reverses a monthly installment into the maximum loan principal it can service:
    PV = EMI * [1 - (1 + r)^(-n)] / r
    """
    if emi <= 0 or n_months <= 0:
        return 0.0
    if rate_annual_pct <= 0:
        return round(emi * n_months, 2)

    r = (rate_annual_pct / 100.0) / 12.0
    pv = emi * (1.0 - (1.0 + r) ** (-n_months)) / r
    return round(pv, 2)


def solve_all_in_apr(
    principal: float,
    emi: float,
    n_months: int,
    processing_fee_pct: float = 1.0,
    doc_charges: float = 0.0,
    gst_rate: float = 0.18
) -> float:
    """
    Calculates True All-In APR (Annualized Internal Rate of Return) accounting for
    upfront processing fees and statutory 18% GST.
    Net Disbursed Cash = Principal - [(Principal * fee_pct * 1.18) + doc_charges]
    Solves for m: sum_{t=1}^n [EMI / (1+m)^t] = Net Disbursed Cash
    APR = m * 12 * 100.
    """
    upfront_fee = (principal * (processing_fee_pct / 100.0) * (1.0 + gst_rate)) + doc_charges
    net_disbursed = principal - upfront_fee

    if net_disbursed <= 0 or emi <= 0 or n_months <= 0:
        return 0.0

    # Initial guess using simple interest proxy
    m = (emi * n_months / net_disbursed - 1.0) / (n_months / 2.0)
    if m <= 0:
        m = 0.01

    # Newton-Raphson 50 iterations
    for _ in range(50):
        if abs(m) < 1e-9:
            pv = emi * n_months
            pv_prime = -emi * n_months * (n_months + 1) / 2.0
        else:
            factor = (1.0 + m) ** (-n_months)
            pv = emi * (1.0 - factor) / m
            pv_prime = emi * ((n_months * factor / ((1.0 + m) * m)) - ((1.0 - factor) / (m * m)))

        diff = pv - net_disbursed
        if abs(diff) < 1e-5:
            break
        if abs(pv_prime) < 1e-12:
            break

        step = diff / pv_prime
        m = m - step
        if m <= -0.99:
            m = 0.001

    apr = max(0.0, m * 12.0 * 100.0)
    return round(apr, 2)


def get_foir_benchmark(category: str, corporate_tier: Optional[str] = None) -> float:
    """
    Codified standard FOIR caps in Indian retail lending:
    - Salaried Tier-1 / PSU: 55% (up to 60% for public sector)
    - Salaried Standard / Mid-Market: 50%
    - Salaried Startup / Contract: 45%
    - Self-Employed MSME: 45%
    - Informal / Gig Economy: 40%
    """
    cat = (category or "").lower()
    tier = (corporate_tier or "").lower()

    if "salaried" in cat:
        if "tier-1" in tier or "mnc" in tier or "govt" in tier or "psu" in tier:
            return 0.55
        if "startup" in tier or "contract" in tier:
            return 0.45
        return 0.50
    elif "self" in cat or "msme" in cat:
        return 0.45
    else:
        return 0.40


def calculate_lender_max_sanction(
    net_income: float,
    existing_emi: float,
    rate_annual_pct: float,
    n_months: int,
    foir_cap: float = 0.50,
    collateral_value: float = 0.0,
    is_lap: bool = False
) -> Tuple[float, float]:
    """
    Returns (lender_max_emi, lender_max_principal).
    If collateral is present (LAP pivot), sanction is bounded by 50%-55% LTV.
    """
    max_allowable_debt_outflow = net_income * foir_cap
    lender_max_emi = max(0.0, max_allowable_debt_outflow - existing_emi)
    lender_max_principal = calculate_present_value(rate_annual_pct, n_months, lender_max_emi)

    # Product Pivot / Collateral Check (LAP Loan-to-Value cap: 50% - 55%)
    if is_lap and collateral_value > 0:
        ltv_principal_cap = collateral_value * 0.50
        if lender_max_principal > ltv_principal_cap:
            lender_max_principal = ltv_principal_cap
            lender_max_emi = calculate_pmt(rate_annual_pct, n_months, lender_max_principal)

    return round(lender_max_emi, 2), round(lender_max_principal, 2)


def calculate_borrower_safe_capacity(
    net_income: float,
    existing_emi: float,
    rent: float,
    living_expenses: float,
    rate_annual_pct: float,
    n_months: int,
    liquid_runway_months: float = 0.0,
    productive_income_boost: float = 0.0,
    is_monsoon_impacted: bool = False,
    seasonal_variance_pct: float = 0.0
) -> Tuple[float, float, float]:
    """
    Returns (safe_emi_capacity, safe_borrowing_limit, emergency_buffer).
    Emergency Buffer: 5% if runway >= 6 months, else 10% of monthly income.
    """
    buffer_pct = 0.05 if liquid_runway_months >= 6.0 else 0.10
    emergency_buffer = net_income * buffer_pct

    # Baseline disposable surplus
    disposable_cash = net_income - existing_emi - rent - living_expenses - emergency_buffer + productive_income_boost

    # Seasonal trough adjustment for self-employed merchants
    if is_monsoon_impacted and seasonal_variance_pct > 0.20:
        # anchor to the lower quartile cash flow to survive trough months
        disposable_cash = disposable_cash * (1.0 - (seasonal_variance_pct * 0.5))

    safe_emi_capacity = max(0.0, disposable_cash)
    safe_borrowing_limit = calculate_present_value(rate_annual_pct, n_months, safe_emi_capacity)

    return round(safe_emi_capacity, 2), round(safe_borrowing_limit, 2), round(emergency_buffer, 2)


def run_dual_stress_test(
    net_income: float,
    existing_emi: float,
    requested_principal: float,
    base_rate_pct: float,
    n_months: int,
    baseline_safe_emi: float,
    distress_threshold_pct: float = 0.65
) -> Dict[str, Any]:
    """
    Simulates dual macroeconomic shocks:
    1. Income Shock: 20% immediate drop in net income (I_stress = I_net * 0.80)
    2. Interest Rate Shock: +2.0% spike on floating rate debt (r_stress = base_rate + 2.0%)
    3. Safety Condition: Stressed Total Debt Outflow / I_stress <= 65%
    If ratio > 65%, ratchet down safe monthly ceiling until test clears.
    """
    stressed_income = net_income * 0.80
    stressed_rate = base_rate_pct + 2.0
    stressed_new_emi = calculate_pmt(stressed_rate, n_months, requested_principal)
    stressed_total_debt = existing_emi + stressed_new_emi

    distress_ratio = (stressed_total_debt / stressed_income) if stressed_income > 0 else 1.0
    passes_stress = distress_ratio <= distress_threshold_pct

    # Max allowable installment under 65% ceiling during stress
    max_allowable_stressed_emi = max(0.0, (stressed_income * distress_threshold_pct) - existing_emi)

    adjusted_ceiling = baseline_safe_emi
    was_adjusted = False

    if baseline_safe_emi > max_allowable_stressed_emi:
        adjusted_ceiling = max_allowable_stressed_emi
        was_adjusted = True

    return {
        "stressed_income": round(stressed_income, 2),
        "stressed_rate": round(stressed_rate, 2),
        "stressed_new_emi": round(stressed_new_emi, 2),
        "stressed_total_debt": round(stressed_total_debt, 2),
        "distress_ratio_pct": round(distress_ratio * 100.0, 1),
        "passes_stress": passes_stress,
        "was_adjusted": was_adjusted,
        "final_safe_ceiling": round(adjusted_ceiling, 2)
    }


def evaluate_verdict(
    bounces_last_6m: int,
    active_digital_app_count: int,
    app_loan_apr: float,
    safe_emi_cap: float,
    requested_emi: float,
    requested_principal: float,
    safe_principal_limit: float,
    distress_ratio_pct: float
) -> Tuple[str, str]:
    """
    Evaluates final recommendation verdict via strict 3-tier hierarchical triage:
    Tier 1: Distress Kill-Switches -> DON'T BORROW
    Tier 2: Over-Leverage & Capacity Constraints -> BORROW LESS
    Tier 3: Affordability Pass & Stress Resilience -> BORROW
    """
    # Tier 1: Distress / Kill-Switch
    if bounces_last_6m >= 1:
        return "DON'T BORROW", "bounces_detected"
    if active_digital_app_count >= 1 and app_loan_apr >= 24.0:
        return "DON'T BORROW", "predatory_app_debt"
    if safe_emi_cap <= 0:
        return "DON'T BORROW", "zero_surplus_deficit"

    # Tier 2: Over-Leverage & Capacity
    if requested_emi > safe_emi_cap or requested_principal > (safe_principal_limit * 1.05):
        return "BORROW LESS", "exceeds_safe_headroom"
    if distress_ratio_pct > 65.0:
        return "BORROW LESS", "fails_stress_test"

    # Tier 3: Affordability Pass
    return "BORROW", "clean_affordability_pass"


def run_full_underwriting(profile: Dict[str, Any]) -> Dict[str, Any]:
    """
    Master pipeline orchestrator taking raw profile inputs and returning complete
    deterministic underwriting figures for O1, O2, O3, O4.
    """
    # Universal Mandatory Inputs
    net_income = float(profile.get("net_income", 0.0))
    requested_principal = float(profile.get("target_loan_amount", 0.0))
    tenure_months = int(profile.get("tenure_months", 48))
    existing_emi = float(profile.get("existing_emi", 0.0))
    rent = float(profile.get("rent", 0.0))
    living_expenses = float(profile.get("living_expenses", 0.0))
    category = profile.get("employment_type", "Salaried")
    cibil = profile.get("cibil", "Unknown")

    # Key Category Variables
    corporate_tier = profile.get("employer_tier", "Standard")
    job_vintage_yrs = float(profile.get("job_vintage_years", 3.0))
    liquid_runway_mos = float(profile.get("liquid_savings_months", 0.0))
    collateral_val = float(profile.get("property_market_value", 0.0))
    has_unencumbered_property = bool(profile.get("has_unencumbered_property", False))
    bounces_6m = int(profile.get("payment_bounces_6m", 0))
    app_loan_count = int(profile.get("active_app_loan_count", 0))
    app_loan_apr = float(profile.get("app_loan_apr", 0.0))
    co_applicant_income = float(profile.get("co_applicant_income", 0.0))
    productive_income_gain = float(profile.get("productive_income_boost", 0.0))
    quoted_fee_pct = float(profile.get("quoted_processing_fee_pct", 1.0))
    is_monsoon_variance = bool(profile.get("seasonal_variance_high", False))

    total_qualifying_income = net_income + co_applicant_income

    # 1. Product Identification & Baseline Rates
    is_lap = has_unencumbered_property or collateral_val > 0
    if is_lap:
        target_product = "Loan Against Property (LAP) / Mortgage Line"
        base_rate_min, base_rate_max = 9.75, 10.50
        nominal_pf = 1.0
    elif "informal" in category.lower() or "gig" in category.lower():
        if "ev" in str(profile.get("loan_purpose", "")).lower() or profile.get("is_ev_vehicle", False):
            target_product = "Priority Sector Commercial EV Hypothecation"
            base_rate_min, base_rate_max = 11.50, 13.00
            nominal_pf = 1.25
        else:
            target_product = "Microfinance / Priority Sector Credit Line"
            base_rate_min, base_rate_max = 12.50, 15.00
            nominal_pf = 1.5
    else:
        if "tier-1" in corporate_tier.lower() or "mnc" in corporate_tier.lower():
            target_product = "Prime Unsecured Corporate Personal Loan"
            base_rate_min, base_rate_max = 11.00, 11.75
            nominal_pf = 1.0
        else:
            target_product = "Standard Retail Personal Loan"
            base_rate_min, base_rate_max = 12.00, 14.00
            nominal_pf = 1.5

    # 2. Risk Adjustments on Rates
    spread_adj = 0.0
    cibil_str = str(cibil).strip()
    is_cibil_unknown = "unknown" in cibil_str.lower() or "unscored" in cibil_str.lower()

    if is_cibil_unknown:
        # Rule 3: Unknown is never zero. Widen band symmetrically.
        rate_min = max(8.5, base_rate_min - 0.75)
        rate_max = base_rate_max + 1.25
    elif "750" in cibil_str or (isinstance(cibil, (int, float)) and cibil >= 750):
        spread_adj -= 0.50
        rate_min = base_rate_min + spread_adj
        rate_max = base_rate_max + spread_adj
    elif "below 700" in cibil_str or (isinstance(cibil, (int, float)) and cibil < 700):
        spread_adj += 1.50
        rate_min = base_rate_min + spread_adj
        rate_max = base_rate_max + spread_adj
    else:
        rate_min = base_rate_min
        rate_max = base_rate_max

    rate_min = round(max(8.5, rate_min), 2)
    rate_max = round(rate_max, 2)
    midpoint_rate = round((rate_min + rate_max) / 2.0, 2)

    # 3. Upfront Fees & All-In APR
    effective_pf = quoted_fee_pct if quoted_fee_pct > 0 else nominal_pf
    requested_emi = calculate_pmt(midpoint_rate, tenure_months, requested_principal)
    all_in_apr = solve_all_in_apr(requested_principal, requested_emi, tenure_months, effective_pf)

    # 4. Two-Sided Borrowing Limits (O2)
    foir_benchmark = get_foir_benchmark(category, corporate_tier)
    lender_max_emi, lender_max_principal = calculate_lender_max_sanction(
        total_qualifying_income, existing_emi, midpoint_rate, tenure_months,
        foir_cap=foir_benchmark, collateral_value=collateral_val, is_lap=is_lap
    )

    safe_emi_cap, safe_principal_limit, emergency_buffer = calculate_borrower_safe_capacity(
        total_qualifying_income, existing_emi, rent, living_expenses,
        midpoint_rate, tenure_months, liquid_runway_months=liquid_runway_mos,
        productive_income_boost=productive_income_gain,
        is_monsoon_impacted=is_monsoon_variance, seasonal_variance_pct=0.35 if is_monsoon_variance else 0.0
    )

    # 5. Stress Testing & Monthly Safe Ceiling (O4)
    baseline_safe_emi = min(lender_max_emi, safe_emi_cap)
    stress_results = run_dual_stress_test(
        total_qualifying_income, existing_emi, requested_principal,
        midpoint_rate, tenure_months, baseline_safe_emi
    )
    final_safe_emi_ceiling = stress_results["final_safe_ceiling"]

    # 6. Recommendation Verdict (O1)
    verdict, verdict_driver = evaluate_verdict(
        bounces_last_6m=bounces_6m,
        active_digital_app_count=app_loan_count,
        app_loan_apr=app_loan_apr,
        safe_emi_cap=final_safe_emi_ceiling,
        requested_emi=requested_emi,
        requested_principal=requested_principal,
        safe_principal_limit=safe_principal_limit,
        distress_ratio_pct=stress_results["distress_ratio_pct"]
    )

    # If Kill-switch fired, freeze borrowing limits to 0
    if verdict == "DON'T BORROW":
        lender_sanction_display = 0.0
        safe_limit_display = 0.0
    else:
        lender_sanction_display = lender_max_principal
        safe_limit_display = safe_principal_limit

    # 7. Tenure Trade-Off Schedule
    tenure_options = [24, 36, 48, 60]
    tenure_schedule = []
    for t in tenure_options:
        t_emi = calculate_pmt(midpoint_rate, t, requested_principal)
        total_repaid = round(t_emi * t, 2)
        total_interest = round(total_repaid - requested_principal, 2)
        tenure_schedule.append({
            "tenure_months": t,
            "monthly_emi": t_emi,
            "total_interest": total_interest,
            "total_repaid": total_repaid,
            "is_affordable": t_emi <= final_safe_emi_ceiling
        })

    return {
        "verdict": verdict,
        "verdict_driver": verdict_driver,
        "target_product": target_product,
        "rate_min": rate_min,
        "rate_max": rate_max,
        "midpoint_rate": midpoint_rate,
        "all_in_apr": all_in_apr,
        "processing_fee_pct": effective_pf,
        "requested_emi": requested_emi,
        "lender_max_emi": lender_max_emi,
        "lender_max_principal": lender_sanction_display,
        "borrower_safe_emi": safe_emi_cap,
        "borrower_safe_limit": safe_limit_display,
        "recommended_which_limit": "safe_limit" if safe_limit_display <= lender_sanction_display else "lender_sanction",
        "monthly_safe_ceiling": final_safe_emi_ceiling,
        "emergency_buffer": emergency_buffer,
        "stress_results": stress_results,
        "tenure_schedule": tenure_schedule,
        "is_lap": is_lap,
        "is_cibil_unknown": is_cibil_unknown,
        "foir_benchmark_pct": round(foir_benchmark * 100.0, 1)
    }
