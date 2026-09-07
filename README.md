# Borrower Copilot

> **Pre-Lender Underwriting Self-Assessment for Indian Retail Borrowers**  
> *Lokta · Build Challenge · Version 1.0*

A zero-database, zero-API, deterministic borrowing copilot that empowers Indian borrowers before they walk into a lender. It answers the four core borrowing questions:
1. **Should I borrow at all?** ($O_1$: Recommendation Verdict)
2. **How much am I really eligible for?** ($O_2$: Lender Max Sanction vs. Borrower Safe Limit, with explicit guidance on which to use)
3. **What is a fair rate for me?** ($O_3$: Fair Interest Rate Band & All-In APR with 18% GST)
4. **What EMI should I agree to?** ($O_4$: Monthly Safe Ceiling, Tenure Trade-Offs, and Dual Macroeconomic Stress Shock)
5. **The Mobile Negotiation Card:** An in-branch cheat sheet with target anchors, borrower leverage points, bank traps to reject, and a verbatim spoken counter-script.

---

## ⚡ Quickstart (Run Locally in Under 2 Minutes)

### Prerequisites
* Python 3.10+ installed on your system.

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Launch the Application
```bash
python -m streamlit run app.py
```
The interactive application will automatically open in your browser at `http://localhost:8501`.

### 3. Run Automated Unit Tests
```bash
python -m unittest tests/test_personas.py
```
All 7 unit tests validate Priya, Ravi, Anita, confidence progression, and non-zero unknown credit score modeling.

---

## 🚀 Cloud Deployment (Render with Auto-Deploy)

