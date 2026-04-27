# 🛒 E-commerce Funnel Analysis

An end-to-end data analysis project that identifies user drop-off points in an e-commerce purchase funnel and quantifies the business impact of improving conversion rates.

**[▶ Live App](https://ecommerce-funnel-analysis-live.streamlit.app/)** · **[📓 Analysis Notebook](analysis.ipynb)**

---

## 📌 Project Summary

Most e-commerce businesses lose users silently — between the moment a product is viewed and the moment it is purchased. This project analyses 885,000+ real user events to find exactly where and why that drop-off happens, then simulates the revenue impact of fixing it.

### Key Findings

| Metric | Value |
|---|---|
| View → Cart conversion | **7.6%** |
| Cart → Purchase conversion | **63.8%** |
| Average Order Value (from data) | **$135.28** |
| Primary bottleneck | **Top-of-funnel engagement** |
| Revenue gain at 12% VTC target | **~$63,800** |

The data tells a clear story: the checkout process works well (63.8% cart-to-purchase). The problem is earlier — users are browsing but not engaging. Improving view-to-cart conversion from 7.6% to 12% could generate approximately 471 additional purchases and ~$63,800 in revenue on this sample alone.

---

## 📁 Project Structure

```
ecommerce-funnel-analysis/
│
├── data/
│   └── raw and cleaned data/
│       ├── events.csv              # Full dataset: 885K events
│       └── funnel_small.csv        # Cleaned 20K sample used in Streamlit app
│
├── analysis.ipynb                  # Full EDA, funnel metrics, revenue simulation
├── app.py                          # Streamlit interactive dashboard
├── funnel_analysis.pbix            # Power BI dashboard
└── README.md
```

---

## 🔍 What This Project Covers

### 1. Data Cleaning & Validation
- Handled missing `category_code` values
- Validated event types and removed duplicates
- Parsed datetime with timezone awareness
- Fixed day-of-week ordering for correct chronological charts

### 2. User-Level Funnel Analysis
Measured the funnel at the **user level** (not event level) — tracking whether each unique user viewed, carted, and purchased — to avoid inflating metrics from repeated actions.

### 3. Category Performance
Identified which product categories have high traffic but low conversion, and which have high average order values — revealing where optimisation investment would have the most impact.

### 4. Time-Based Analysis
Analysed conversion rates by hour of day and day of week. Peak traffic hours (afternoon) do not correspond to peak conversion — users are browsing, not buying.

### 5. Data-Driven Revenue Simulation
Used the **actual average order value ($135.28)** calculated from real purchase events — not an assumed figure — to model three realistic improvement scenarios.

| Scenario | Target VTC | Extra Purchases | Revenue Gain |
|---|---|---|---|
| Conservative (9.5%) | +25% improvement | ~143 | ~$19,300 |
| Target (12%) | +58% improvement | ~471 | ~$63,800 |
| Optimistic (15%) | +100% improvement | ~920 | ~$124,500 |

---

## 🖥 Streamlit App Features

The interactive app allows anyone — analyst or stakeholder — to explore the data without code.

- **Funnel Overview** — KPI cards for views, carts, purchases, and conversion rates
- **Category Filter** — Drill into specific product categories
- **Time Range Filter** — Restrict analysis to specific hours of the day
- **Top/Worst Category Charts** — See which categories convert best and worst
- **Hourly Conversion Chart** — Identify high-intent hours vs. browsing hours
- **Business Impact Simulator** — Drag a slider to set a target conversion rate and see the estimated additional purchases in real time

### Screenshots

> *(Add screenshots here: funnel overview, category performance, business impact slider)*  
> Suggested: `docs/screenshots/funnel_overview.png`, `docs/screenshots/category_chart.png`, `docs/screenshots/simulator.png`

---

## 📊 Power BI Dashboard

The Power BI file (`funnel_analysis.pbix`) contains three pages:

1. **Funnel Overview** — Overall conversion metrics and funnel visualisation
2. **Category Performance** — Conversion rates and revenue by product category
3. **Time Trends** — Hourly and daily activity and conversion patterns

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.8+
- pip

### Install Dependencies

```bash
pip install streamlit pandas plotly
```

### Run the Streamlit App

```bash
# Clone the repo
git clone https://github.com/your-username/ecommerce-funnel-analysis.git
cd ecommerce-funnel-analysis

# Run the app
streamlit run app.py
```

The app reads from `data/raw and cleaned data/funnel_small.csv`. Make sure the data folder is present.

### Run the Notebook

```bash
pip install jupyter pandas numpy matplotlib seaborn plotly
jupyter notebook analysis.ipynb
```

---

## 🗂 Dataset

**Source:** [REES46 E-commerce Dataset — Kaggle](https://www.kaggle.com/datasets/mkechinov/ecommerce-behavior-data-from-multi-category-store)

| Column | Description |
|---|---|
| `event_time` | Timestamp of the user action |
| `event_type` | `view`, `cart`, or `purchase` |
| `product_id` | Unique product identifier |
| `category_code` | Product category (e.g. `electronics.telephone`) |
| `brand` | Product brand |
| `price` | Product price in USD |
| `user_id` | Unique user identifier |
| `user_session` | Session identifier |

**Size:** 885,129 rows · 9 columns  
**Period:** Sep 2020 – Jan 2021  
The analysis notebook works on a reproducible 20,000-row sample (`random_state=42`) for speed. The Streamlit app uses the same sample.

---

## 💡 Business Recommendations

1. **Improve product pages** — Better images, clearer descriptions, and visible reviews directly address the view → cart gap
2. **Optimise pricing for high-traffic, low-conversion categories** — A/B test discounts or bundles where views are high but purchases are low
3. **Add trust signals** — Ratings, return policy, and secure payment badges reduce hesitation at the product page
4. **Target high-intent hours** — Run promotions during hours where conversion rate is elevated, not just where traffic is highest
5. **Don't over-invest in checkout** — With 63.8% cart-to-purchase, the checkout process is already efficient; resources are better spent earlier in the funnel

---

## 🛠 Tools & Technologies

| Tool | Purpose |
|---|---|
| Python (Pandas, NumPy) | Data cleaning, EDA, funnel metrics |
| Plotly / Matplotlib | Visualisations in notebook |
| Streamlit | Interactive web application |
| Power BI (DAX) | Stakeholder-facing dashboard |
| Git / GitHub | Version control |

---

## 👩‍💻 Author

**Sahana L**  
Data Analyst · Python · SQL · Power BI  
[LinkedIn](https://www.linkedin.com/in/sahana-l-37543a323/) · [GitHub](https://github.com/sana23-ship)
