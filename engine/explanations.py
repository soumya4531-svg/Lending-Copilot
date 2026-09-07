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
                f"Why: An auto-debit bounce in the last 6 months and active high-cost app debt ({app_loan_apr:.0f}% APR) "
                f"flag acute distress; adding new debt before clearing arrears creates severe insolvency risk."
            )
        if bounces >= 1:
            return (
                f"Why: An auto-debit payment bounce in the last 6 months triggered our distress safety rule; "
                f"adding new debt before clearing arrears creates extreme default risk."
            )
        if app_loan_count >= 1 and app_loan_apr >= 24.0:
            return (
                f"Why: You carry active digital app loans above 24% APR; taking new loans before consolidating "
                f"these leads to a compounding high-cost debt trap."
            )
        if safe_emi_cap <= 0:
            return (
                f"Why: Essential living costs of ₹{float(profile.get('living_expenses', 0)):,g} and existing debt of "
                f"₹{float(profile.get('existing_emi', 0)):,g} already consume 100% of your take-home pay, leaving no safety margin."
            )
        return "Why: Critical cash-flow distress signals were detected; new borrowing is blocked to prevent insolvency."

    elif verdict == "BORROW LESS":
        if requested_emi > safe_emi_cap:
            gap = requested_emi - safe_emi_cap
            return (
                f"Why: Your requested loan requires an EMI of ₹{requested_emi:,.0f}, which overshoots your safe monthly "
                f"ceiling of ₹{safe_emi_cap:,.0f} by ₹{gap:,.0f}."
            )
        if requested_principal > safe_limit:
            principal_gap = requested_principal - safe_limit
            return (
                f"Why: Your requested loan of ₹{requested_principal:,.0f} exceeds your safe borrowing limit of "
                f"₹{safe_limit:,.0f} by ₹{principal_gap:,.0f}."
            )
        return (
            f"Why: Servicing your requested loan under our simulated 20% income shock breaches the safe 65% debt-to-income threshold."
        )

    else:  # BORROW
        if profile.get("has_unencumbered_property") or calculated.get("is_lap"):
            return (
                f"Why: Pledging unencumbered commercial property unlocks prime LAP capacity, and your ₹{requested_emi:,.0f} "
                f"monthly EMI fits comfortably within your safe cash flow."
            )
        return (
            f"Why: Your requested monthly EMI of ₹{requested_emi:,.0f} fits comfortably within your ₹{safe_emi_cap:,.0f} "
            f"safe monthly limit while keeping your emergency living buffer intact."
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
        driver = calculated.get("verdict_driver", "")
        bounces = int(profile.get("payment_bounces_6m", 0))
        app_loan_count = int(profile.get("active_app_loan_count", 0))
        
        if driver == "zero_surplus_deficit" or (bounces == 0 and app_loan_count == 0):
            why = (
                f"Why: Essential living expenses (₹{living:,.0f}) and existing obligations leave zero residual "
                f"cash flow surplus after reserving a basic 10% emergency buffer, leaving no headroom to service any new EMI."
            )
            recommendation = "Do Not Borrow — Increase monthly cash flow surplus or reduce expenses before taking new debt."
        else:
            why = (
                "Why: Active payment bounces and digital loan arrears block institutional lending eligibility "
                "until existing debts are consolidated."
            )
            recommendation = "Do Not Borrow — Prioritize debt restructuring and app loan consolidation."
    elif is_lap:
        why = (
            f"Why: Pledging your unencumbered property pivots you to secured LAP, unlocking up to ₹{lender:,.0f} "
            f"while avoiding predatory 18%+ unsecured business installment loans."
        )
        recommendation = f"Use Your Safe Limit (₹{safe:,.0f}): Anchors your borrowing to real cash flow."
    elif safe < lender:
        why = (
            f"Why: Banks will approve up to ₹{lender:,.0f} based purely on gross salary, but your rent of ₹{rent:,.0f} "
            f"and essential living costs limit your safe debt capacity to ₹{safe:,.0f}."
        )
        recommendation = (
            f"Use Your Safe Limit (₹{safe:,.0f}): Do NOT take the lender's full sanction of ₹{lender:,.0f}. "
            f"The bank formula ignores your rent and living expenses; taking the bank's maximum will wipe out your cash buffer."
        )
    else:
        why = (
            f"Why: Minimal fixed living expenses and low ongoing debt allow your safe borrowing capacity to match "
            f"the maximum standard banking sanction limit."
        )
        recommendation = f"Use the Lender Sanction Limit (₹{lender:,.0f}): Your income and buffers comfortably support this capacity."

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
            f"Why: Pledging an unencumbered shop/property shifts your product to Loan Against Property (LAP), "
            f"reducing the interest band from standard 18%+ unsecured business rates down to {rate_min}%–{rate_max}%."
        )
    if "informal" in category.lower() or "gig" in category.lower():
        if profile.get("is_ev_vehicle") or "ev" in str(profile.get("loan_purpose", "")).lower():
            return (
                f"Why: Platform transaction logs and commercial EV hypothecation unlock priority-sector rates of "
                f"{rate_min}%–{rate_max}%, replacing predatory digital app debt charging over 30% APR."
            )
        return (
            f"Why: Priority micro-credit benchmarks set your fair rate band at {rate_min}%–{rate_max}%, "
            f"far below predatory payday lending apps."
        )
    if "750" in cibil_str or (isinstance(cibil, (int, float)) and cibil >= 750):
        return (
            f"Why: Your 750+ CIBIL and Tier-1 employer qualify you for the prime corporate band ({rate_min}%–{rate_max}%), "
            f"while a {pf_pct}% processing fee plus statutory 18% GST sets your true all-in APR at {apr}%."
        )
    if calculated.get("is_cibil_unknown"):
        return (
            f"Why: A wider rate band of {rate_min}%–{rate_max}% is applied because your credit history is unverified, "
            f"ensuring transparency without penalizing you as a defaulter (Rule 3: Unknown is never zero)."
        )
    return (
        f"Why: Standard credit risk adjustments for debt utilization and tenure set your fair rate band at "
        f"{rate_min}%–{rate_max}% with an all-in APR of {apr}%."
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
            f"Why: Household essential costs and existing debt leave only ₹{safe_cap:,.0f} surplus; "
            f"clearing active app debt and arrears must precede taking on new loan commitments."
        )
    if stress_results.get("was_adjusted"):
        return (
            f"Why: Under a 20% income downturn, an EMI above ₹{safe_cap:,.0f} would consume over 65% of your remaining "
            f"cash flow, so the monthly ceiling was adjusted downward to protect you from insolvency."
        )
    if profile.get("seasonal_variance_high") or "self" in category.lower():
        return (
            f"Why: Because retail enterprises experience seasonal revenue fluctuations, your safe ceiling of "
            f"₹{safe_cap:,.0f}/mo is anchored strictly to your lowest earning trough months."
        )
    if safe_cap < lender_emi:
        return (
            f"Why: While bank FOIR rules allow up to ₹{lender_emi:,.0f}/month, your monthly rent of ₹{rent:,.0f} "
            f"and living expenses cap your safe payment at ₹{safe_cap:,.0f} to protect your living buffer."
        )
    return (
        f"Why: Capped at ₹{safe_cap:,.0f}/month because regulatory guidelines prevent total monthly debt repayments "
        f"from exceeding your allowable income headroom."
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
