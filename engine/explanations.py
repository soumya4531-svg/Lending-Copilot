"""
engine/explanations.py
Deterministic Bottleneck Priority Trees & Single-Sentence "The Why" Formulators.
Fulfills Rule 4: "The borrower must be able to read, in one sentence, why the ceiling is ₹22,000 and not ₹30,000."
"""

from typing import Dict, Any


def explain_verdict(profile: Dict[str, Any], calculated: Dict[str, Any]) -> str:
    """
    Generates the single-sentence reason for Output 1 (Verdict: BORROW, BORROW LESS, or DON'T BORROW).
    Follows strict risk hierarchy: Distress Kill-Switches -> Cash Deficit -> Over-Leverage -> Affordability Pass.
    """
    verdict = calculated.get("verdict", "BORROW")
    bounces = int(profile.get("payment_bounces_6m", 0))
    app_loan_count = int(profile.get("active_app_loan_count", 0))
    app_loan_apr = float(profile.get("app_loan_apr", 0.0))
    safe_emi_cap = float(calculated.get("monthly_safe_ceiling", 0.0))
    requested_emi = float(calculated.get("requested_emi", 0.0))
    requested_principal = float(profile.get("target_loan_amount", 0.0))
    safe_limit = float(calculated.get("borrower_safe_limit", 0.0))

    if verdict == "DON'T BORROW":
        if bounces >= 1 and app_loan_count >= 1:
            return (
                f"Why: An auto-debit payment bounce in the last 6 months and active high-cost app loans ({app_loan_apr:.0f}% APR) "
                f"flag serious financial stress. Taking on new debt before clearing these could make managing your finances very difficult."
            )
        if bounces >= 1:
            return (
                f"Why: An auto-debit payment bounce in the last 6 months means new borrowing is too risky right now. "
                f"Clearing overdue payments first is much safer than adding another loan."
            )
        if app_loan_count >= 1 and app_loan_apr >= 24.0:
            return (
                f"Why: You have active app loans at {app_loan_apr:.0f}% APR. Taking on another loan before paying these off "
                f"creates a compounding debt trap."
            )
        if safe_emi_cap <= 0:
            return (
                f"Why: Your regular expenses and current loan payments leave very little of your income free. "
                f"Taking on another loan now could make your existing commitments harder to manage."
            )
        return "Why: Your current expenses and loan payments leave very little room for another loan right now."

    elif verdict == "BORROW LESS":
        if requested_emi > safe_emi_cap:
            return (
                f"Why: A bank may approve this loan, but the monthly payment of ₹{requested_emi:,.0f} is higher than the "
                f"₹{safe_emi_cap:,.0f} that comfortably fits your budget. Consider borrowing closer to ₹{safe_limit:,.0f}, or repaying over a longer period."
            )
        if requested_principal > safe_limit:
            return (
                f"Why: The amount you asked for (₹{requested_principal:,.0f}) is higher than your safe borrowing limit of "
                f"₹{safe_limit:,.0f}. Applying for ₹{safe_limit:,.0f} is much safer for your monthly budget."
            )
        return (
            f"Why: If your income dropped or interest rates rose, this loan payment would take up too much of your monthly budget."
        )

    else:  # BORROW
        if profile.get("has_unencumbered_property") or calculated.get("is_lap"):
            return (
                f"Why: Using your debt-free property unlocks a much lower interest rate, and your monthly payment of "
                f"₹{requested_emi:,.0f} fits comfortably within your safe monthly budget."
            )
        return (
            f"Why: Your requested monthly payment of ₹{requested_emi:,.0f} is within your affordable monthly limit of "
            f"₹{safe_emi_cap:,.0f}. You should still have room for your regular expenses and emergencies."
        )


def explain_borrowing_limits(profile: Dict[str, Any], calculated: Dict[str, Any]) -> Dict[str, str]:
    """
    Generates the explanation for Output 2 (Lender Sanction vs. Borrower Safe Limit),
    and crucially tells the borrower WHICH ONE TO USE.
    """
    lender = float(calculated.get("lender_max_principal", 0.0))
    safe = float(calculated.get("borrower_safe_limit", 0.0))
    rent = float(profile.get("rent", 0.0))
    living = float(profile.get("living_expenses", 0.0))
    is_lap = bool(calculated.get("is_lap", False))

    if calculated.get("verdict") == "DON'T BORROW":
        why = (
            f"Why: Your current loan payments and monthly expenses leave very little room for another loan. "
            f"Taking one on now could make your existing commitments harder to manage."
        )
        recommendation = "Do not borrow — clear overdue payments and reduce existing debt before borrowing."
    elif is_lap:
        why = (
            f"Why: Pledging your unencumbered property unlocks secured Loan Against Property (LAP) up to ₹{lender:,.0f} "
            f"at a lower interest rate, avoiding high-interest unsecured loans."
        )
        recommendation = f"Use your safe limit (₹{safe:,.0f}): This keeps your monthly payments comfortable and aligned with your real cash flow."
    elif safe < lender:
        why = (
            f"Why: A bank looks only at your gross income and may offer up to ₹{lender:,.0f}, but your rent (₹{rent:,.0f}) "
            f"and essential expenses limit what you can safely afford to ₹{safe:,.0f}."
        )
        recommendation = (
            f"Use your safe limit (₹{safe:,.0f}): Borrowing the full amount a bank offers can leave too little room "
            f"for your regular expenses and emergencies."
        )
    else:
        why = (
            f"Why: Your regular expenses and current debt leave plenty of room each month, so you can safely afford the full amount a bank would offer."
        )
        recommendation = f"Use the lender offer (₹{lender:,.0f}): Your income and savings comfortably support this loan."

    return {
        "why": why,
        "recommendation": recommendation
    }


