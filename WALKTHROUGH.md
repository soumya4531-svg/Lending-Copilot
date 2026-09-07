# FIVE-MINUTE PRODUCT & ENGINEERING WALKTHROUGH (WALKTHROUGH.md)

> **Challenge:** Lokta · Borrower Copilot (Version 1.0)  
> **Deliverable:** Deliverable #4 (5-Minute Technical & Design Walkthrough)  
> **Author:** Antigravity Engineering  
> **Topic:** Codifying Institutional Lending Judgement into an Explainable Borrower Assistant

---

## 1. THE GAP WE SOLVED
Institutional lenders operate with extreme informational asymmetry:
- Lenders use regulatory FOIR formulas (approving up to 50%–60% of gross salary) that deliberately ignore living rent, dependents, and emergency liquidity.
- Lenders hide substantial fee drag behind nominal rates (processing fee + 18% statutory GST).
- Borrowers enter negotiations blind, accepting the first sanction letter without counter-benchmarks.

The **Borrower Copilot** turns lending judgement into deterministic, transparent rules running entirely on the borrower's device. No login, no remote database, no bureau footprint.

---

## 2. HOW THE FIVE JUDGING RULES ARE CODIFIED IN THE APP

### Rule 1: Adaptive Branching
- Salaried applicants (Priya), MSME merchants (Ravi), and informal gig riders (Anita) see completely different question paths.
- Selecting the employment type in $M_{04}$ dynamically reveals category-specific risk variables (e.g. Kirana ITR and property collateral vs. Gig delivery days and smartphone EMI) while hiding irrelevant questions.

### Rule 2: Confidence Widens with Silence
- The app initializes at **60.0% Base Confidence** upon completing the 10 Universal Mandatory questions ($M_{01}–M_{10}$).
- At 60% confidence, output bands are wide ($\pm 2.35\%$) because employer tier, liquid runway, and collateral remain unverified.
- As the user answers category variables, confidence scales smoothly up to **95.0% Max**, contracting the uncertainty band to $\pm 0.35\%$.
- Confidence is deliberately capped at 95.0% because self-reported borrower inputs lack third-party API verification.

### Rule 3: Unknown is Never Zero
- If a borrower enters "Unknown / Unscored" for their credit score or property value, the engine **never** defaults to zero or penalizes them as a subprime defaulter (300).
- Instead, it models an unrated risk band ($\pm 2.0\%$ symmetric spread) and explicitly explains the consequence on Output 3.

### Rule 4: Every Number Has a Why
- Every quantitative output ($O_1$ to $O_4$) is paired directly with an exact, single-sentence plain-English diagnostic.
- The engine uses **deterministic bottleneck priority trees** to identify the limiting factor (e.g., whether the safe ceiling was bounded by high rent, bank FOIR rules, or macroeconomic stress shocks).

### Rule 5: Grounded in Indian Lending Realities
- Standard FOIR caps (40%–55%), statutory 18% GST on processing fees, Loan Against Property (LAP) 50% LTV norms, and commercial EV hypothecation benchmarks. All calculations in Indian Rupees (₹).

---

## 3. VERIFICATION OF THE THREE PERSONAS

### Persona 1: Priya (Salaried MNC Professional, Bengaluru)
- **Profile:** Software engineer at a large MNC for 5 years. Net ₹1,10,000/mo. One car loan, EMI ₹14,000, 2 years left. Credit score 780. Rents at ₹28,000. Essential living: ₹25,000.
- **Loan Wanted:** ₹8,00,000 personal loan for a wedding over 48 months.
- **App Evaluation:**
  - $O_1$ (Verdict): **BORROW** (Safe surplus comfortably covers the ₹20,690 EMI).
  - $O_2$ (Limits): **Lender Sanction: ₹18,10,000 | Safe Limit: ₹14,60,000** $\rightarrow$ **Use Your Safe Limit (₹14.6L)**.
  - $O_3$ (Rate & APR): **Fair Rate: 10.50% – 11.25% | All-In APR: 11.65%** (Includes 1.0% fee + 18% GST).
  - $O_4$ (Ceiling): **₹37,500/month** (Survives 20% income shock: stress ratio is 39.4% $\le$ 65%).
  - **Negotiation Card:** Points out 780 CIBIL and 5-year Tier-1 tenure; advises rejecting bundled single-premium insurance.

