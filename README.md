# FinTech FTE Dashboard 📊

An interactive dashboard displaying FinTech Product & Initiative FTE (Full-Time Equivalent) Allocations as of **02/24/2026**.

## 🚀 View the Dashboard

**Live Dashboard:** https://mgmccor.github.io/FinTech-FTE-Dashboard/

Just click the link above to see the interactive dashboard in your browser. No installation required!

## 📈 What's Inside

The dashboard provides comprehensive FTE allocation data across:

- **👥 Roles** - 12 role categories showing distribution across Engineering (70.94%), Management, Product, and Support functions
- **📊 Products** - 7 product areas with 50+ sub-products:
  - Commercial Finance (30.96%)
  - Finance Retail Enablement (27.98%)
  - SAP Finance (17.77%)
  - Indirect Procurement (13.89%)
  - Central Item Level Ledger (6.20%)
  - FinTech Admin & UX (3.20%)

- **🚀 Initiatives** - Top 8+ strategic initiatives with FTE allocations:
  - MX-CAM Financial Transformation (219.27 FTEs)
  - Continuous Operational Excellence (182.74 FTEs)
  - Cost Optimization Experience (125.02 FTEs)
  - And more...

- **🏢 Business Units** - Distribution across organizational units with Enterprise Business Services representing 98.92% of initiative resources

## 📊 Key Metrics

| Metric | Value |
|--------|-------|
| **Total Product FTEs** | 1,542.49 |
| **Total Initiative FTEs** | 1,407.00 |
| **FTE Discrepancy** | 135.49 |
| **Period Ending** | 02/24/2026 |

## ✨ Features

✅ **Interactive Tabs** - Switch between Roles, Products, Initiatives, and Business Units  
✅ **Visual Charts** - Doughnut and bar charts with Walmart brand colors  
✅ **Detailed Tables** - Complete FTE breakdown with percentages  
✅ **Progress Bars** - Visual allocation distribution  
✅ **Executive Insights** - Key takeaways for each section  
✅ **Responsive Design** - Works on desktop, tablet, and mobile  
✅ **No Server Required** - Pure HTML/CSS/JavaScript  

## 📁 File Structure

```
├── index.html                      # Main dashboard (GitHub Pages default)
├── FinTech-FTE-Dashboard.html      # Standalone shareable version
├── main.py                         # FastAPI backend (optional)
├── requirements.txt                # Python dependencies
├── templates/                      # FastAPI templates
│   ├── index.html
│   ├── roles.html
│   ├── products.html
│   ├── initiatives.html
│   └── business-units.html
└── README.md                       # This file
```

## 🛠️ How to Use

### View Online (Easiest)
1. Go to: https://mgmccor.github.io/FinTech-FTE-Dashboard/
2. Click through the tabs to explore data
3. Share the link with others!

### Download & Use Offline
1. Download `FinTech-FTE-Dashboard.html` from this repo
2. Open it in any web browser
3. No internet connection needed after download!

### Run Locally with FastAPI (Optional)
```bash
# Create virtual environment
uv venv
source .venv/bin/activate

# Install dependencies
uv pip install -r requirements.txt

# Run server
python main.py

# Visit http://127.0.0.1:8000
```

## 📚 Data Source

Data extracted from Confluence page: [02/24/26: By The Numbers - FinTech Product & Initiative Allocations](https://confluence.walmart.com/pages/viewpage.action?pageId=3374153877)

## 🎨 Design

Designed with Walmart brand colors:
- **Primary Blue:** #0053e2
- **Spark Yellow:** #ffc220
- **Accessible contrast ratios** for WCAG 2.2 compliance

## 📋 Notes

⚠️ **FTE Discrepancy Alert**: There is a 135.49 FTE difference between Product allocations (1,542.49) and Initiative allocations (1,407.00). This is documented in the source data.

## 🤝 Contributing

To update data:
1. Edit the `ROLES`, `PRODUCT_AREAS`, `TOP_INITIATIVES`, and `BUSINESS_UNITS` data structures in `index.html`
2. Commit and push to GitHub
3. Changes appear automatically on the live site!

## 📝 License

Internal Walmart Use

---

**Created with ❤️ by Code Puppy** 🐕