def explain_rate_band(profile: Dict[str, Any], calculated: Dict[str, Any]) -> str:
    """
    Generates the explanation for Output 3 (Fair Interest Rate Band & All-In APR).
    """
    is_lap = bool(calculated.get("is_lap", False))
    cibil = profile.get("cibil", "Unknown")
    cibil_str = str(cibil).strip()
    rate_min = calculated.get("rate_min", 10.5)
    rate_max = calculated.get("rate_max", 11.5)
    apr = calculated.get("all_in_apr", 11.65)
    pf_pct = calculated.get("processing_fee_pct", 1.0)
    category = profile.get("employment_type", "Salaried")

    if is_lap:
        return (
            f"Why: Using your unencumbered property unlocks Loan Against Property (LAP) rates of {rate_min}%–{rate_max}%, "
            f"which are much lower than standard unsecured business rates."
        )
    if "informal" in category.lower() or "gig" in category.lower():
        if profile.get("is_ev_vehicle") or "ev" in str(profile.get("loan_purpose", "")).lower():
            return (
                f"Why: Financing an electric vehicle unlocks a lower commercial EV rate of {rate_min}%–{rate_max}%, "
                f"much cheaper than instant app loans."
            )
        return (
            f"Why: Priority sector small-loan rates set your fair rate range at {rate_min}%–{rate_max}%, "
            f"far below high-interest digital loan apps."
        )
    if "750" in cibil_str or (isinstance(cibil, (int, float)) and cibil >= 750):
        return (
            f"Why: A credit score of 750+ and stable employment qualify you for a prime rate of {rate_min}%–{rate_max}%. "
            f"The estimated yearly cost adds a {pf_pct}% processing fee plus statutory 18% GST (APR {apr}%)."
        )
    if calculated.get("is_cibil_unknown"):
        return (
            f"Why: A wider range of {rate_min}%–{rate_max}% is shown because your credit score is unverified, "
            f"without treating you as high risk."
        )
    return (
        f"Why: This range reflects your credit score and income type. The estimated yearly cost of {apr}% "
        f"includes standard fees and tax on top of the interest rate."
    )


def explain_monthly_ceiling(profile: Dict[str, Any], calculated: Dict[str, Any]) -> str:
    """
    Generates the single-sentence explanation for Output 4 (Monthly Safe EMI Ceiling & Stress Resilience).
    """
    safe_cap = float(calculated.get("monthly_safe_ceiling", 0.0))
    lender_emi = float(calculated.get("lender_max_emi", 0.0))
    rent = float(profile.get("rent", 0.0))
    living = float(profile.get("living_expenses", 0.0))
    stress_results = calculated.get("stress_results", {})
    category = profile.get("employment_type", "Salaried")

    if calculated.get("verdict") == "DON'T BORROW":
        return (
            f"Why: Your necessary living costs and current loan payments leave only ₹{safe_cap:,.0f} a month; "
            f"clearing high-cost app debt comes first before taking a new loan."
        )
    if stress_results.get("was_adjusted"):
        return (
            f"Why: If your income dropped by 20% or interest rates rose, a monthly payment above ₹{safe_cap:,.0f} "
            f"would stretch your budget too thin, so your safe ceiling was set here."
        )
    if profile.get("seasonal_variance_high") or "self" in category.lower():
        return (
            f"Why: Because small business earnings fluctuate through the year, your safe monthly payment of "
            f"₹{safe_cap:,.0f} is anchored to your lower earning months."
        )
    if safe_cap < lender_emi:
        return (
            f"Why: While a bank might allow monthly payments up to ₹{lender_emi:,.0f}, your rent of ₹{rent:,.0f} "
            f"and essential expenses mean keeping your payment at or below ₹{safe_cap:,.0f} protects your emergency cushion."
        )
    return (
        f"Why: Keeping your payment at or below ₹{safe_cap:,.0f} a month leaves plenty of breathing room for daily expenses and savings."
    )


def generate_all_explanations(profile: Dict[str, Any], calculated: Dict[str, Any]) -> Dict[str, Any]:
    """
    Bundles all qualitative "The Why" explanations into a single dictionary.
    """
    limits_explained = explain_borrowing_limits(profile, calculated)

    return {
        "verdict_why": explain_verdict(profile, calculated),
        "limits_why": limits_explained["why"],
        "which_limit_recommendation": limits_explained["recommendation"],
        "rate_why": explain_rate_band(profile, calculated),
        "ceiling_why": explain_monthly_ceiling(profile, calculated)
    }
