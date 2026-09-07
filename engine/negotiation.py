"""
engine/negotiation.py
Tactical Negotiation Card Engine: Target Anchors, Borrower Leverage, Bank Traps,
and Dynamic In-Branch Verbatim Spoken Counter-Script Generator.
"""

from typing import Dict, Any, List


def build_negotiation_card(profile: Dict[str, Any], calculated: Dict[str, Any]) -> Dict[str, Any]:
    """
    Builds the complete Negotiation Card payload for in-branch negotiation.
    """
    leverage_points: List[str] = []
    traps_to_reject: List[str] = []

    target_product = calculated.get("target_product", "Prime Personal Loan")
    rate_min = calculated.get("rate_min", 10.5)
    rate_max = calculated.get("rate_max", 11.25)
    apr = calculated.get("all_in_apr", 11.65)
    safe_emi = float(calculated.get("monthly_safe_ceiling", 0.0))
    processing_fee_pct = calculated.get("processing_fee_pct", 1.0)
    category = profile.get("employment_type", "Salaried")
    cibil = profile.get("cibil", "Unknown")
    cibil_str = str(cibil).strip()

    # -------------------------------------------------------------
    # 1. Product Routing & Rate Rationale
    # -------------------------------------------------------------
    if calculated.get("is_lap"):
        prop_val = float(profile.get("property_market_value", 0))
        rate_rationale = f"pledging an unencumbered commercial/residential property valued at ₹{prop_val:,.0f}"
        max_fee_cap = "1.0% + GST"
    elif "informal" in category.lower() or "gig" in category.lower():
        rate_rationale = "priority sector commercial asset financing with proven digital payout records"
        max_fee_cap = "1.5% + GST"
    else:
        rate_rationale = f"verified employment stability and strong debt-service headroom"
        max_fee_cap = "1.0% + GST"

    # -------------------------------------------------------------
    # 2. Dynamic Borrower Leverage Extraction
    # -------------------------------------------------------------
    # CIBIL leverage
    if "750" in cibil_str or (isinstance(cibil, (int, float)) and cibil >= 750):
        leverage_points.append("Credit score of 750+ qualifies for the bank's lowest Tier-1 prime pricing bracket.")
    elif "unknown" in cibil_str.lower() or "unscored" in cibil_str.lower():
        leverage_points.append("Demonstrated positive operating cash flow offsets unscored bureau standing.")

    # Collateral leverage
    if calculated.get("is_lap"):
        leverage_points.append("100% unencumbered real estate provides absolute security, removing unsecured risk premiums.")

    # Employment & Vintage leverage
    job_vintage = float(profile.get("job_vintage_years", 0))
    biz_vintage = float(profile.get("business_vintage_years", 0))
    if job_vintage >= 3.0:
        leverage_points.append(f"Over {job_vintage:.0f} years of continuous tenure with current corporate employer.")
    elif biz_vintage >= 5.0:
        leverage_points.append(f"Over {biz_vintage:.0f} years of established operational stability at current retail location.")

    # Cash Reserve leverage
    savings_runway = float(profile.get("liquid_savings_months", 0))
    if savings_runway >= 6.0:
        leverage_points.append(f"Holding {savings_runway:.0f} months of liquid emergency runway eliminates repayment default risk.")

    # Co-applicant / Family leverage
    co_inc = float(profile.get("co_applicant_income", 0)) or float(profile.get("co_applicant_income_msme", 0))
    if co_inc > 0:
        leverage_points.append(f"Verified secondary co-applicant income of ₹{co_inc:,.0f}/month strengthens total repayment capacity.")

    # Productive Utility leverage
    prod_boost = float(profile.get("productive_income_boost", 0))
    if prod_boost > 0:
        leverage_points.append(f"Asset directly generates ₹{prod_boost:,.0f}/month in incremental operating cash flow.")

    if not leverage_points:
        leverage_points.append("Documented verifiable monthly income leaves sufficient disposable surplus for debt service.")

    # -------------------------------------------------------------
    # 3. Dynamic Trap Warning Extraction
    # -------------------------------------------------------------
    # Single-premium credit insurance bundling (universal retail lending trap)
    traps_to_reject.append("DECLINE mandatory single-premium credit life or loan-shield insurance deducted from disbursement.")
    
    # Excessive fee drag
    traps_to_reject.append(f"REFUSE processing fees exceeding {max_fee_cap}.")

    # Unsecured vs Secured divergence
    if calculated.get("is_lap"):
        traps_to_reject.append("DO NOT let the lender divert you to an express unsecured business loan at >16% APR.")

    # Digital app rollover trap
    bounces = int(profile.get("payment_bounces_6m", 0))
    app_loans = int(profile.get("active_app_loan_count", 0))
    if bounces >= 1 or app_loans >= 1:
        traps_to_reject.append("REJECT any new high-interest consumer credit prior to restructuring existing digital app debt.")

    # Prepayment penalties
    traps_to_reject.append("INSIST on zero foreclosure or part-prepayment penalty after 12 months as per RBI guidelines.")

    # -------------------------------------------------------------
    # 4. Verbatim Spoken Script Assembly
    # -------------------------------------------------------------
    primary_leverage = leverage_points[0] if leverage_points else "my verified income stability"

    if calculated.get("verdict") == "DON'T BORROW":
        spoken_script = (
            f"I have reviewed my credit position. Before taking on any new loan obligations, "
            f"I am prioritizing the consolidation and clearance of my active digital loan balances. "
            f"I will revisit new asset financing once my credit registry is clean."
        )
    else:
        spoken_script = (
            f"I am applying for a {target_product}. Based on {rate_rationale}, standard regulatory pricing "
            f"indicates a fair rate of {rate_min}% to {rate_max}%, with an all-in APR cap of {apr}%. "
            f"My monthly commitment ceiling is strictly ₹{safe_emi:,.0f}/month. "
            f"I will not accept structured tenures, fee markups above {max_fee_cap}, "
            f"or mandatory single-premium insurance add-ons that breach these limits."
        )

    return {
        "target_product": target_product,
        "fair_rate_band": f"{rate_min}% – {rate_max}%",
        "rate_min": rate_min,
        "rate_max": rate_max,
        "all_in_apr": apr,
        "monthly_safe_ceiling": safe_emi,
        "processing_fee_cap": max_fee_cap,
        "leverage_points": leverage_points,
        "traps_to_reject": traps_to_reject,
        "spoken_script": spoken_script
    }