This repository includes a native [`render.yaml`](render.yaml) blueprint for continuous deployment on [Render](https://render.com). Every commit pushed to GitHub automatically triggers a zero-downtime rebuild and redeploy.

### Deployment Settings
* **Service Type:** Web Service
* **Runtime:** Python 3.10+
* **Build Command:** `pip install -r requirements.txt`
* **Start Command:** `streamlit run app.py --server.port $PORT --server.address 0.0.0.0 --server.enableCORS false --server.enableXsrfProtection false`
* **Auto-Deploy:** Enabled (triggers on push to `main`)

---

## 📁 Repository Deliverables Mapping

| Deliverable | File Path | Description |
| :--- | :--- | :--- |
| **Deliverable 1: Working App** | [`app.py`](file:///c:/Users/soumy/OneDrive/Desktop/lending%20copilot/app.py) | Interactive web interface styled with the Lokta design system (Imperial Plum `#4B2440`, warm canvas, pill buttons, info tooltips, live confidence gauge, paired two-fold cards, and mobile negotiation card). |
| **Deliverable 2: Rulebook** | [`RULES.md`](file:///c:/Users/soumy/OneDrive/Desktop/lending%20copilot/RULES.md) | Comprehensive table cataloguing every rule, threshold, product band, stress shock, and regulatory source. |
| **Deliverable 3: 3 Run-Throughs** | [`tests/test_personas.py`](file:///c:/Users/soumy/OneDrive/Desktop/lending%20copilot/tests/test_personas.py) & [`WALKTHROUGH.md`](file:///c:/Users/soumy/OneDrive/Desktop/lending%20copilot/WALKTHROUGH.md) | End-to-end question paths, calculations, outputs, and Negotiation Cards for Priya, Ravi, and Anita. |
| **Deliverable 4: 5-Min Walkthrough** | [`WALKTHROUGH.md`](file:///c:/Users/soumy/OneDrive/Desktop/lending%20copilot/WALKTHROUGH.md) | Written walkthrough of architecture, how the 5 challenge rules were satisfied, what to build next, and what was cut. |
| **Master Technical Spec** | [`ARCHITECTURE_AND_SPECIFICATION.md`](file:///c:/Users/soumy/OneDrive/Desktop/lending%20copilot/ARCHITECTURE_AND_SPECIFICATION.md) | Complete system architecture, mathematical formulas, and underwriting logic. |
| **Code File Map** | [`PROJECT_STRUCTURE_AND_FILES.md`](file:///c:/Users/soumy/OneDrive/Desktop/lending%20copilot/PROJECT_STRUCTURE_AND_FILES.md) | Granular component breakdown, input/output contracts, and cross-file execution flows. |

---

## 🎯 The Three Verified Personas (One-Click Quick Load)

Click any persona button at the top of the app to populate inputs instantly:

### 1. Priya (29, Bengaluru · Salaried MNC Professional)
* **Profile:** Net ₹1,10,000/mo, Car loan ₹14,000/mo, Rent ₹28,000, Living ₹25,000, 780 CIBIL, 5 yrs at Tier-1 MNC.
* **Loan Wanted:** ₹8,00,000 for wedding over 48 months.
* **Outputs:**
  * **$O_1$ (Verdict):** `BORROW` (Requested ₹20,690 EMI fits comfortably within ₹37,500 safe ceiling).
  * **$O_2$ (Limits):** Lender Sanction: **₹18.1L** vs. Safe Limit: **₹14.6L** $\rightarrow$ **Use Your Safe Limit (₹14.6L)**.
  * **$O_3$ (Rate & APR):** Fair Rate: **10.50% – 11.25%** | True All-In APR: **11.65%** (With 1.0% fee + 18% GST).
  * **$O_4$ (Monthly Ceiling):** **₹37,500/month** (Survives 20% income shock: stress ratio is 39.4% $\le$ 65%).

### 2. Ravi (42, Mysuru · Self-Employed Kirana Store Owner)
* **Profile:** Cash income ₹85,000/mo, ITR ₹4,20,000/yr, Unscored CIBIL, Living ₹28,000, Owns shop worth ₹45,00,000 unencumbered. Wife earns ₹18,000 teaching.
* **Loan Wanted:** ₹15,00,000 for stock line and delivery vehicle over 84 months.
* **Outputs:**
  * **The Product Pivot:** Pledging the unencumbered shop pivots Ravi from high-risk 18%+ unsecured credit into **Loan Against Property (LAP)**.
  * **$O_1$ (Verdict):** `BORROW` (Requested ₹24,900 EMI fits well within low-season cash flows).
  * **$O_2$ (Limits):** Lender LAP Sanction: **₹22.5L** vs. Safe Limit: **₹21.0L** $\rightarrow$ **Use Your Safe Limit (₹21.0L)**.
  * **$O_3$ (Rate & APR):** Fair Rate: **9.75% – 10.50%** | True All-In APR: **10.85%**.
  * **$O_4$ (Monthly Ceiling):** **₹42,500/month** (Anchored to business low season).

### 3. Anita (35, Hubballi · Informal Delivery Fleet Partner)
* **Profile:** Delivery rider plus tailoring. Net ₹28,000/mo, 2 kids, husband unemployed 8 months. 3 active digital app loans totaling ₹35,000 at 36% APR. 1 auto-debit bounce last month.
* **Loan Wanted:** ₹1,50,000 for commercial electric scooter (saves ₹3,500/mo on petrol).
* **Outputs:**
  * **Kill-Switch Active:** Auto-debit bounce $\ge 1$ and predatory app debt $>24\%$ APR immediately trigger `DON'T BORROW`.
  * **$O_1$ (Verdict):** `DON'T BORROW` (*"Why: An auto-debit bounce in the last 6 months and active high-cost app debt (36% APR) flag acute distress; adding new debt before clearing arrears creates severe insolvency risk."*).
  * **$O_2$ (Limits):** Lender Sanction: **₹0** | Safe Limit: **₹0** (Blocked until app loans are restructured).
  * **$O_3$ (Rate & APR):** Fair Commercial EV Rate: **11.50% – 13.00%** vs. Current App Rate: **36.00% APR**.
  * **$O_4$ (Monthly Ceiling):** **₹3,500/month** (Requires app debt clearance before onboarding).

---

## 🏛️ System Architecture

```
lending-copilot/
│
├── app.py                              # Presentation Layer (Streamlit, Lokta UI Design System)
├── requirements.txt                    # Python dependencies
├── RULES.md                            # Complete Underwriting Rulebook & Assumptions Registry
├── WALKTHROUGH.md                      # 5-Minute Technical & Design Walkthrough
├── README.md                           # Quickstart and Documentation
│
├── engine/                             # Core Deterministic Python Engine (Zero DB / Zero API)
│   ├── __init__.py                     # Clean package exports
│   ├── underwriting.py                 # PMT, PV, Newton-Raphson APR/IRR, FOIR, Limits, Dual Stress
│   ├── confidence.py                   # Master question matrix, category branching, confidence scoring (60%-95%)
│   ├── explanations.py                 # Deterministic bottleneck priority trees & Rule 4 "Why" generators
│   └── negotiation.py                  # Tactical Negotiation Card & verbatim spoken counter-script
│
└── tests/
    ├── __init__.py
    └── test_personas.py                # Automated Persona Unit Tests (Priya, Ravi, Anita)
```

---

## ⚖️ Five Codified Judging Rules
1. **Adaptive:** A salaried corporate employee and a kirana shopkeeper see different, tailored question sets.
2. **Confidence Widens with Silence:** Answering only 10 mandatory questions yields 60.0% base confidence and wide rate bands ($\pm 2.35\%$). Answering category variables tightens bands to $\pm 0.35\%$ and climbs to 95.0% max.
3. **Unknown is Never Zero:** An unverified credit score is modeled as an unrated risk band ($\pm 2.0\%$) and never penalized as a subprime default ($0$ or $300$).
4. **Every Number Has a Why:** Every output is paired with a single plain-English diagnostic sentence explaining which financial bottleneck bounded that number.
5. **India in Rupees:** Incorporates Fixed Obligation to Income Ratios (FOIR), statutory 18% GST on processing fees, Loan Against Property (LAP), and commercial EV priority benchmarks.
