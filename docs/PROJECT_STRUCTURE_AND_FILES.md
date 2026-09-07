# PROJECT FILE MAP & SYSTEM COMPONENT BREAKDOWN

> **Document:** `PROJECT_STRUCTURE_AND_FILES.md`  
> **Purpose:** Detailed directory tree, granular responsibilities, input/output contracts, and cross-file execution flows for the Borrower Copilot codebase.  
> **Status:** Architecture Approved — File Map Specification

---

## 1. COMPLETE DIRECTORY TREE

Below is the complete file and directory layout required to build, test, and run the Borrower Copilot application:

```
lending-copilot/
│
├── ARCHITECTURE_AND_SPECIFICATION.md   # Master technical blueprint & mathematical spec
├── PROJECT_STRUCTURE_AND_FILES.md      # This file: Comprehensive file map & component breakdown
├── RULES.md                            # Deliverable 2: Complete rule, threshold, and source registry
├── WALKTHROUGH.md                      # Deliverable 4: 5-minute technical & design walkthrough
├── README.md                           # Quickstart guide, persona run-throughs, and setup instructions
├── requirements.txt                    # Python runtime dependencies
│
├── app.py                              # Deliverable 1: Interactive presentation layer & UI entrypoint
│
├── engine/                             # Core Deterministic Underwriting Engine (Zero DB / Zero API)
│   ├── __init__.py                     # Package interface exporting primary calculation APIs
│   ├── underwriting.py                 # Financial mathematics: PMT, PV, Newton-Raphson APR, FOIR, Limits, Stress
│   ├── confidence.py                   # Master question matrix, category branching, confidence scoring (60%-95%)
│   ├── explanations.py                 # Deterministic bottleneck priority trees & Rule 4 "Why" generators
│   └── negotiation.py                  # Tactical Negotiation Card compiler & verbatim counter-script generator
│
└── tests/                              # Automated Verification Suite
    ├── __init__.py                     # Test suite package initializer
    └── test_personas.py                # Deliverable 3: Automated test vectors for Priya, Ravi, and Anita
```

---

## 2. GRANULAR FILE SPECIFICATIONS & RESPONSIBILITIES

---

### `app.py`
* **Type:** Python Presentation Layer (Interactive Web Application)
* **Primary Role:** Entry point for the user interface. It renders the mobile-first terminal interface, handles user session state, manages dynamic conditional question flows, and visualizes calculations produced by the `engine/` package.
* **Key Responsibilities:**
  1. **One-Click Persona Quick-Loaders:** Provides buttons to instantly populate the form with canonical test profiles:
     - `Priya (Salaried MNC Professional)`
     - `Ravi (Self-Employed Kirana Store Owner)`
     - `Anita (Informal Delivery Fleet Partner)`
     - `Custom / Blank Profile`
  2. **Adaptive Two-Tier Questionnaire Wizard:**
     - Renders the 10 Universal Mandatory inputs ($M_{01} - M_{10}$).
     - Dynamically reveals the relevant category-specific variable questions ($S_{01}-S_{18}$ for Salaried, $B_{01}-B_{18}$ for MSME, or $I_{01}-I_{18}$ for Informal) based on the employment type chosen in $M_{04}$.
     - Hides irrelevant questions automatically without page reload.
  3. **Live Confidence Progress Gauge:**
     - Displays an animated visual meter scaling from `0%` $\rightarrow$ `60.0%` (after 10 mandatory questions) $\rightarrow$ up to `95.0%` as variable questions are answered.
     - Displays real-time tooltips explaining how additional answers tighten rate and capacity bands.
  4. **The Four Paired Output Cards ($O_1$ to $O_4$):**
     - Renders **Card 1 ($O_1$)**: Large recommendation verdict badge (`BORROW`, `BORROW LESS`, or `DON'T BORROW`) + single-sentence "Why".
     - Renders **Card 2 ($O_2$)**: Side-by-side comparison of **Lender Maximum Sanction** vs. **Borrower Safe Limit** with clear directive on **Which One to Use**.
     - Renders **Card 3 ($O_3$)**: Fair interest rate band ($r_{\min}\% - r_{\max}\%$) + All-In APR badge disclosing fee drag and statutory GST.
     - Renders **Card 4 ($O_4$)**: Safe monthly EMI ceiling + interactive **Tenure Trade-Off Table** (24m, 36m, 48m, 60m) + dual stress-test shock results ($-20\%$ income, $+2.0\%$ rate).
  5. **Mobile Negotiation Card:**
     - Displays a high-contrast, mobile-optimized card containing Target Anchors, Borrower Leverage Points, Bank Traps to Decline, and the Verbatim Spoken Script with a one-click `[Copy Script]` button.
