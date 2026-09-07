# MASTER ARCHITECTURE & SPECIFICATION PLAN: BORROWER COPILOT
## Autonomous Underwriting Engine, Evaluation Rubric Mapping & Implementation Blueprint

> **Challenge:** Lokta · Borrower Copilot Take-Home Challenge (Version 1.0)  
> **Target Audience:** Underwriting Evaluators, Product Judges, and Engineering Agent  
> **Core Mandate:** A zero-database, zero-API, client-deterministic personal borrowing assistant for Indian retail borrowers. It answers the four core borrowing questions before a borrower walks into a lending institution and equips them with an in-branch Negotiation Card.

---

## TABLE OF CONTENTS
1. [Challenge Deconstruction & Scoring Rubric Alignment](#1-challenge-deconstruction--scoring-rubric-alignment)
2. [The Four Core Outputs ($O_1$ to $O_4$) & Product Standards](#2-the-four-core-outputs-o_1-to-o_4--product-standards)
3. [The Five Codified Underwriting Rules](#3-the-five-codified-underwriting-rules)
4. [System Architecture & Technology Stack](#4-system-architecture--technology-stack)
5. [Borrower Taxonomy & Persona Archetypes](#5-borrower-taxonomy--persona-archetypes)
6. [Master Question Matrix & Confidence Progression Engine](#6-master-question-matrix--confidence-progression-engine)
7. [Mathematical Formulas & Underwriting Core](#7-mathematical-formulas--underwriting-core)
   - [7.1 Output 3 ($O_3$): Fair Interest Rate Band & All-In APR (IRR)](#71-output-3-o_3-fair-interest-rate-band--all-in-apr-irr)
   - [7.2 Output 2 ($O_2$): Two-Sided Borrowing Limits & "Which to Use"](#72-output-2-o_2-two-sided-borrowing-limits--which-to-use)
   - [7.3 Output 4 ($O_4$): Monthly Payment Ceiling, Tenure Trade-Off & Dual Stress Shock](#73-output-4-o_4-monthly-payment-ceiling-tenure-trade-off--dual-stress-shock)
   - [7.4 Output 1 ($O_1$): Three-Tier Recommendation Verdict Engine](#74-output-1-o_1-three-tier-recommendation-verdict-engine)
8. [The "Every Number Has a Why" Diagnostic Engine](#8-the-every-number-has-a-why-diagnostic-engine)
9. [The Mobile Negotiation Card & In-Branch Script Engine](#9-the-mobile-negotiation-card--in-branch-script-engine)
10. [End-to-End Canonical Persona Run-Throughs (Priya, Ravi, Anita)](#10-end-to-end-canonical-persona-run-throughs-priya-ravi-anita)
11. [Honesty About Limits & Guessing Transparency](#11-honesty-about-limits--guessing-transparency)
12. [UI/UX Layout, Visual Hierarchy & Interactive Components](#12-uiux-layout-visual-hierarchy--interactive-components)
13. [Deliverables Mapping & Implementation Roadmap](#13-deliverables-mapping--implementation-roadmap)

---

## 1. CHALLENGE DECONSTRUCTION & SCORING RUBRIC ALIGNMENT

The Lokta Borrower Copilot challenge evaluates whether institutional lending judgement can be codified into deterministic rules that a borrower can understand and a computer can run. The evaluation rubric allocates 100 points across six core dimensions:

```
+-----------------------------------------------------------------------------------------+
|                                SCORING RUBRIC BREAKDOWN                                 |
+------------------------------+--------+-------------------------------------------------+
| Evaluation Area              | Points | How This Specification & App Directly Solves It |
+------------------------------+--------+-------------------------------------------------+
| 1. Domain Reasoning          | 30 pts | - Lender sanction and borrower safe limit are   |
|                              |        |   clearly separated via FOIR vs. Cash Flow math.|
|                              |        | - Explicit advice on WHICH limit to use.        |
|                              |        | - "Don't Borrow" kill-switch fires on bounces,  |
|                              |        |   >24% predatory app debt, or zero cash surplus.|
|                              |        | - Product pivot: Ravi routes from 18%+ unsecured|
|                              |        |   to 9.75% LAP using unencumbered shop property.|
|                              |        | - All-In APR solves true IRR including GST (18%)|
|                              |        |   and upfront processing fee drag.              |
+------------------------------+--------+-------------------------------------------------+
| 2. Question Design           | 20 pts | - 10 Universal Must questions establish 60% base|
|                              |        | - 18 Adaptive category questions (S01-S18,      |
|                              |        |   B01-B18, I01-I18) move exact numbers & ranges.|
|                              |        | - Adaptive branching: Salaried IT vs Kirana     |
|                              |        |   owner see completely customized question sets.|
|                              |        | - "Unknown" inputs widen bands without defaults.|
+------------------------------+--------+-------------------------------------------------+
| 3. Explainability & The Card | 20 pts | - Rule 4 enforced: Every output carries a single|
|                              |        |   diagnostic plain-English sentence below it.   |
|                              |        | - Standalone mobile-ready Negotiation Card with |
|                              |        |   Target Anchors, Leverage, Traps, and a        |
|                              |        |   verbatim spoken counter-script for branches.  |
+------------------------------+--------+-------------------------------------------------+
| 4. Product Craft             | 15 pts | - Responsive mobile-first terminal UI (375-430px|
|                              |        |   optimized, also stunning on desktop).         |
|                              |        | - Live visual confidence meter (60.0% to 95.0%).|
|                              |        | - Ranges shown as explicit visual bands.        |
|                              |        | - One-click quick-loaders for Priya, Ravi, Anita|
+------------------------------+--------+-------------------------------------------------+
| 5. Engineering               | 10 pts | - Pure decoupled architecture: mathematical     |
|                              |        |   engine in `engine/`, presentation in `app.py`.|
|                              |        | - Zero DB, zero external API, runs in < 5 mins. |
|                              |        | - Fully covered by unit tests in `test_personas`|
+------------------------------+--------+-------------------------------------------------+
| 6. Honesty About Limits      | 5 pts  | - Clear UI flags identifying where the model is |
|                              |        |   making assumptions vs. verified calculations. |
|                              |        | - Formal `RULES.md` documenting what we assume, |
|                              |        |   what we do not know, and regulatory origins.  |
+------------------------------+--------+-------------------------------------------------+
```

---

## 2. THE FOUR CORE OUTPUTS ($O_1$ TO $O_4$) & PRODUCT STANDARDS

The HTML brief mandates four primary outputs, followed by the mobile Negotiation Card. Every output must meet strict "what good looks like" criteria:

```
                                  [USER RESPONSES]
                                         │
                 ┌───────────────────────┴───────────────────────┐
                 ▼                                               ▼
     [LENDER'S PERSPECTIVE]                           [BORROWER'S PERSPECTIVE]
    - Regulatory FOIR (40% - 55%)                    - Actual Take-Home Income
    - Max Gross EMI Sanction                         - Fixed Shelter (Rent / Housing)
    - Unsecured Product Pricing                      - Non-Negotiable Living Costs Floor
    - Upfront Fee Deductions                         - Emergency Liquidity Reserve (5% - 10%)
                 │                                   - Asset Collateral Backing (LAP Pivot)
                 │                                   - Dual Stress Shock (-20% Income, +2% Rate)
                 │                                               │
                 └───────────────────────┬───────────────────────┘
                                         ▼
   ┌─────────────────────────────────────────────────────────────────────────────┐
   │                    THE FOUR TWO-FOLD OUTPUT CARDS                           │
   ├─────────────────────────────────────────────────────────────────────────────┤
   │ O1: THE VERDICT               │ "BORROW", "BORROW LESS", or "DON'T BORROW"  │
   │                               │ + Single-sentence bottleneck reason         │
   ├───────────────────────────────┼─────────────────────────────────────────────┤
   │ O2: MAXIMUM AMOUNT (2-SIDED)  │ Lender Sanction vs. Borrower Safe Limit     │
   │                               │ + Explicit directive on WHICH ONE TO USE    │
   ├───────────────────────────────┼─────────────────────────────────────────────┤
   │ O3: FAIR INTEREST RATE & APR  │ Market Rate Band (%) + All-In APR (with GST)│
   │                               │ + Fee drag disclosure to evaluate quotes   │
   ├───────────────────────────────┼─────────────────────────────────────────────┤
   │ O4: MONTHLY PAYMENT CEILING   │ Safe EMI Cap + Tenure Trade-off Matrix      │
   │                               │ + Dual Stress Shock Resilience (-20% / +2%) │
   ├───────────────────────────────┴─────────────────────────────────────────────┤
   │                                     ▼                                       │
   │                      THE MOBILE NEGOTIATION CARD                            │
   │          [Target Anchors | Leverage Points | Bank Traps | Spoken Script]    │
   └─────────────────────────────────────────────────────────────────────────────┘
```

### Output Breakdown:
* **$O_1$ (Recommendation Verdict):** Must reach three legitimate states:
  1. `BORROW`: Safe cash flow comfortably covers the requested loan; zero distress triggers.
  2. `BORROW LESS`: The borrower has capacity, but the requested loan amount/EMI breaches safe cash flow or stress limits.
  3. `DON'T BORROW`: Mandatory kill-switch triggered by active debt bounces, predatory digital app debt ($>24\%$ APR), or zero disposable cash.
* **$O_2$ (Maximum Amount - Two-Sided):** Clearly displays two distinct numbers:
  1. **Lender Sanction Limit:** What an institutional bank algorithm will approve based on gross FOIR guidelines.
  2. **Borrower Safe Limit:** What the borrower can safely carry without risking default or exhausting living buffers.
  3. **Which to Use Directive:** Explicitly instructs the borrower to use $\min(\text{Lender}, \text{Borrower Safe})$ and explains why taking the bank's maximum is dangerous.
* **$O_3$ (Fair Interest Rate & True APR):** 
  - Expressed as a **band** ($r_{\min}\% - r_{\max}\%$), never an arbitrary single point.
  - Accompanied by the **True All-In APR** (annualized Internal Rate of Return equating net disbursed funds to monthly EMIs), factoring in upfront processing fees and 18% statutory GST.
* **$O_4$ (Monthly Payment Ceiling & Stress Resilience):**
  - Defines the non-negotiable monthly EMI ceiling.
  - Displays a **Tenure Trade-Off Table** (e.g., 24m vs 36m vs 48m vs 60m showing monthly payment vs total interest paid).
  - Explicitly stress-tests the payment against a simultaneous **20% income downturn** and a **+2.0% floating rate spike**, capping debt service at 65% of stressed income.
* **The Negotiation Card:** A one-screen mobile-optimized card displaying tactical counter-benchmarks, positive borrower leverage points, bank traps to decline, and a word-for-word spoken counter-script.

---

## 3. THE FIVE CODIFIED UNDERWRITING RULES

The system strictly enforces the five judging rules specified in the challenge HTML:

1. **Rule 1: Adaptive Architecture**  
   A salaried IT employee (Priya) and a kirana store merchant (Ravi) never see the same questionnaire. Selecting the employment type in $M_{04}$ instantly branches the workflow into specialized variable question modules (Salaried, Self-Employed/MSME, Informal/Gig). Questions that do not apply are hidden.
2. **Rule 2: Confidence Widens with Silence**  
   When only the mandatory questions are answered, output spreads remain wide ($\pm 2.0\%$ to $\pm 2.5\%$) and the confidence meter sits at **60.0%**. As each category question is answered, the confidence score climbs toward **95.0%**, and the rate/amount bands progressively tighten. The engine never narrows a band without an empirical input.
3. **Rule 3: Unknown is Never Zero**  
   If a borrower enters "Unknown / Unscored" for their credit score or property valuation, the engine does not default to zero or penalize them as a subprime defaulter ($300$). Instead, it models an unrated risk band ($\pm 2.0\%$ symmetric spread) and explicitly explains the consequence.
4. **Rule 4: Every Number Has a Why**  
   Every quantitative output ($O_1$ to $O_4$) is paired directly with a single plain-English sentence explaining which exact mathematical constraint, household expense, or regulatory policy bounded that number.
5. **Rule 5: Grounded in Indian Lending Realities**  
   Codifies RBI Priority Sector Lending (PSL) rules, standard Fixed Obligation to Income Ratios (FOIR: 40%–55%), statutory 18% GST on upfront bank fees, Loan Against Property (LAP) 50% LTV norms, and electric vehicle commercial financing benchmarks. All calculations use Indian Rupees (₹) with Lakh formatting.

---

## 4. SYSTEM ARCHITECTURE & TECHNOLOGY STACK

```
+-----------------------------------------------------------------------------+
|                            app.py (UI Layer)                                |
|  - Streamlit or Pure Web Interface (Mobile-First 375px - 430px Viewport)    |
|  - One-Click Persona Quick-Loaders (Priya, Ravi, Anita, Custom)             |
|  - Adaptive Question Wizard (Tier 1: Mandatory | Tier 2: Category Variable) |
|  - Live Confidence Progress Gauge (0% -> 60.0% -> 95.0% Max)                |
|  - Paired Two-Fold Output Cards (Fold 1: Metric | Fold 2: Qualitative Why)  |
|  - Interactive Tenure Trade-Off Slider / Amortization Visualizer            |
|  - Standalone High-Contrast Mobile Negotiation Card with [Copy Script]      |
+--------------------------------------^--------------------------------------+
                                       | Clean JSON Data Protocol
+--------------------------------------v--------------------------------------+
|                     engine/ (Pure Deterministic Python)                     |
|                                                                             |
|  +---------------------------+  +----------------------------------------+  |
|  | engine/underwriting.py    |  | engine/confidence.py                   |  |
|  | - PMT & PV Amortization   |  | - 104-Row Parameter Mapping Table      |  |
|  | - Newton-Raphson APR/IRR |  | - Live Confidence Gauge (60% to 95%)   |  |
|  | - FOIR & Sanction Limits  |  | - Adaptive Question Filtering          |  |
|  | - Residual Cash Flow Math |  | - Uncertainty Spread Tightener         |  |
|  | - 20% Dual Shock Engine   |  |                                        |  |
|  +---------------------------+  +----------------------------------------+  |
|  +---------------------------+  +----------------------------------------+  |
|  | engine/explanations.py    |  | engine/negotiation.py                  |  |
|  | - Bottleneck Priority Tree|  | - Target Anchor Synthesizer            |  |
|  | - Rule 4 Single-Sentence  |  | - Borrower Leverage Rule Evaluator     |  |
|  |   Diagnostic Generator    |  | - Trap & Predatory Fee Detector        |  |
|  | - "Which to Use" Logic    |  | - Spoken Counter-Script Interpolator   |  |
|  +---------------------------+  +----------------------------------------+  |
+-----------------------------------------------------------------------------+
```

### Architectural Guarantees:
- **Zero External Dependencies:** Native Python libraries (`math`, `typing`, `json`, `dataclasses`).
- **Zero Persistence:** Does not write borrower financial data to databases or send payloads to remote credit bureau APIs.
- **Fast Startup:** Runs locally via standard single-line commands in under 15 seconds.
- **Unit Tested:** Includes `tests/test_personas.py` validating expected calculations for Priya, Ravi, and Anita.

---

## 5. BORROWER TAXONOMY & PERSONA ARCHETYPES

The engine dynamically classifies applicants into 3 main sectors and 10 detailed sub-categories based on market underwriting behavior:

```
                               [Select Category (M04)]
                                          │
       ┌──────────────────────────────────┼──────────────────────────────────┐
       ▼                                  ▼                                  ▼
 ┌──────────────┐                  ┌──────────────┐                   ┌──────────────┐
 │   SALARIED   │                  │SELF-EMPLOYED │                   │INFORMAL / GIG│
 └──────┬───────┘                  └──────┬───────┘                   └──────┬───────┘
        │                                 │                                  │
        ├─ Tier-1 Listed MNC (Priya)      ├─ Retail / Kirana (Ravi)          ├─ Platform Gig Fleet (Anita)
        ├─ Mid-Sized SME                  ├─ Formal MSME (Audited/GST)       ├─ Home Micro-Enterprise
        ├─ Early Startup / Contract       └─ Licensed Pro (Doctor/CA)        └─ Daily Wage / Unregistered
        └─ Govt / PSU Employee
```

### Archetype Profiles:
1. **Priya (29, Bengaluru · Salaried Tier-1 MNC):**
   - *Underwriting Focus:* Prime corporate unsecured loan pricing (10.5%–11.25%), capping processing fee drag, and budgeting real disposable income after urban rent and lifestyle expenses.
   - *Failure Mode:* Banks approve large loans based strictly on gross salary, while high fixed rent and living costs leave insufficient liquidity for emergencies.
2. **Ravi (42, Mysuru · Self-Employed MSME Kirana Store):**
   - *Underwriting Focus:* **Product Pivoting.** Diverting cash-heavy, low-ITR merchants away from predatory 18%–24% unsecured business loans into prime 9.75%–10.50% Loan Against Property (LAP) backed by unencumbered commercial real estate.
   - *Failure Mode:* Traditional bank algorithms reject low-tax-return merchants, forcing them into high-interest informal finance.
3. **Anita (35, Hubballi · Informal / Gig Economy Courier):**
   - *Underwriting Focus:* **Distress Screening & Productive Asset ROI.** Activating mandatory kill-switches on active bounces or high-cost digital app debt (>30% APR), then modeling fuel savings from commercial EV scooters.
   - *Failure Mode:* Stacking high-cost digital payday app loans to bridge daily cash shortfalls, leading to compounding debt cycles.

---

## 6. MASTER QUESTION MATRIX & CONFIDENCE PROGRESSION ENGINE

### 6.1 Two-Tier Structure:
- **Tier 1: Universal Mandatory ($M_{01} - M_{10}$):** 10 questions required from every applicant. Answering these unlocks baseline calculations at **60.0% Base Confidence** with wide rate and capacity spreads ($\pm 2.0\%$).
- **Tier 2: Category Variable Questions (18 per category):** Specialized questions ($S_{01}–S_{18}$ for Salaried, $B_{01}–B_{18}$ for MSME, $I_{01}–I_{18}$ for Informal). Each answered question increases confidence by $+1.0\%$ to $+4.0\%$ and narrows output bands.
- **Confidence Cap (95.0%):** Acknowledges that self-reported inputs lack third-party API or document verification.

```
[Universal Mandatory Questions (M01-M10)] ───> 60.0% Base Confidence (Wide Output Bands: ±2.0%)
                 │
                 ▼ Branch on M04 (Employment Type)
┌──────────────────────────────────────┬──────────────────────────────────────┐
▼                                      ▼                                      ▼
[Salaried Track: S01-S18]     [MSME Track: B01-B18]         [Informal Track: I01-I18]
(+1.0% to +3.0% per answer)   (+1.0% to +4.0% per answer)   (+1.0% to +3.5% per answer)
└──────────────────────────────────────┼──────────────────────────────────────┘
                                       │
                                       ▼
             Full Category Completion ───> 95.0% Max Confidence (Tight Bands: ±0.3%)
```

---

### 6.2 Universal Mandatory Questions (10 Questions – Base 60.0%)

| ID | Question Text | Input Type | Options / Units | Impact | Underwriting Logic & Impact | Weight |
| :---: | :--- | :---: | :--- | :---: | :--- | :---: |
| **M01** | What is the primary purpose of this loan? | Select | Wedding, Business Expansion, Vehicle Purchase, Home Renovation, Debt Consolidation, Medical Emergency | $O_1, O_3$ | Sets default product category and maximum allowed tenure boundaries. | +6.0% (6%) |
| **M02** | What is the target loan amount you want to borrow? | Numeric | INR (₹) | $O_1, O_2$ | Sets requested principal ($P_{\text{req}}$) to evaluate against safe borrowing limit. | +6.0% (12%) |
| **M03** | Over how many months do you plan to repay? | Select/Num | Months (12, 24, 36, 48, 60, 84, 120) | $O_4$ | Defines amortization term ($n$) for installment calculations. | +6.0% (18%) |
| **M04** | What is your primary employment structure? | Select | Salaried, Self-Employed / MSME, Informal / Gig Economy | Branching | Sets baseline regulatory FOIR (40%–55%) and activates category wizard. | +6.0% (24%) |
| **M05** | What is your net monthly take-home income? | Numeric | INR (₹/month) | $O_2, O_4$ | Denominator ($I_{\text{net}}$) for FOIR and baseline for disposable cash flow. | +6.0% (30%) |
| **M06** | What is your total monthly outflow toward existing loan EMIs? | Numeric | INR (₹/month) | $O_2, O_4$ | Deducted directly ($E_{\text{old}}$) from allowable debt headroom. | +6.0% (36%) |
| **M07** | What is your monthly rent or housing outflow? | Numeric | INR (₹/month) | $O_2, O_4$ | Deducted directly ($C_{\text{rent}}$) in borrower residual cash flow calculation. | +6.0% (42%) |
| **M08** | What do you spend monthly on essential household living costs? | Numeric | INR (₹/month) | $O_2, O_4$ | Non-negotiable floor ($C_{\text{living}}$) for food, utilities, school fees, healthcare. | +6.0% (48%) |
| **M09** | What is your current credit score (CIBIL)? | Select | 750+, 700–749, Below 700, Unknown / Unscored | $O_3$ | Prime discounts rate (-1.0%); unknown widens band ($\pm 2.0\%$) without penalty. | +6.0% (54%) |
| **M10** | What is your current age? | Numeric | Years | $O_2, O_4$ | Caps maximum loan tenure based on retirement age boundary ($60 - \text{Age}$). | +6.0% (60%) |

---

### 6.3 Category-Specific Variable Questions (18 Questions Per Track)

#### Track A: Salaried Variables ($S_{01} - S_{18}$)
1. **S01. Employer Corporate Classification (+3.0% $\rightarrow$ 63.0%):** Tier-1/MNC/Govt raises FOIR to 55% and cuts spread by 0.50%; Early-Stage Startup caps FOIR at 45%.
2. **S02. Current Job Vintage (+2.5% $\rightarrow$ 65.5%):** $\ge 3$ years narrows spread by $\pm 0.50\%$; $<1$ year adds 0.75% job-hopping penalty.
3. **S03. Total Career Experience (+2.0% $\rightarrow$ 67.5%):** $>5$ years unlocks 60–72 month tenures; $<2$ years caps tenure at 36 months.
4. **S04. Salary Payment Mode (+2.0% $\rightarrow$ 69.5%):** Direct bank transfer (NEFT/IMPS) validates 100% income; cash salary takes a 25% qualifying haircut.
5. **S05. Variable Pay / Bonus Share (+2.0% $\rightarrow$ 71.5%):** If $>20\%$ of CTC, discounts monthly base income by 15% to buffer bonus volatility.
6. **S06. Notice Period / Probation Status (+2.0% $\rightarrow$ 73.5%):** Active notice or probation adds a 1.50% spread markup and caps principal to 6 months' salary.
7. **S07. Liquid Emergency Runway (+2.5% $\rightarrow$ 76.0%):** $\ge 6$ months reduces required cash reserve from 10% to 5%, boosting safe EMI.
8. **S08. Credit Card Limit Utilization (+2.0% $\rightarrow$ 78.0%):** $>50\%$ utilization adds 0.50% spread penalty; $<20\%$ lowers spread by 0.25%.
9. **S09. Bureau Inquiries in Last 90 Days (+1.5% $\rightarrow$ 79.5%):** $>3$ inquiries widens upper rate band by +1.0% (credit hunger signal).
10. **S10. Quoted Bank Pre-Approved Rate (+3.0% $\rightarrow$ 82.5%):** Benchmarks the exact bank rate on the Negotiation Card to quantify savings.
11. **S11. Quoted Processing Fee % (+2.0% $\rightarrow$ 84.5%):** Factored into internal rate formulas with 18% GST to calculate true all-in APR.
12. **S12. Largest Existing Loan Remaining Tenure (+1.5% $\rightarrow$ 86.0%):** If $<12$ months remaining, engine projects step-up in future safe cash flow.
13. **S13. Planned Large Outlays in Next 12 Months (+1.5% $\rightarrow$ 87.5%):** Deducts planned one-off capital needs from liquid buffers.
14. **S14. Co-Applicant Net Income (+2.0% $\rightarrow$ 89.5%):** Combines with primary income to increase FOIR ceiling and safe limit.
15. **S15. Home Loan Tax Benefit Status (+1.5% $\rightarrow$ 91.0%):** Credits back monthly tax savings (~₹3,000–₹7,000) into disposable cash.
16. **S16. EPF / PF Balance Available (+1.5% $\rightarrow$ 92.5%):** Serves as secondary distress backstop, lowering stress test failure penalty.
17. **S17. Comprehensive Health Insurance (+1.0% $\rightarrow$ 93.5%):** Lowers required monthly emergency medical cash deduction by 5%.
18. **S18. Standalone Unsecured Loan Count (+1.5% $\rightarrow$ 95.0% Max):** $>2$ active unsecured personal loans adds a 1.0% multi-loan leverage penalty.

#### Track B: Self-Employed / MSME Variables ($B_{01} - B_{18}$)
1. **B01. Documented Annual ITR Profit (+3.0% $\rightarrow$ 63.0%):** Hard cap for formal unsecured banking sanction.
2. **B02. ITR Filing Vintage (+2.0% $\rightarrow$ 65.0%):** $\ge 3$ consecutive years of ITR filings cuts base rate spread by 0.75%.
3. **B03. Monthly Gross Cash Intake (+2.5% $\rightarrow$ 67.5%):** Evaluates actual operational cash flow to establish borrower safe EMI capacity.
4. **B04. Unencumbered Property Ownership (+3.5% $\rightarrow$ 71.0%):** **Critical Product Pivot.** If yes, switches loan from unsecured (16%–22%) to LAP (9.25%–11.0%).
5. **B05. Property Market Value (+2.5% $\rightarrow$ 73.5%):** Computes maximum LAP sanction capacity using 50%–60% Loan-to-Value (LTV).
6. **B06. Title Deed Legal Clarity (+2.0% $\rightarrow$ 75.5%):** Clean registered title deed narrows spread; unpartitioned deed widens spread by $\pm 2.0\%$.
7. **B07. Business Operating Vintage (+2.0% $\rightarrow$ 77.5%):** $\ge 5$ years operating at current location cuts rate spread by 0.50%.
8. **B08. Business Premises Ownership (+1.5% $\rightarrow$ 79.0%):** Owned shop eliminates rental overhead and increases stability score.
9. **B09. Annual GSTR-3B Turnover (+2.0% $\rightarrow$ 81.0%):** Unlocks GST surrogate lines (sanctioning up to 10%–15% of verified turnover).
10. **B10. Seasonal Cash Inflow Variance (+1.5% $\rightarrow$ 82.5%):** If revenue drops $>35\%$ in low season, anchors safe EMI strictly to the trough month.
11. **B11. Co-Applicant Family Income (+2.0% $\rightarrow$ 84.5%):** Adds verified secondary family cash flow to debt-servicing limits.
12. **B12. Commercial Vehicle Fleet Assets (+1.5% $\rightarrow$ 86.0%):** Provides secondary movable asset security, reducing equipment rate spreads.
13. **B13. Supplier Payment Terms (+1.5% $\rightarrow$ 87.5%):** Immediate cash-only suppliers require higher cash cushion, lowering safe EMI.
14. **B14. Customer Credit Receivables Days (+1.5% $\rightarrow$ 89.0%):** Receivables locked $>45$ days applies a 10% haircut on operating cash.
15. **B15. Average Daily Bank Balance (ABB) (+2.0% $\rightarrow$ 91.0%):** High daily credit balance cuts loan spreads by up to 1.0%.
16. **B16. Unsecured / MCA Debt Portion (+1.5% $\rightarrow$ 92.5%):** High short-term merchant cash advance debt flags distress, triggering "Borrow Less".
17. **B17. Expansion Net Margin Boost (+1.5% $\rightarrow$ 94.0%):** Incremental earnings from inventory added to future safe servicing capacity.
18. **B18. Statutory Tax / GST Disputes (+1.0% $\rightarrow$ 95.0% Max):** Pending statutory notices widens rate spread by 1.50% and bars prime NBFCs.

#### Track C: Informal / Gig Economy Variables ($I_{01} - I_{18}$)
1. **I01. Payment Bounces in Last 6 Months (+3.5% $\rightarrow$ 63.5%):** **Kill-Switch Rule.** Any bounce $\ge 1$ forces verdict to "Don't Borrow".
2. **I02. Active Instant Digital App Loans (+2.5% $\rightarrow$ 66.0%):** Identifies short-term digital leverage; triggers debt consolidation rules.
3. **I03. Total App Loan Outstanding Balance (+2.5% $\rightarrow$ 68.5%):** Sets mandatory debt clearance requirement before taking new credit.
4. **I04. App Loan Interest Rate Level (+2.5% $\rightarrow$ 71.0%):** Rates $>24\%$ trigger predatory debt policy, blocking non-essential debt.
5. **I05. Productive Equipment Income Boost (+3.0% $\rightarrow$ 74.0%):** Incremental income from equipment credited toward future repayment.
6. **I06. Payout Mode (Platform vs. Cash) (+2.5% $\rightarrow$ 76.5%):** Platform digital records unlock priority-sector EV rates (11%–13%) over personal rates.
7. **I07. Platform Active Working Days/Month (+2.0% $\rightarrow$ 78.5%):** $\ge 24$ days validates regular earnings; $<15$ days applies 20% volatility haircut.
8. **I08. Household Adult Earning Members (+1.5% $\rightarrow$ 80.0%):** Quantifies income redundancy to cushion household shocks.
9. **I09. Spouse Employment Status (+2.0% $\rightarrow$ 82.0%):** Long-term unemployed spouse increases stress test income drop to 30%.
10. **I10. Dependent Children Count (+1.5% $\rightarrow$ 83.5%):** Adds +₹3,000 per child to non-negotiable living expense floor.
11. **I11. Secondary Trade / Craft Skill (+1.5% $\rightarrow$ 85.0%):** Secondary informal income cushions platform vehicle downtime.
12. **I12. Liquid Emergency Cash / Gold (+2.0% $\rightarrow$ 87.0%):** Zero buffer triggers explicit warning: any lost workday causes default.
13. **I13. EV Fuel & Maintenance Savings (+2.0% $\rightarrow$ 89.0%):** Direct operational savings (~₹3,000–₹5,000/mo) credited toward vehicle EMI.
14. **I14. Informal Moneylender Debt (+1.5% $\rightarrow$ 90.5%):** Unregistered private debt treated as extreme distress, dropping allowable FOIR to 25%.
15. **I15. Commercial Registration / Badge (+1.5% $\rightarrow$ 92.0%):** Unlocks asset-hypothecated financing and clean commercial subsidies.
16. **I16. Primary Smartphone EMI Status (+1.0% $\rightarrow$ 93.0%):** Core tool installment prioritized; default on phone halts all gig earnings.
17. **I17. Family Medical Shock (Last 12 Mos) (+1.0% $\rightarrow$ 94.0%):** Past uninsured medical debt widens safe capacity uncertainty spread.
18. **I18. SHG / JLG Group Membership (+1.0% $\rightarrow$ 95.0% Max):** Unlocks priority micro-credit options at capped RBI rates (18%–22%).

---

## 7. MATHEMATICAL FORMULAS & UNDERWRITING CORE

### 7.1 Output 3 ($O_3$): Fair Interest Rate Band & All-In APR (IRR)

#### 1. Base Benchmark Rate Lookup Table
```python
PRODUCT_BASE_RATES = {
    "Prime_Corporate_Personal": {"min": 10.50, "max": 11.50, "default_pf": 1.0},
    "Standard_Personal":         {"min": 11.50, "max": 14.00, "default_pf": 1.5},
    "LAP_Mortgage":              {"min": 9.25,  "max": 10.75, "default_pf": 1.0},
    "Commercial_EV_Asset":       {"min": 11.00, "max": 13.50, "default_pf": 1.5},
    "High_Risk_Unsecured_MSME":  {"min": 16.00, "max": 22.00, "default_pf": 2.0},
    "Microfinance_JLG":          {"min": 18.00, "max": 22.00, "default_pf": 2.0}
}
```

#### 2. Risk Modifiers & Spread Calculation
- **Credit Score (CIBIL):**
  - $\ge 750$: $-1.00\%$
  - $700–749$: $0.00\%$
  - $< 700$: $+2.00\%$
  - **"Unknown / Unscored":** Widen spread symmetrically by $\pm 2.0\%$ without moving median.
- **Collateral / LAP Pivot:**
  - If unencumbered real estate is pledged ($V_{\text{prop}} > 0$): Product pivots to **LAP** ($9.25\%–10.75\%$), overriding high unsecured business rates.
- **Employer Tier:**
  - Listed Tier-1 / PSU: $-0.50\%$
  - Early-Stage Startup: $+0.75\%$
- **Confidence Spread Tightening:**
  $$\text{Half-Width} = 2.0\% \times \left(1 - \frac{\text{Confidence} - 60\%}{35\%}\right) + 0.35\%$$

#### 3. True All-In APR via Newton-Raphson Solver
Upfront fee deductions with statutory GST:
$$\text{Upfront Fees} = (P_{\text{req}} \times \text{Processing Fee \%}) \times (1 + \text{GST}_{0.18}) + \text{Documentation Charges}$$
$$\text{Net Disbursed Cash} = P_{\text{req}} - \text{Upfront Fees}$$

The True All-In APR ($r_{\text{APR}}$) is the annualized Internal Rate of Return equating monthly EMIs over $n$ periods to the net disbursed cash:
$$\text{Net Disbursed Cash} = \sum_{t=1}^{n} \frac{\text{EMI}}{(1 + r_{\text{APR}}/12)^t}$$

Solved iteratively in Python:
```python
def solve_true_apr(principal: float, emi: float, n: int, fee_pct: float, doc_charges: float = 0.0) -> float:
    upfront_fees = (principal * (fee_pct / 100.0) * 1.18) + doc_charges
    net_disbursed = principal - upfront_fees
    if net_disbursed <= 0 or emi <= 0 or n <= 0:
        return 0.0
    
    # Solve for monthly rate m: emi * (1 - (1+m)^(-n)) / m = net_disbursed
    m = (emi * n / net_disbursed - 1.0) / (n / 2.0)
    for _ in range(50):
        if abs(m) < 1e-9:
            pv = emi * n
            pv_prime = -emi * n * (n + 1) / 2.0
        else:
            pv = emi * (1.0 - (1.0 + m) ** (-n)) / m
            pv_prime = emi * ((n * (1.0 + m) ** (-n - 1) / m) - ((1.0 - (1.0 + m) ** (-n)) / (m * m)))
        
        diff = pv - net_disbursed
        if abs(diff) < 1e-5:
            break
        if abs(pv_prime) < 1e-12:
            break
        m = m - diff / pv_prime
        if m <= -1.0:
            m = 0.001
            
    return max(0.0, m * 12.0 * 100.0)
```

---

### 7.2 Output 2 ($O_2$): Two-Sided Borrowing Limits & "Which to Use"

#### 1. Lender Maximum Sanction (Bank View)
Calculated using regulatory Fixed Obligation to Income Ratio (FOIR):
$$\text{FOIR}_{\text{cap}} = \begin{cases} 
0.55 & \text{Salaried Tier-1 / PSU} \\ 
0.50 & \text{Salaried Mid-Market / Standard} \\ 
0.45 & \text{Self-Employed MSME} \\ 
0.40 & \text{Informal / Gig Worker} 
\end{cases}$$

$$\text{Lender Max EMI} = \max(0, (I_{\text{net}} \times \text{FOIR}_{\text{cap}}) - E_{\text{old}})$$
$$\text{Lender Sanction Limit} = \frac{\text{Lender Max EMI} \times [1 - (1 + r/12)^{-n}]}{r/12}$$

*Collateral Cap (LAP):*
If property collateral is pledged, sanction is bounded by Loan-To-Value:
$$\text{Lender Sanction}_{\text{LAP}} = \min(\text{Lender Sanction Limit}, \text{Property Value} \times 0.55)$$

#### 2. Borrower Safe Borrowing Limit (Affordability View)
Calculated using real disposable cash flow:
$$\text{Buffer}_{\text{pct}} = \begin{cases} 0.05 & \text{if liquid savings runway } \ge 6 \text{ months} \\ 0.10 & \text{standard / unverified} \end{cases}$$
$$\text{Emergency Buffer} = I_{\text{net}} \times \text{Buffer}_{\text{pct}}$$
$$\text{Borrower Safe EMI} = \max(0, I_{\text{net}} - E_{\text{old}} - C_{\text{rent}} - C_{\text{living}} - \text{Emergency Buffer} + \Delta I_{\text{asset}})$$
$$\text{Borrower Safe Limit} = \frac{\text{Borrower Safe EMI} \times [1 - (1 + r/12)^{-n}]}{r/12}$$

#### 3. The "Which One to Use" Recommendation Directive
The app compares both limits and provides an unequivocal recommendation:
- If $\text{Borrower Safe Limit} < \text{Lender Sanction Limit}$:
  > **Use Your Safe Limit (₹X):** The bank is willing to sanction up to ₹Y because its formula ignores your rent (₹A) and living expenses (₹B). Taking the bank's maximum will wipe out your savings and leave you vulnerable to immediate default during an emergency.
- If $\text{Borrower Safe Limit} \ge \text{Lender Sanction Limit}$:
  > **Use the Lender Sanction Limit (₹Y):** Your strong cash buffers easily support the maximum regulatory sanction.

---

### 7.3 Output 4 ($O_4$): Monthly Payment Ceiling, Tenure Trade-Off & Dual Stress Shock

#### 1. Baseline Safe Monthly Ceiling
$$\text{Baseline EMI Ceiling} = \min(\text{Lender Max EMI}, \text{Borrower Safe EMI})$$

#### 2. Dual Stress Shock Engine
Simulate an adverse macroeconomic scenario:
1. **Income Drop Shock:** $20\%$ drop in net take-home earnings ($I_{\text{stress}} = I_{\text{net}} \times 0.80$).
2. **Interest Rate Shock:** $+2.0\%$ spike on floating rate debt ($r_{\text{stress}} = r + 2.0\%$).

Compute stressed debt obligations:
$$\text{Stressed EMI} = \text{PMT}\left(\frac{r_{\text{stress}}}{12}, n, P_{\text{req}}\right)$$
$$\text{Stressed Total Debt Outflow} = E_{\text{old}} + \text{Stressed EMI}$$
$$\text{Distress Ratio} = \frac{\text{Stressed Total Debt Outflow}}{I_{\text{stress}}}$$

**The 65% Distress Ceiling:**
If $\text{Distress Ratio} > 65\%$, the Monthly EMI Ceiling is systematically reduced until debt service survives the downturn:
$$\text{Stressed EMI Cap} = (I_{\text{stress}} \times 0.65) - E_{\text{old}}$$
$$\text{Monthly EMI Ceiling} = \max(0, \min(\text{Baseline EMI Ceiling}, \text{Stressed EMI Cap}))$$

#### 3. Tenure Trade-Off Matrix
The app displays an interactive table showing how extending tenure impacts monthly payment versus total interest paid:

| Repayment Tenure | Monthly Installment (₹) | Total Interest Paid (₹) | Total Repayment (₹) | Affordability Rating |
| :---: | :---: | :---: | :---: | :---: |
| **24 Months** | ₹37,290 / mo | ₹94,960 | ₹8,94,960 | High Monthly Strain |
| **36 Months** | ₹26,200 / mo | ₹1,43,200 | ₹9,43,200 | Balanced Outflow |
| **48 Months** | ₹20,690 / mo | ₹1,93,120 | ₹9,93,120 | **Recommended Sweet-Spot** |
| **60 Months** | ₹17,400 / mo | ₹2,44,000 | ₹10,44,000 | Excessive Interest Drag |

---

### 7.4 Output 1 ($O_1$): Three-Tier Recommendation Verdict Engine

```
                             [Triage Check 1]
                 Are any Distress Kill-Switches Active?
       - Auto-debit / loan bounces in last 6 months >= 1?
       - Active digital payday app loans charging > 24% APR?
       - Borrower Safe EMI Capacity <= 0?
                              │
               YES ───────────┴─────────── NO
                │                           │
                ▼                           ▼
       [VERDICT: DON'T BORROW]     [Triage Check 2]
                                   Does the Loan Breach Safe Headroom?
                                   - Requested EMI > Safe EMI Ceiling?
                                   - Requested Principal > Safe Limit?
                                            │
                             YES ───────────┴─────────── NO
                              │                           │
                              ▼                           ▼
                     [VERDICT: BORROW LESS]      [Triage Check 3]
                                                 Stress Ratio <= 65% &
                                                 Cash Buffers Intact?
                                                          │
                                                          ▼
                                                 [VERDICT: BORROW]
```

---

## 8. THE "EVERY NUMBER HAS A WHY" DIAGNOSTIC ENGINE

Every output pairs its hard quantitative fact with a single, dynamically formatted English diagnostic sentence derived from deterministic bottleneck priority trees:

```python
# Output 1: Verdict Why Generator
def explain_verdict(profile: dict, calculated: dict) -> str:
    if calculated["bounces_last_6m"] >= 1:
        return f"Why: A loan bounce in the last 6 months triggered our distress safety rule; adding new debt before clearing arrears creates severe insolvency risk."
    if calculated["has_high_cost_app_debt"]:
        return f"Why: You carry active digital app debt above 24% APR; taking new loans before consolidating these leads to a compounding debt trap."
    if calculated["safe_emi_cap"] <= 0:
        return f"Why: Essential living costs of ₹{profile['living']:,} and existing debt of ₹{profile['existing_emi']:,} already consume 100% of your take-home pay."
    if profile["requested_emi"] > calculated["safe_emi_cap"]:
        gap = profile["requested_emi"] - calculated["safe_emi_cap"]
        return f"Why: Your requested loan requires an EMI of ₹{profile['requested_emi']:,}, which overshoots your safe monthly surplus of ₹{calculated['safe_emi_cap']:,} by ₹{gap:,}."
    return f"Why: Your requested monthly EMI of ₹{profile['requested_emi']:,} fits comfortably within your safe monthly limit of ₹{calculated['safe_emi_cap']:,} while keeping your emergency living buffer intact."

# Output 2: Maximum Amount Gap Why Generator
def explain_limits(profile: dict, calculated: dict) -> str:
    lender = calculated["lender_sanction"]
    safe = calculated["safe_limit"]
    rent = profile.get("rent", 0)
    living = profile.get("living", 0)
    if safe < lender:
        return f"Why: Banks will approve up to ₹{lender:,} based purely on gross income, but your rent of ₹{rent:,} and living expenses limit your safe debt capacity to ₹{safe:,}."
    return f"Why: Minimal fixed living expenses and zero high-cost debt allow your safe borrowing capacity to match standard banking sanction limits."

# Output 3: Rate Band & APR Why Generator
def explain_rate(profile: dict, calculated: dict) -> str:
    if profile.get("has_collateral"):
        return f"Why: Pledging an unencumbered shop/property shifts your product to Loan Against Property (LAP), reducing the rate from 18%+ unsecured to {calculated['rate_min']}%–{calculated['rate_max']}%."
    if profile.get("cibil", 0) >= 750:
        return f"Why: Your 750+ CIBIL qualifies you for the prime corporate band, while a {calculated['pf_pct']}% processing fee plus GST sets the true all-in APR at {calculated['all_in_apr']}%."
    if profile.get("cibil_unknown"):
        return f"Why: A wider rate band of {calculated['rate_min']}%–{calculated['rate_max']}% is applied because your credit history is unverified, ensuring transparency without penalizing you as a defaulter."
    return f"Why: Standard credit risk adjustments for debt utilization and job vintage set your rate band at {calculated['rate_min']}%–{calculated['rate_max']}%."

# Output 4: Monthly Safe EMI Ceiling Why Generator
def explain_ceiling(profile: dict, calculated: dict) -> str:
    safe = calculated["safe_emi_cap"]
    lender_foir_emi = calculated["lender_foir_emi"]
    rent = profile.get("rent", 0)
    if calculated.get("stress_adjusted"):
        return f"Why: Under a 20% income downturn, an EMI above ₹{safe:,} would consume over 65% of your remaining cash flow, so the ceiling was adjusted downward."
    if safe < lender_foir_emi:
        return f"Why: While bank FOIR rules allow up to ₹{lender_foir_emi:,}/month, your monthly rent of ₹{rent:,} and living expenses cap your safe payment at ₹{safe:,} to protect your living buffer."
    return f"Why: Capped at ₹{safe:,} because regulatory guidelines prevent total monthly debt repayments from exceeding 50% of your take-home pay."
```

---

## 9. THE MOBILE NEGOTIATION CARD & IN-BRANCH SCRIPT ENGINE

The Negotiation Card transforms backend calculations into concrete leverage points and an actionable counter-script that the borrower can hold up to a loan officer inside a bank branch:

```
+-----------------------------------------------------------------------------------------+
|                                 MOBILE NEGOTIATION CARD                                 |
+-----------------------------------------------------------------------------------------+
| 1. TARGET ANCHORS (Counter-Benchmarks)                                                  |
|   * Target Product: Prime Unsecured Corporate Personal Loan                             |
|   * Fair Rate Band: 10.50% - 11.25%                                                     |
|   * Hard APR Ceiling: 11.65% (With Upfront Fee <= 1.0% + GST)                           |
|   * Safe Monthly EMI Ceiling: ₹37,500 / month                                           |
+-----------------------------------------------------------------------------------------+
| 2. BORROWER LEVERAGE POINTS                                                             |
|   [+] CIBIL score of 780 places profile in prime institutional pricing tier.             |
|   [+] 5 years of verified continuous stability at a Tier-1 listed corporate employer.   |
|   [+] 8 months of liquid emergency runway eliminates repayment default risk.            |
|   [+] Existing car loan utilization is under 15% of net income with 2 years clean history.  |
+-----------------------------------------------------------------------------------------+
| 3. BANK TRAPS TO REJECT                                                                 |
|   [!] DECLINE mandatory single-premium credit life or loan shield insurance bundling.    |
|   [!] REFUSE upfront processing fee charges exceeding 1.0% + GST.                       |
|   [!] REJECT loan structures with foreclosure lock-in periods exceeding 12 months.       |
+-----------------------------------------------------------------------------------------+
| 4. VERBATIM SPOKEN COUNTER-SCRIPT                                                       |
|   "I am applying for a Prime Unsecured Corporate Personal Loan. Based on my CIBIL score |
|   of 780 and 5-year tenure at a Tier-1 corporate, standard regulatory pricing indicates |
|   a fair rate of 10.50% to 11.25%, with an all-in APR cap of 11.65%. My monthly payment  |
|   ceiling is strictly ₹37,500/month; I will not accept structured tenures, fee markups  |
|   above 1.0%, or mandatory insurance deductions from my loan disbursement."             |
+-----------------------------------------------------------------------------------------+
```

---

## 10. END-TO-END CANONICAL PERSONA RUN-THROUGHS

### 10.1 Persona 1: Priya (29, Bengaluru · Salaried)
* **Profile:** Software engineer at a large MNC for 5 years. Net ₹1,10,000/mo. One car loan, EMI ₹14,000, 2 years left. Credit score 780. Rents at ₹28,000. Essential living: ₹25,000. Runway: 8 months.
* **Loan Request:** Wants ₹8,00,000 for a wedding over 48 months.
* **Underwriting Math:**
  - Base FOIR Cap: $55\%$ (Tier-1 MNC) $\rightarrow \text{Lender Max EMI} = (1,10,000 \times 0.55) - 14,000 = \text{₹46,500/mo}$.
  - Emergency Buffer: $5\%$ (runway $\ge 6$ mos) $\rightarrow \text{Buffer} = \text{₹5,500/mo}$.
  - Borrower Safe EMI: $1,10,000 - 14,000 - 28,000 - 25,000 - 5,500 = \text{₹37,500/mo}$.
  - Requested EMI (₹8L at 11.0% for 48m): ₹20,690/mo.
  - True All-In APR (with 1.0% fee + 18% GST): $11.65\%$.
  - Stress Shock Test: Under 20% income shock ($I_{\text{stress}} = \text{₹88,000}$), total debt is $14,000 + 20,690 = \text{₹34,690}$ ($\text{Stress Ratio} = 39.4\% \le 65\% \rightarrow \text{PASS}$).
* **Outputs:**
  - $O_1$ (Verdict): **BORROW**  
    *Why: Your requested monthly EMI of ₹20,690 fits comfortably within your safe monthly limit of ₹37,500 while keeping your emergency living buffer intact.*
  - $O_2$ (Limits): **Lender Sanction: ₹18,10,000 | Safe Limit: ₹14,60,000 $\rightarrow$ Use Your Safe Limit (₹14.6L)**  
    *Why: Banks will approve up to ₹18.1L based purely on gross income, but your rent of ₹28,000 and living expenses limit your safe debt capacity to ₹14.6L.*
  - $O_3$ (Rate & APR): **Fair Rate: 10.50% – 11.25% | All-In APR: 11.65%**  
    *Why: Your 780 CIBIL and Tier-1 employer qualify you for the prime corporate band, while a 1.0% processing fee plus GST sets the true APR at 11.65%.*
  - $O_4$ (Monthly Ceiling): **₹37,500/month (Survives 20% income shock)**  
    *Why: While bank FOIR rules allow up to ₹46,500/month, your monthly rent of ₹28,000 and living expenses cap your safe payment at ₹37,500 to protect your living buffer.*
* **Negotiation Card:** Target prime corporate rate; reject bundled credit-life insurance.

---

### 10.2 Persona 2: Ravi (42, Mysuru · Self-Employed)
* **Profile:** Kirana store for 14 years. Cash income ₹40,000–80,000/mo (avg ₹65,000/mo, gross ₹85,000/mo); ITR shows ₹4,20,000/year (₹35,000/mo). Owns shop premises valued at ₹45,00,000, unencumbered. Never taken formal loan; no credit score. Wife earns ₹18,000 teaching. Living costs: ₹28,000. Rent: ₹0.
* **Loan Request:** Wants ₹15,00,000 for a second stock line and delivery vehicle over 84 months.
* **Underwriting Math:**
  - **The Critical Product Pivot:** Standard unsecured bank algorithms cap unsecured business loans at $1.5\times$ annual ITR profit (~₹5,00,000) at punitive rates of $18\%–22\%$. Pledging the unencumbered ₹45L commercial shop pivots the product to **Loan Against Property (LAP)** at $9.75\%–10.50\%$.
  - LAP Sanction Capacity (50% LTV): $45,00,000 \times 0.50 = \text{₹22,50,000}$.
  - Combined Family Cash Income: $65,000 + 18,000 = \text{₹83,000/mo}$.
  - Borrower Safe EMI Capacity: $83,000 - 0 - 0 - 28,000 - 8,300 (\text{buffer}) = \text{₹46,700/mo}$ (Conservative anchor: ₹42,500/mo for low monsoon season).
  - Requested Loan EMI (₹15L at 10.0% for 84m): ₹24,900/mo.
* **Outputs:**
  - $O_1$ (Verdict): **BORROW**  
    *Why: Pledging your unencumbered shop unlocks prime LAP pricing, and the ₹24,900 EMI fits well within low-season cash flows.*
  - $O_2$ (Limits): **Lender Sanction (LAP): ₹22,50,000 | Safe Limit: ₹21,00,000 $\rightarrow$ Use Your Safe Limit (₹21.0L)**  
    *Why: Pledging your unencumbered shop pivots you to secured LAP, unlocking up to ₹22.5L while avoiding predatory 18%+ unsecured loans.*
  - $O_3$ (Rate & APR): **Fair Rate: 9.75% – 10.50% | All-In APR: 10.85%**  
    *Why: Pledging an unencumbered shop shifts your product to Loan Against Property (LAP), reducing the rate from 18%+ unsecured to 9.75%–10.50%.*
  - $O_4$ (Monthly Ceiling): **₹42,500/month (Anchored to business low season)**  
    *Why: Because retail businesses experience seasonal turnover drops, your safe ceiling is anchored strictly to your lowest earning months.*
* **Negotiation Card:** Demand LAP pricing (9.75%–10.50%); firmly reject diversion to high-interest unsecured merchant loans.

---

### 10.3 Persona 3: Anita (35, Hubballi · Informal)
* **Profile:** Food delivery rider plus home tailoring. Net ₹26,000–30,000/mo (avg ₹28,000/mo). Two children. Husband unemployed 8 months. Three instant digital app loans, ₹35,000 outstanding at 30%+ APR. One EMI bounced last month. Smartphone EMI: ₹1,500/mo. Rent: ₹5,000/mo. Living costs: ₹18,000/mo.
* **Loan Request:** Wants ₹1,50,000 for an electric scooter over 24 months. EV saves ₹3,500/mo in petrol.
* **Underwriting Math:**
  - **Kill-Switch Active:** Auto-debit bounce in last 6 months $\ge 1$ and active digital app loans $>24\%$ APR immediately trigger **DON'T BORROW**.
  - Disposable Cash Surplus (Pre-Restructuring): $28,000 - 1,500 - 5,000 - 18,000 = \text{₹3,500/mo}$.
  - Requested EV Loan EMI (₹1.5L at 12.5% for 24m): ~₹7,090/mo (overshoots available surplus).
* **Outputs:**
  - $O_1$ (Verdict): **DON'T BORROW**  
    *Why: A loan bounce in the last 6 months and active 30%+ instant app loans flag severe default distress; taking new debt before clearing arrears creates extreme insolvency risk.*
  - $O_2$ (Limits): **Lender Sanction: ₹0 (Blocked) | Safe Limit: ₹0 $\rightarrow$ Clear App Debt First**  
    *Why: Active payment bounces and short-term digital loan arrears block formal lending eligibility until debts are consolidated.*
  - $O_3$ (Rate & APR): **Fair Rate: 11.50% – 13.00% (Commercial EV) | Current App Debt: >30% APR**  
    *Why: You carry active digital app debt above 24% APR; taking new loans before consolidating these leads to a compounding debt trap.*
  - $O_4$ (Monthly Ceiling): **₹3,500/month (Requires debt clearance before onboarding)**  
    *Why: Household essential costs and smartphone installments leave only ₹3,500 surplus; clearing app debt must precede vehicle purchase.*
* **Negotiation Card:** Restructure existing app loans; leverage operational EV fuel savings to finance asset through OEM NBFC or priority micro-credit.

---

## 11. HONESTY ABOUT LIMITS & GUESSING TRANSPARENCY

To satisfy Scoring Area #6 (Honesty about limits - 5 pts), the application explicitly discloses where it is estimating versus calculating from verified facts:

```
+-----------------------------------------------------------------------------------------+
|                            ESTIMATION & ASSUMPTION BADGES                               |
+-----------------------------------------------------------------------------------------+
| [!] BASELINE ESTIMATION: Credit score is unverified. Rate band expanded by +/- 2.0%     |
| [!] ASSUMED PROPERTY LTV: Valuation is unverified; standard 50% conservative LTV applied|
| [!] UNVERIFIED SAVINGS RUNWAY: Default 10% cash reserve applied (assumes < 6 mos liquid)|
| [*] VERIFIED INFERENCE: Employer classified as Tier-1; corporate prime spread unlocked  |
+-----------------------------------------------------------------------------------------+
```

1. **Explicit Uncertainty Indicators:** If the user has only answered mandatory questions, every card features an amber banner:  
   *`Preliminary Assessment (60% Confidence) — Output bands widened to reflect unverified variables.`*
2. **Missing Input Consequences:** When a user selects "Unknown" for credit score or leaves collateral empty, the card directly informs them how that choice impacted their numbers (e.g., *`"Unknown CIBIL added ±2.0% spread uncertainty"`*).
3. **Formal Codification in `RULES.md`:** Every threshold, cap, and formula is mapped to its regulatory benchmark or documented as *"Author's Domain Judgement"*.

---

## 12. UI/UX LAYOUT, VISUAL HIERARCHY & INTERACTIVE COMPONENTS

```
+-----------------------------------------------------------------------------------------+
|                                    BORROWER COPILOT                                     |
|           Pre-Lender Underwriting Self-Assessment for Indian Borrowers                  |
+-----------------------------------------------------------------------------------------+
| QUICK-LOAD TEST PERSONAS:                                                               |
| [ > Priya (Salaried MNC) ]  [ > Ravi (Kirana MSME) ]  [ > Anita (Informal Delivery) ]   |
+-----------------------------------------------------------------------------------------+
| LIVE CONFIDENCE GAUGE: [████████████████████░░░░░░░░░░] 60.0% (Mandatory Baseline)      |
| "Answer category questions below to tighten rate bands and increase confidence to 95%"  |
+-----------------------------------------------------------------------------------------+
| STEP 1: MANDATORY QUESTIONS (10 of 10 Completed)                                        |
| 1. Purpose [Wedding]   2. Target [₹8,00,000]   3. Tenure [48 Mos]   4. Type [Salaried]  |
| 5. Income [₹1,10,000]  6. Old EMIs [₹14,000]   7. Rent [₹28,000]    8. Living [₹25,000] |
| 9. CIBIL [750+]        10. Age [29 Years]                                               |
+-----------------------------------------------------------------------------------------+
| STEP 2: ADAPTIVE VARIABLE QUESTIONS (Salaried Module: 8 of 18 Answered)                 |
| [v] S01: Tier-1 MNC (+3.0%)  [v] S02: 5 Years Vintage (+2.5%)  [v] S07: 8 Mos Runway...|
+-----------------------------------------------------------------------------------------+
|                                   THE FOUR OUTPUT CARDS                                 |
| +------------------------------------+  +---------------------------------------------+ |
| | O1: RECOMMENDATION VERDICT         |  | O2: MAXIMUM BORROWING CAPACITY              | |
| | [VERDICT: BORROW]                  |  | Lender Max: ₹18.1L  |  Safe Limit: ₹14.6L   | |
| | Why: Requested EMI of ₹20,690 fits |  | > USE YOUR SAFE LIMIT: ₹14,60,000           | |
| | within safe limit of ₹37,500...    |  | Why: Banks approve up to ₹18.1L, but rent...| |
| +------------------------------------+  +---------------------------------------------+ |
| | O3: FAIR INTEREST RATE & APR       |  | O4: SAFE MONTHLY PAYMENT CEILING            | |
| | Fair Rate: 10.50% - 11.25%         |  | Safe EMI Ceiling: ₹37,500 / month           | |
| | All-In APR: 11.65% (With GST)      |  | Stress Test: Survives 20% income shock      | |
| | Why: 780 CIBIL & Tier-1 employer...|  | Why: Rent & living expenses cap payment...  | |
| +------------------------------------+  +---------------------------------------------+ |
+-----------------------------------------------------------------------------------------+
| TENURE TRADE-OFF COMPARISON TABLE (24m vs 36m vs 48m vs 60m)                            |
+-----------------------------------------------------------------------------------------+
|                             STANDALONE MOBILE NEGOTIATION CARD                          |
| [Target Anchors]  |  [Borrower Leverage]  |  [Traps to Reject]  |  [Verbatim Script]    |
| [ Copy In-Branch Negotiation Script ]                                                   |
+-----------------------------------------------------------------------------------------+
```

---

## 13. DELIVERABLES MAPPING & IMPLEMENTATION ROADMAP

The project directly produces the four required deliverables specified in the HTML challenge:

```
borrowing-copilot/
│
├── ARCHITECTURE_AND_SPECIFICATION.md  # Master Architectural Blueprint (This Document)
├── RULES.md                           # Deliverable 2: Complete Rule Registry with Sources
├── WALKTHROUGH.md                     # Deliverable 4: 5-Minute Technical & Design Walkthrough
├── README.md                          # Quickstart, Setup Guide & Persona Run-Throughs
├── requirements.txt                   # Minimal dependencies (streamlit)
│
├── engine/                            # Pure Python Deterministic Underwriting Core
│   ├── __init__.py
│   ├── underwriting.py                # PMT, PV, Newton-Raphson APR, FOIR, Limits, Stress
│   ├── confidence.py                  # 104-Row Parameter Table, Category Filter, Weights
│   ├── explanations.py                # Deterministic Priority Trees & Rule 4 "Why" Strings
│   └── negotiation.py                 # Negotiation Card & Dynamic Counter-Script
│
├── app.py                             # Deliverable 1: Interactive Mobile-First Web Application
└── tests/
    └── test_personas.py               # Deliverable 3: Automated Persona Test Suite
```

### Execution Milestones:
1. **Phase 1: Pure Underwriting Engine (`engine/underwriting.py`, `engine/confidence.py`)**  
   Implement PMT formulas, Present Value, Newton-Raphson IRR solver for True APR with 18% GST, FOIR lookups, disposable cash flow math, dual shock stress simulation, and 104-row confidence progression.
2. **Phase 2: Diagnostic & Negotiation Generators (`engine/explanations.py`, `engine/negotiation.py`)**  
   Implement the deterministic bottleneck priority trees for single-sentence diagnostics (Rule 4) and assemble the high-contrast Negotiation Card.
3. **Phase 3: Formal Rule Registry (`RULES.md`)**  
   Compile every rule, threshold, percentage, and regulatory origin into a structured reference table.
4. **Phase 4: Persona Validation Suite (`tests/test_personas.py`)**  
   Validate Priya, Ravi, and Anita against expected benchmarks with automated unit assertions.
5. **Phase 5: Interactive Web Application (`app.py`)**  
   Construct the responsive interface featuring adaptive question flows, live confidence gauge, paired two-fold cards, tenure trade-off visualizer, and in-branch negotiation card.
6. **Phase 6: Written Walkthrough (`WALKTHROUGH.md`)**  
   Provide the 5-minute written walkthrough detailing design trade-offs, what to build next, and what to cut.

---
*End of Master Architecture & Specification Plan.*
