"""
Deterministic Underwriting Engine for Borrower Copilot.
Pure Python package executing financial math, confidence tracking, explanations, and negotiation generation.
"""

from .underwriting import (
    calculate_pmt,
    calculate_present_value,
    solve_all_in_apr,
    calculate_lender_max_sanction,
    calculate_borrower_safe_capacity,
    run_dual_stress_test,
    evaluate_verdict,
    run_full_underwriting,
)

from .confidence import (
    compute_confidence_score,
    get_spread_half_width,
    get_questions_for_category,
    MASTER_QUESTIONS,
)

from .explanations import (
    generate_all_explanations,
    explain_verdict,
    explain_borrowing_limits,
    explain_rate_band,
    explain_monthly_ceiling,
)

from .negotiation import (
    build_negotiation_card,
)

__all__ = [
    "calculate_pmt",
    "calculate_present_value",
    "solve_all_in_apr",
    "calculate_lender_max_sanction",
    "calculate_borrower_safe_capacity",
    "run_dual_stress_test",
    "evaluate_verdict",
    "run_full_underwriting",
    "compute_confidence_score",
    "get_spread_half_width",
    "get_questions_for_category",
    "MASTER_QUESTIONS",
    "generate_all_explanations",
    "explain_verdict",
    "explain_borrowing_limits",
    "explain_rate_band",
    "explain_monthly_ceiling",
    "build_negotiation_card",
]
