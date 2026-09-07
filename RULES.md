# RULES REGISTRY & UNDERWRITING ASSUMPTIONS (RULES.md)

> **Document:** `RULES.md`  
> **Challenge:** Lokta · Borrower Copilot (Version 1.0)  
> **Mandate:** Comprehensive registry of all financial rules, thresholds, product pricing bands, stress shocks, and confidence calibrations implemented in the deterministic underwriting engine.  
> **Standard Format:** *What · Value · Why · Source / Attribution*

---

## 1. UNDERWRITING RULES, THRESHOLDS & BENCHMARKS

| Parameter / Rule Name | Assigned Value | Why (Financial & Risk Rationale) | Source / Attribution |
| :--- | :---: | :--- | :--- |
| **Salaried Prime FOIR Cap** | **55.0%** of net income | Tier-1 corporate and PSU employees enjoy institutional job security and low uncollateralized default risk, allowing higher debt-servicing allowances. | Standard Indian Banking Norm (SBI / HDFC Corporate Salary Circulars) |
| **Salaried Standard FOIR Cap** | **50.0%** of net income | Regulatory prudential limit ensuring mid-market corporate employees do not over-leverage disposable income. | RBI Prudential Retail Underwriting Guidelines |
| **Salaried Startup/Contract FOIR Cap** | **45.0%** of net income | Early-stage startup employees and fixed-term contractors face higher employer churn and liquidity runway risks. | Standard Credit Policy (NBFC FinTech Underwriting) |
| **Self-Employed / MSME FOIR Cap** | **45.0%** of gross cash intake | Business cash flows exhibit operational volatility, supplier cycle variances, and unrecorded trade overheads. | RBI MSME Lending Framework |
| **Informal / Gig Worker FOIR Cap** | **40.0%** of net earnings | Daily wage and gig earners have volatile platform shifts and zero formal paid leave or provident fund cushion. | RBI Fair Practices Code for Digital Lending |
| **Informal Moneylender Distress FOIR**| **25.0%** of net earnings | Unregistered daily/weekly private debt incurs extortionate compounding interest (>60% APR), depleting basic survival capacity. | Author's Domain Judgement |
| **Cash Salary Haircut** | **25.0%** deduction | Cash salary deposits lack bank statement audit trails and verifiable employer payroll remittances. | Bank Income Verification & KYC Policy |
| **Variable Pay / Bonus Discount** | **15.0%** haircut if bonus > 20% | Annual bonuses and quarterly incentives are volatile; conservative underwriting anchors to base guaranteed monthly pay. | Prime Retail Bank Credit Policy |
| **Emergency Cash Buffer (High Runway)**| **5.0%** of monthly income | Borrowers with $\ge 6$ months of verified liquid living expenses in bank/liquid mutual funds require smaller monthly deductions. | Personal Financial Planning Standards |
| **Emergency Cash Buffer (Standard)** | **10.0%** of monthly income | Default deduction from monthly take-home to ensure debt repayment does not deplete non-negotiable emergency liquidity. | Author's Domain Judgement |
| **Dependent Child Expense Floor** | **+₹3,000** / child / month | Direct addition to the non-negotiable living cost floor to guarantee nutrition, school fees, and child healthcare. | Cost of Living Benchmark (Tier-2/3 India) |
| **Notice Period / Probation Penalty** | **+1.50%** rate spread & 6-month cap | Pending job departure signals imminent cash-flow discontinuity; borrowing is capped to 6 months' salary. | Retail Underwriting Policy |
| **Multi-Loan Personal Leverage Penalty**| **+1.00%** rate spread if > 2 loans | Multiple active standalone unsecured loans indicate borrowing to service existing debts (leverage stacking). | Credit Bureau Credit-Hunger Indicators |
| **Credit Inquiries Risk Markup** | **+1.00%** rate spread if > 3 in 90d | High bureau inquiry frequency signals urgent liquidity distress, categorized as credit-hungry behavior. | CIBIL / Experian Credit Scoring Mechanics |
| **Credit Card Utilization Markup** | **+0.50%** rate spread if > 50% | Revolving card balances above 50% indicate high credit dependency and reduced monthly repayment headroom. | Credit Bureau Scoring Algorithms |
| **Credit Card Utilization Discount** | **-0.25%** rate spread if < 20% | Disciplined low credit card utilization signals prime liquidity management. | Author's Domain Judgement |
| **Dual Stress Shock: Income Downturn** | **-20.0%** net take-home pay | Simulates sudden job disruption, pay cuts, or local economic slowdown to test whether debt remains serviceable. | Lokta Challenge Brief & Basel Stress Guidelines |
| **Dual Stress Shock: Floating Rate Hike**| **+2.00%** interest rate spike | Simulates RBI monetary tightening and benchmark repo rate hikes on floating-rate retail debt. | RBI Monetary Policy Rate Cycle Benchmark |
| **Debt Distress Ratio Ceiling** | **65.0%** of stressed net income | Hard ceiling: Total monthly debt obligations exceeding 65% of stressed income trigger imminent default and insolvency. | Lokta Challenge Brief Deliverable #3 |
| **Statutory Upfront Fee Tax** | **18.0%** GST on Processing Fee | Processing and documentation fees charged by banks attract mandatory statutory GST, increasing effective fee drag. | Central Goods & Services Tax (CGST + SGST) Act |
| **Unencumbered Property LTV Cap** | **50.0% - 55.0%** Loan-to-Value | Conservative mortgage valuation ceiling applied when pivoting MSME borrowers from unsecured credit into secured LAP. | RBI Master Directions on Housing & LAP Finance |
| **Kill-Switch 1: Recent Loan Bounces** | **$\ge 1$ bounce in last 6 months** | Auto-debit (NACH/e-Mandate) bounce indicates immediate repayment distress; taking new loans deepens insolvency. | Lokta Challenge Brief (Rule: "Don't Borrow is reachable") |
| **Kill-Switch 2: Predatory App Debt** | **Active app debt with APR > 24%** | Micro-loans and payday apps charging >24%–36% APR create compounding debt spirals that cannot be fixed with new debt. | RBI Digital Lending Directions (May 2025) |
| **Kill-Switch 3: Zero / Negative Surplus**| **Borrower Safe Cash Flow $\le 0$** | When rent, essentials, and existing EMIs consume 100% of income, borrowing any additional amount causes immediate default. | Mathematical Affordability Rule |