* **Dependencies:** `streamlit`, `engine.underwriting`, `engine.confidence`, `engine.explanations`, `engine.negotiation`.

---

### `engine/__init__.py`
* **Type:** Python Package Interface
* **Primary Role:** Exposes a clean, unified API surface from the underlying engine modules.
* **Key Exports:**
  - `run_full_underwriting(profile: dict) -> UnderwritingResult`
  - `calculate_confidence(profile: dict) -> ConfidenceResult`
  - `build_negotiation_card(profile: dict, calculated: dict) -> NegotiationCard`

---

### `engine/underwriting.py`
* **Type:** Core Financial Mathematics & Deterministic Logic
* **Primary Role:** Contains all quantitative calculations, amortization formulas, regulatory ratio benchmarks, and macroeconomic stress simulations.
* **Key Responsibilities & Functions:**
  1. `calculate_pmt(rate_annual: float, n_months: int, principal: float) -> float`:
     - Computes monthly installment using standard loan amortization:
       $$\text{EMI} = \frac{P \times r \times (1 + r)^n}{(1 + r)^n - 1}$$
  2. `calculate_present_value(rate_annual: float, n_months: int, emi: float) -> float`:
     - Reverses EMI into maximum borrowable principal:
       $$\text{Principal} = \frac{\text{EMI} \times [1 - (1 + r)^{-n}]}{r}$$
  3. `solve_all_in_apr(principal: float, emi: float, n_months: int, processing_fee_pct: float, doc_charges: float) -> float`:
     - Calculates upfront fee deductions including statutory 18% GST:
       $$\text{Fees} = (P \times \text{Fee}_{\%} \times 1.18) + \text{Doc Charges}$$
       $$\text{Net Disbursed} = P - \text{Fees}$$
     - Solves for the annualized Internal Rate of Return (IRR) via a 50-step Newton-Raphson root-finding algorithm.
  4. `calculate_lender_max_sanction(income: float, foir_pct: float, existing_emi: float, rate_annual: float, n_months: int, collateral_value: float = 0.0) -> tuple[float, float]`:
     - Computes maximum allowable bank EMI under regulatory FOIR caps (50%–55% for Salaried, 45% for MSME, 40% for Informal).
     - Caps sanction by 50%–55% LTV if unencumbered property collateral is pledged (LAP).
  5. `calculate_borrower_safe_capacity(income: float, existing_emi: float, rent: float, living_expenses: float, liquid_runway_months: float, productive_income_boost: float = 0.0, rate_annual: float = 11.0, n_months: int = 48) -> tuple[float, float]`:
     - Computes real disposable cash flow after shelter, essential groceries/utilities, and liquid emergency reserves (5% if runway $\ge 6$ mos, else 10%).
  6. `run_dual_stress_test(income: float, existing_emi: float, requested_principal: float, base_rate: float, n_months: int) -> dict`:
     - Simulates an immediate 20% drop in net take-home earnings ($I_{\text{stress}} = I_{\text{net}} \times 0.80$).
     - Simulates a +2.0% rate spike on floating debt ($r_{\text{stress}} = r + 2.0\%$).
     - Tests against the **65% distress ratio ceiling** and iteratively ratchets down the monthly ceiling if breached.
  7. `evaluate_verdict(profile: dict, calculated: dict) -> str`:
     - Executes strict 3-tier hierarchical triage:
       - **Tier 1 (Distress / Kill-Switch):** Auto-debit bounce $\ge 1$, digital app loans $>24\%$ APR, or safe cash $\le 0$ $\rightarrow$ `DON'T BORROW`.
       - **Tier 2 (Capacity Over-Leverage):** Requested EMI $>$ safe ceiling or requested principal $>$ safe limit $\rightarrow$ `BORROW LESS`.
       - **Tier 3 (Affordability Clearance):** Stressed debt ratio $\le 65\%$ and all buffers intact $\rightarrow$ `BORROW`.