### Persona 2: Ravi (Self-Employed Kirana Store Owner, Mysuru)
- **Profile:** Kirana store for 14 years. Cash income ₹85,000/mo; ITR shows ₹4,20,000/yr. Owns shop premises valued at ₹45,00,000 unencumbered. Unscored. Wife earns ₹18,000 teaching. Living: ₹28,000.
- **Loan Wanted:** ₹15,00,000 for stock line and delivery vehicle over 84 months.
- **App Evaluation:**
  - **The Critical Product Pivot:** Standard unsecured algorithms cap loans at ~₹5,00,000 at 18%–22% APR due to low ITR. The app detects the unencumbered shop and pivots Ravi to **Loan Against Property (LAP)**.
  - $O_1$ (Verdict): **BORROW**.
  - $O_2$ (Limits): **Lender Sanction (LAP): ₹22,50,000 | Safe Limit: ₹21,00,000** $\rightarrow$ **Use Your Safe Limit (₹21.0L)**.
  - $O_3$ (Rate & APR): **Fair Rate: 9.75% – 10.50% | All-In APR: 10.85%** (Rate dropped from 18%+ to 9.75% via collateral).
  - $O_4$ (Ceiling): **₹42,500/month** (Anchored to business low season).
  - **Negotiation Card:** Demands secured LAP pricing; rejects diversion to high-interest unsecured merchant debt.

### Persona 3: Anita (Informal Delivery Fleet Partner, Hubballi)
- **Profile:** Delivery rider plus home tailoring. Net ₹28,000/mo. Two children. Husband unemployed 8 months. Three app loans, ₹35,000 outstanding at 36% APR. One auto-debit bounce last month. Smartphone EMI: ₹1,500. Rent: ₹5,000. Living: ₹18,000.
- **Loan Wanted:** ₹1,50,000 for electric scooter over 24 months. EV saves ₹3,500/mo in petrol.
- **App Evaluation:**
  - **Kill-Switch Active:** Auto-debit bounce $\ge 1$ and app debt $> 24\%$ APR immediately trigger **DON'T BORROW**.
  - $O_1$ (Verdict): **DON'T BORROW** (*"Why: An auto-debit bounce in the last 6 months and active high-cost app debt (36% APR) flag acute distress; adding new debt before clearing arrears creates severe insolvency risk."*).
  - $O_2$ (Limits): **Lender Sanction: ₹0 | Safe Limit: ₹0** (Blocked until app loans are restructured).
  - $O_3$ (Rate & APR): **Fair Commercial EV Rate: 11.50% – 13.00% | Current App Debt: 36.00% APR**.
  - $O_4$ (Ceiling): **₹3,500/month** (Remaining surplus pre-restructuring).
  - **Negotiation Card:** Concrete strategy to consolidate digital app loans before onboarding EV asset financing.

---

## 4. WHAT WE WOULD BUILD NEXT (VERSION 2.0 ROADMAP)

1. **Client-Side Bank Statement OCR Parser:**
   - Allow users to drop in a PDF bank e-statement locally. Using client-side JavaScript/WASM OCR, parse out salary credits, true average monthly rent, and existing auto-debits without sending data to any server.
2. **Vernacular Multi-Language Audio Scripts:**
   - In-branch negotiation scripts translated and played aloud in Kannada, Hindi, Tamil, Telugu, and Marathi so gig workers and small shopkeepers can speak confidently to loan officers.
3. **Interactive Sanction Letter Scanner:**
   - Upload a sanction letter PDF or photo to automatically detect hidden insurance line items, inflated processing charges, and penal interest covenants.

---

## 5. WHAT WE CUT (AND WHY)

1. **Remote Credit Bureau APIs:**
   - Cut to protect borrower privacy and preserve zero-footprint self-assessment. External bureau pulls trigger hard inquiries on credit reports, dragging down the borrower's CIBIL score.
2. **Machine Learning / Neural Networks:**
   - Cut in favor of deterministic financial formulas. In credit negotiations, explainability is everything: a borrower cannot argue with a bank manager by citing black-box neural network weights.
3. **Heavy Database Backends:**
   - Cut in favor of pure in-memory state. Zero database means zero maintenance, zero vulnerability to data breaches, and instant startup in any environment.

---
*End of WALKTHROUGH.md.*