---

## 2. PRODUCT PRICING BANDS & ALL-IN APR BENCHMARKS

The underwriting engine models fair market interest bands rather than single arbitrary point estimates. True All-In APR accounts for processing fees and statutory 18% GST:

| Product Classification | Target Profile | Nominal Fair Rate Band | Default Processing Fee | True All-In APR Band (with 18% GST) | Product Routing Logic |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **Prime Corporate Personal Loan** | Salaried Tier-1 MNC / PSU (750+ CIBIL) | **10.50% – 11.25%** | 1.0% + GST | **11.15% – 11.95%** | Category = Salaried, Tier-1 employer, CIBIL $\ge 750$. |
| **Standard Retail Personal Loan** | Salaried Mid-Market / Private SME | **11.50% – 13.50%** | 1.5% + GST | **12.45% – 14.55%** | Category = Salaried, standard employer vintage. |
| **Loan Against Property (LAP)** | Self-Employed / MSME (Unencumbered Shop) | **9.75% – 10.50%** | 1.0% + GST | **10.35% – 11.15%** | Pivoted when unencumbered property value $> 0$. |
| **Commercial EV Asset Hypothecation**| Informal Delivery Partner (Clean Digits) | **11.50% – 13.00%** | 1.25% + GST | **12.30% – 13.90%** | Category = Informal/Gig, EV vehicle purchase, digital payouts. |
| **Priority Sector Micro-Credit** | Informal Trade / Home Artisan / Daily Wage | **12.50% – 15.00%** | 1.5% + GST | **13.50% – 16.20%** | Category = Informal/Gig, general consumption/tool loan. |
| **High-Risk Unsecured MSME Line** | Self-Employed without Property Collateral | **16.00% – 22.00%** | 2.0% + GST | **17.50% – 23.90%** | Unsecured merchant advance when no collateral exists. |
| **Predatory Digital App Loans** | Instant Payday Credit Apps | **24.00% – 36.00%+**| 3.0% + GST | **27.50% – 42.00%+** | Flagged as predatory debt; triggers debt consolidation. |