* **Dependencies:** Python native `math`, `typing`.

---

### `engine/confidence.py`
* **Type:** Question Parameter Matrix & Confidence Engine
* **Primary Role:** Tracks question completion, maps the 104-row parameter lookup table, manages dynamic category filtering, and computes the live confidence score.
* **Key Responsibilities & Functions:**
  1. `MASTER_QUESTIONS`:
     - Data dictionary encoding the 10 Universal Mandatory questions ($M_{01} - M_{10}$) and 54 Category Variable questions ($S_{01}–S_{18}$, $B_{01}–B_{18}$, $I_{01}–I_{18}$).
     - Records question ID, category, label, input type, options, default values, confidence point weight, and underwriting logic moved.
  2. `compute_confidence_score(answered_keys: list[str], category: str) -> float`:
     - Evaluates base 60.0% confidence upon completion of $M_{01} - M_{10}$.
     - Sums calibrated variable gains ($+1.0\%$ to $+4.0\%$ per question) up to the strict **95.0% maximum cap**.
  3. `get_spread_half_width(confidence_score: float) -> float`:
     - Dynamically contracts the uncertainty spread as confidence increases:
       $$\text{Half-Width} = 2.0\% \times \left(1 - \frac{\text{Confidence} - 60\%}{35\%}\right) + 0.35\%$$
       *(Wide spread of $\pm 2.35\%$ at 60% confidence tightens down to $\pm 0.35\%$ at 95% confidence).*
* **Dependencies:** Python native `typing`, `dataclasses`.

---

### `engine/explanations.py`
* **Type:** Deterministic Bottleneck Priority Trees & Rule 4 "Why" Formulators
* **Primary Role:** Generates the exact, single-sentence plain-English diagnostic explaining why each number stops where it does, satisfying Rule 4: *"Every number has a why"*.
* **Key Responsibilities & Functions:**
  1. `explain_verdict(profile: dict, calculated: dict) -> str`:
     - Evaluates active kill-switch reasons (bounces, high-interest apps), cash deficits, or over-leverage gaps, and formats the active reason.
  2. `explain_borrowing_limits(profile: dict, calculated: dict) -> tuple[str, str]`:
     - Explains the disparity between bank gross FOIR allowances and real household disposable surplus.
     - Formulates the directive on **which limit the borrower should use** (protecting living buffers).
  3. `explain_rate_band(profile: dict, calculated: dict) -> str`:
     - Identifies the primary spread driver: property collateral pivot, 750+ prime CIBIL tier, unscored bureau uncertainty, or high credit utilization.
  4. `explain_monthly_ceiling(profile: dict, calculated: dict) -> str`:
     - Identifies whether the monthly payment ceiling was bounded by high urban rent/living costs, regulatory 50% FOIR caps, or the 20% stress test shock.
* **Dependencies:** Python native `typing`.

---

### `engine/negotiation.py`
* **Type:** Tactical Counter-Benchmark & Script Generator
* **Primary Role:** Generates the in-branch Negotiation Card, compiling target anchors, borrower leverage points, bank traps to decline, and a word-for-word spoken counter-script.
* **Key Responsibilities & Functions:**
  1. `identify_target_product(profile: dict) -> str`:
     - Selects the optimal credit product (Prime Corporate Personal Loan, Loan Against Property / LAP, Commercial EV Asset Loan, or Micro-Credit).
  2. `extract_borrower_leverage(profile: dict, calculated: dict) -> list[str]`:
     - Mines profile for strong negotiation assets: CIBIL $\ge 750$, 5+ years employer tenure, unencumbered real estate, low existing FOIR ($<20\%$), or liquid emergency runway $\ge 6$ months.
  3. `identify_bank_traps(profile: dict, calculated: dict) -> list[str]`:
     - Identifies predatory terms to refuse: bundled single-premium insurance deducted from disbursement, processing fee markups above 1.0% + GST, and foreclosure lock-in periods $>12$ months.
  4. `compile_spoken_script(target_product: str, leverage_point: str, rate_min: float, rate_max: float, all_in_apr: float, safe_emi: float, fee_cap: str) -> str`:
     - Assembles the word-for-word conversational counter-statement for the borrower to read to the loan officer.