---

## 3. UNCERTAINTY & CONFIDENCE PROGRESSION FORMULATION

In strict accordance with **Rule 2 ("Confidence widens with silence... Never narrow a range you have no basis to narrow")** and **Rule 3 ("Unknown is never zero")**:

1. **The 60.0% Mandatory Baseline:**  
   Answering the 10 Universal Mandatory questions ($M_{01} - M_{10}$) establishes the foundation for cash-flow calculations. The initial confidence meter sits at **60.0%**, and all interest rate spreads and capacity limits display wide uncertainty buffers ($\pm 2.0\%$ to $\pm 2.35\%$).
2. **Dynamic Spread Tightening Equation:**  
   As category-specific variable questions are answered, the confidence score climbs from 60.0% to 95.0%. The rate spread half-width ($W$) contracts according to:
   $$W = 2.0\% \times \left(1 - \frac{\text{Confidence} - 60\%}{35\%}\right) + 0.35\%$$
   - At 60.0% Confidence: $W = \pm 2.35\%$ (Wide uncertainty band reflecting unverified employer tier, liquid runway, and collateral).
   - At 95.0% Confidence: $W = \pm 0.35\%$ (Tight competitive band reflecting verified stability, collateral, and cash buffers).
3. **The 95.0% Confidence Ceiling:**  
   Confidence is capped at 95.0% because self-reported borrower inputs lack formal third-party bureau APIs, physical title deed scrutiny, or bank statement OCR verification.
4. **Handling of "Unknown" Inputs:**  
   - An unknown credit score is modeled as an unrated risk band ($\pm 2.0\%$ symmetric spread around product median). It is **never** defaulted to zero or treated as a subprime default.
   - An unknown property valuation does not block calculations; the engine alerts the borrower that LAP pivoting is available upon property appraisal.

---

## 4. HONESTY ABOUT LIMITS: ESTIMATION VS. DETERMINISTIC CALCULATION

| Area of Underwriting | Deterministic Calculation (What We Know) | Model Estimation / Guess (What We Assume) | Transparency Notice Shown to Borrower |
| :--- | :--- | :--- | :--- |
| **Loan Amortization (PMT & PV)** | Exact mathematical formula based on declared principal, tenure, and rate. | None. Mathematically exact. | None. Figures are accurate to the rupee. |
| **All-In APR (IRR)** | Exact 50-step Newton-Raphson internal rate of return including 18% statutory GST. | Quoted bank processing fee is assumed at 1.0%–1.5% if unquoted by user. | *"Assumed 1.0% processing fee with 18% GST; adjust if bank quote differs."* |
| **Lender Sanction Limit** | Regulatory FOIR percentage minus declared existing EMIs. | Assumes standard institutional bank underwriting policies (SBI/HDFC/ICICI). | *"Lender approval estimates standard bank FOIR; actual NBFC rules may vary."* |
| **Safe Borrowing Limit** | Exact subtraction of rent, essential living expenses, and old EMIs from net income. | Assumes living expenses remain steady during the loan tenure. | *"Living expenses self-reported; emergency buffer assumed at 5%–10%."* |
| **Credit Score Impact** | Codified prime discount (-0.50% to -1.0%) for 750+ CIBIL. | When "Unknown", assumes average unrated retail credit risk band. | *"Credit score unverified; rate band widened by ±2.0% without default penalty."* |
| **Dual Stress Shock** | Exact math: -20% net income drop and +2.0% rate hike tested against 65% debt cap. | Macroeconomic shock duration assumed to be temporary (6 to 12 months). | *"Simulates adverse economic shocks; does not predict personal health shocks."* |
| **Property Valuation (LAP)** | 50% LTV applied to declared unencumbered property value. | Assumes registered clean title deed free of litigation. | *"Subject to formal legal title search and registered bank valuation."* |

---
*End of RULES.md Registry.*