* **Dependencies:** Python native `typing`.

---

### `RULES.md`
* **Type:** Core Deliverable #2 (Underwriting Rulebook & Assumptions Registry)
* **Primary Role:** A comprehensive, formal markdown table read alongside the code. It catalogues every rule, threshold, product band, and assumption used across the engine.
* **Table Structure:**
  - `Parameter / Rule Name`: The exact underwriting parameter (e.g., `Salaried FOIR Cap`, `Distress Ratio Ceiling`, `Unknown CIBIL Spread`).
  - `Assigned Value`: The exact numeric or conditional value (e.g., `55%`, `65%`, `±2.0%`).
  - `Why (Financial Reasoning)`: The economic and risk rationale protecting the borrower.
  - `Source / Attribution`: Origin tag (e.g., `RBI Retail Lending Circular 2023`, `SBI Personal Loan Master Policy`, `Statutory CGST+SGST Rule`, or `Author's Domain Judgement`).
  - `Honesty Disclosure`: States where the model is estimating versus calculating from codified law.

---

### `WALKTHROUGH.md`
* **Type:** Core Deliverable #4 (5-Minute Technical & Design Walkthrough)
* **Primary Role:** A structured written walkthrough of the application architecture, design decisions, trade-offs, and forward roadmap.
* **Key Sections:**
  1. **Architecture Overview:** Explanation of the decoupled engine/presentation pattern.
  2. **How the Five Challenge Rules Were Enforced:** Detailed code walkthrough of Adaptive Branching, Confidence Progression, Non-Zero Unknowns, Rule 4 "Why" Generation, and Indian Benchmark Integration.
  3. **Verification of the Three Personas:** Demonstration of results for Priya, Ravi, and Anita.
  4. **What to Build Next:** Features for Version 2.0 (e.g., automated bank statement PDF OCR parser, vernacular language support in Hindi/Kannada, and lender quote comparator).
  5. **What to Cut:** Unnecessary complexity eliminated to preserve simplicity (e.g., external database dependencies, multi-page routing, heavy CSS frameworks).

---

### `README.md`
* **Type:** Core Repository Guide & 5-Minute Quickstart
* **Primary Role:** Provides clear, step-by-step instructions for judges and developers to run the application locally in under 5 minutes.
* **Key Sections:**
  1. One-line local installation command (`pip install -r requirements.txt`).
  2. One-line local execution command (`streamlit run app.py`).
  3. Quick-start walkthrough of the four outputs and the Negotiation Card.
  4. Summary of the three verified test personas with expected figures.

---

### `requirements.txt`
* **Type:** Dependency Configuration
* **Primary Role:** Minimal dependency list ensuring clean local execution.
* **Contents:**
  ```text
  streamlit>=1.30.0
  ```

---

### `tests/test_personas.py`
* **Type:** Core Deliverable #3 (Automated Unit & Persona Test Suite)
* **Primary Role:** Contains automated Python unit tests that execute the exact canonical test profiles for Priya, Ravi, and Anita, asserting that outputs match expected benchmarks.
* **Test Cases:**
  1. `test_persona_priya_salaried()`:
     - Asserts: $O_1 = \text{BORROW}$, Lender Sanction $\approx \text{₹18.1L}$, Safe Limit $\approx \text{₹14.6L}$, Fair Rate Band $\approx 10.5\% - 11.25\%$, All-In APR $\approx 11.65\%$, Safe Monthly Ceiling $\approx \text{₹37,500/mo}$, Stress Test $=$ PASS.
  2. `test_persona_ravi_self_employed()`:
     - Asserts: Unencumbered shop pivots to LAP, $O_1 = \text{BORROW}$, Lender LAP Sanction $\approx \text{₹22.5L}$, Safe Limit $\approx \text{₹21.0L}$, Fair Rate Band $\approx 9.75\% - 10.50\%$, Safe Monthly Ceiling $\approx \text{₹42,500/mo}$ (monsoon anchor).
  3. `test_persona_anita_informal()`:
     - Asserts: Auto-debit bounce $\ge 1$ and app loans $>30\%$ APR fire kill-switch, $O_1 = \text{DON'T BORROW}$, Lender & Safe Sanctions $= \text{₹0}$ (Blocked), Safe Ceiling $\approx \text{₹3,500/mo}$ pre-restructuring.
  4. `test_rule_unknown_never_zero()`:
     - Validates that unverified credit score widens spread by $\pm 2.0\%$ without altering median.
  5. `test_rule_confidence_progression()`:
     - Validates that confidence starts at 60.0% for mandatory inputs and scales up to 95.0% max.
* **Execution:** Run via `python -m unittest tests/test_personas.py`.

---

## 3. COMPONENT COLLABORATION & EXECUTION FLOW

```
                          [User Interacts with app.py]
                                       │
            ┌──────────────────────────┴──────────────────────────┐
            │ 1. Selects Persona (Priya/Ravi/Anita) or Custom     │
            │ 2. Fills Mandatory (M01-M10) + Variable Questions   │
            └──────────────────────────┬──────────────────────────┘
                                       │
                                       ▼ (Calls Engine API)
            ┌─────────────────────────────────────────────────────┐
            │ engine.confidence.compute_confidence_score()        │
            │ -> Evaluates answered keys against 104-row matrix   │
            │ -> Returns confidence % (60.0% to 95.0%)            │
            │ -> Determines uncertainty spread width (±0.35%-2.0%)│
            └──────────────────────────┬──────────────────────────┘
                                       │
                                       ▼
            ┌─────────────────────────────────────────────────────┐
            │ engine.underwriting.run_full_underwriting()         │
            │ -> Computes Product Rate Band (O3)                  │
            │ -> Solves True All-In APR via Newton-Raphson (O3)   │
            │ -> Computes Lender Sanction via FOIR (O2)           │
            │ -> Computes Borrower Safe Limit via Cash-Flow (O2)  │
            │ -> Simulates -20% Income & +2.0% Rate Shock (O4)    │
            │ -> Binds Monthly Ceiling to 65% Distress Line (O4)  │
            │ -> Evaluates 3-Tier Verdict Triage (O1)             │
            └──────────────────────────┬──────────────────────────┘
                                       │
                                       ▼
            ┌─────────────────────────────────────────────────────┐
            │ engine.explanations.generate_all_explanations()     │
            │ -> Evaluates Bottleneck Priority Tree for O1        │
            │ -> Evaluates Bottleneck Priority Tree for O2        │
            │ -> Generates "Which One to Use" Guidance for O2     │
            │ -> Evaluates Bottleneck Priority Tree for O3        │
            │ -> Evaluates Bottleneck Priority Tree for O4        │
            └──────────────────────────┬──────────────────────────┘
                                       │
                                       ▼
            ┌─────────────────────────────────────────────────────┐
            │ engine.negotiation.build_negotiation_card()         │
            │ -> Assigns Target Anchors (Product, Rate, APR, EMI) │
            │ -> Extracts Borrower Leverage Bullets               │
            │ -> Identifies Bank Traps & Predatory Fees to Reject │
            │ -> Compiles Verbatim Spoken Counter-Script          │
            └──────────────────────────┬──────────────────────────┘
                                       │
                                       ▼
                     [UI Renders Complete Results in app.py]
            - Live Confidence Progress Bar (60.0% to 95.0%)
            - 4 Two-Fold Cards (Fold 1: Metric | Fold 2: Why)
            - Interactive Tenure Trade-Off Comparison Matrix
            - Mobile-Ready High-Contrast Negotiation Card
```

---

*End of Project File Map & System Component Breakdown.*
