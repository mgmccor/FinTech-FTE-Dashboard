from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.requests import Request
from jinja2 import Environment, FileSystemLoader
import json
from datetime import datetime

app = FastAPI(title="FinTech FTE Dashboard")
env = Environment(loader=FileSystemLoader("templates"))

# FTE Data from Confluence (Actual data from page 3374153877)
DATA = {
    "period": "02/24/2026",
    "total_product_fte": 1542.49,
    "total_initiative_fte": 1407.00,
    "discrepancy": 135.49,
    "roles": [
        {"name": "Engineering", "fte": 1094.22, "percent": 70.94},
        {"name": "Engineering Manager", "fte": 107.76, "percent": 6.99},
        {"name": "Product Manager", "fte": 107.70, "percent": 6.98},
        {"name": "Program, Project, Ops", "fte": 66.74, "percent": 4.33},
        {"name": "Operational Support", "fte": 66.20, "percent": 4.29},
        {"name": "Data Scientist", "fte": 51.67, "percent": 3.35},
        {"name": "Sr Dir and Above", "fte": 22.70, "percent": 1.47},
        {"name": "UX & Research", "fte": 12.00, "percent": 0.78},
        {"name": "QE", "fte": 7.00, "percent": 0.45},
        {"name": "Enterprise Architect", "fte": 3.00, "percent": 0.19},
        {"name": "No Role Assigned", "fte": 2.50, "percent": 0.16},
        {"name": "Other", "fte": 1.00, "percent": 0.06},
    ],
    "product_areas": [
        {
            "name": "Commercial Finance",
            "fte": 477.55,
            "percent": 30.96,
            "products": [
                {"name": "FDF - Data Foundations", "fte": 69.82},
                {"name": "FP&A - Intelligent Business Growth", "fte": 71.51},
                {"name": "FDF - Helix", "fte": 49.53},
                {"name": "FDF - Foundational Agentic Stream", "fte": 45.61},
                {"name": "FP&A - Reporting and Analytics", "fte": 53.72},
                {"name": "FDF - Allocation Platform", "fte": 39.19},
                {"name": "FDF - Data Governance and Controls", "fte": 27.15},
                {"name": "FP&A - Finance Data Hub", "fte": 31.67},
                {"name": "FP&A - OneStream", "fte": 21.93},
                {"name": "FDF - Data Consumption Service", "fte": 12.31},
                {"name": "Others", "fte": 57.18},
            ]
        },
        {
            "name": "Finance Retail Enablement",
            "fte": 431.59,
            "percent": 27.98,
            "products": [
                {"name": "Tax - Tax Analytics and Insights", "fte": 51.48},
                {"name": "AP - Upstream Data Processing", "fte": 45.40},
                {"name": "Exceptions, Disputes, Self Service", "fte": 40.56},
                {"name": "Matching & Reconciliation Processes", "fte": 40.79},
                {"name": "Tax - Tax Determination", "fte": 40.57},
                {"name": "Risk - Casualty Claims", "fte": 27.98},
                {"name": "ACCTG - General Ledger", "fte": 30.83},
                {"name": "Treasury & FinTech Platform Agents", "fte": 20.88},
                {"name": "Others", "fte": 93.10},
            ]
        },
        {
            "name": "SAP Finance",
            "fte": 274.03,
            "percent": 17.77,
            "products": [
                {"name": "SAP Accounts Payable", "fte": 45.91},
                {"name": "SAP Application Security", "fte": 30.10},
                {"name": "SAP Basis", "fte": 27.35},
                {"name": "SAP Enterprise Asset Management", "fte": 29.78},
                {"name": "SAP Extended Warehouse Management", "fte": 18.09},
                {"name": "SAP Accounts Receivable", "fte": 26.81},
                {"name": "SAP General Ledger", "fte": 20.75},
                {"name": "Others", "fte": 75.23},
            ]
        },
        {
            "name": "Indirect Procurement",
            "fte": 214.26,
            "percent": 13.89,
            "products": [
                {"name": "SAP-GNFR-ECC-S4", "fte": 58.63},
                {"name": "MyGNFR Ordering Web / Mobile", "fte": 27.24},
                {"name": "MyGNFR Expense", "fte": 20.70},
                {"name": "MyGNFR Invoicing (iP2P)", "fte": 19.10},
                {"name": "MyGNFR Catalog (iCatalog)", "fte": 14.87},
                {"name": "GNFR Datalake", "fte": 12.41},
                {"name": "Others", "fte": 61.31},
            ]
        },
        {
            "name": "Central Item Level Ledger",
            "fte": 95.71,
            "percent": 6.20,
            "products": [
                {"name": "FDF - Ledger Service", "fte": 37.82},
                {"name": "SAP Master Data Governance Finance", "fte": 17.46},
                {"name": "FP&A - SAP Business Intelligence", "fte": 23.87},
                {"name": "Location MDM", "fte": 16.56},
            ]
        },
        {
            "name": "FinTech Admin",
            "fte": 37.35,
            "percent": 2.42,
            "products": [
                {"name": "FinTech Administration", "fte": 32.35},
                {"name": "FinTech Excellence Analytics", "fte": 5.00},
            ]
        },
        {
            "name": "FinTech UX",
            "fte": 12.00,
            "percent": 0.78,
            "products": [
                {"name": "FinTech UX & Design", "fte": 12.00},
            ]
        },
    ],
    "top_initiatives": [
        {"id": "fintech-003", "name": "FINTECH: Deliver MX-CAM Financial Transformation", "fte": 219.27, "percent": 15.58, "description": "Modernize Mexico and Central America finance platforms and processes to create a simpler, finance grade backbone that scales. This includes the Finance 2.0 program elements like S4 enablement, common e invoicing capabilities, master data readiness, and the integrations required to eliminate brittle middleware dependencies. It also supports regional adoption of global tools such as MyGNFR and standard invoicing, enabling more consistent controls and reporting across MX and CAM. Benefits: faster and more reliable close and reporting, reduced integration and operational risk, and a foundation that supports market growth with fewer one off fixes."},
        {"id": "fintech-012", "name": "FINTECH: Deliver Continuous Operational Excellence", "fte": 182.74, "percent": 12.99, "description": "Deliver continuous operational excellence across the finance product portfolio through disciplined sustainment and reliability practices. Covers tech debt and vulnerability remediation, end to end test support, smaller enhancements, incident triage and resolution, and ongoing platform hygiene such as certificate updates and access renewals. This ensures critical finance capabilities remain stable and performant while major transformations are underway. Benefits: fewer production issues, faster recovery when incidents occur, reduced compliance risk, and more predictable delivery for business partners."},
        {"id": "fintech-002", "name": "FINTECH: Deliver Cost Optimization Experience", "fte": 125.02, "percent": 8.89, "description": "Deliver a unified cost optimization experience for associates and business partners by standardizing indirect procurement and expense workflows on common platforms. Includes launching GENIE and IDEA to automate support and contract intelligence, expanding MyGNFR, Catalog, and Concur, and improving ApprovalHub and GNFR data products for better visibility and governance. Also covers targeted process and platform improvements that close financial integrity gaps across real estate and ERP related procurement flows. Benefits: lower cost to serve through automation, clearer spend and contract insights for better savings decisions, and a smoother associate experience from request to payment."},
        {"id": "fintech-001", "name": "FINTECH: Reduce Supplier Friction (payments & collections)", "fte": 113.08, "percent": 8.04, "description": "Reduce supplier friction across the end to end invoice to pay and bill to cash lifecycle for GFR and GNFR. This work strengthens supplier payment accuracy and transparency, modernizes disputes and collections, and improves upstream imports and matching signals so issues are prevented not worked downstream. Includes supplier self service and explainability experiences, payables and receivables workflow automation, and post payment audit integration to accelerate recoveries. Benefits: fewer exceptions and inquiries, faster on time payments and collections, lower manual effort, and improved supplier and merchant trust."},
        {"id": "fintech-008", "name": "FINTECH: Improve Budgeting, Forecasting, and Analytic Capabilities", "fte": 112.81, "percent": 8.02, "description": "Improve budgeting, forecasting, and analytics by connecting forecasting and planning platforms to the signals that drive business performance. This includes scaling Forecast Intelligence (F1), progressing the future of OneStream and planning migrations, expanding Walmart Machine Learning for forecasting baselines, and strengthening BI reporting and total cost of ownership insights. The focus is on better scenario and driver modeling, clearer governance, and more automation so teams spend less time reconciling and more time acting. Benefits: higher forecast accuracy, faster planning cycles, better capital and spend decisions, and reduced manual effort across finance and business teams."},
        {"id": "fintech-006", "name": "FINTECH: Deliver Unified Financial Flow", "fte": 111.98, "percent": 7.96, "description": "Deliver a unified financial flow that moves the enterprise toward a single, trusted source of finance grade data at the right grain and frequency. Includes MetaHub for master data governance, Helix plus DoP standards for compliant data logistics, and unified accounting and reconciliation services that reduce parallel pipelines and manual matching. The program also advances Digital Accountant capabilities to automate validation and close activities across finance operations. Benefits: higher data trust and faster decision making, increased auto reconciliation, fewer manual adjustments, and a faster, more reliable close."},
        {"id": "fintech-005", "name": "FINTECH: Deliver Tax Transformation and Modernization", "fte": 87.15, "percent": 6.19, "description": "Modernize enterprise tax capabilities across management, exemption, determination, compliance, and analytics to keep pace with omni channel growth and changing regulations. Includes advancing Tax Mod and related item categorization and determination services, expanding Omni Tax Exemption capabilities, and improving audit and compliance tooling and reporting. Also covers foundational upgrades such as Vertex modernization and targeted regulatory readiness work across markets. Benefits: more accurate and consistent tax outcomes, lower audit and compliance risk, reduced manual touch points for tax ops, and better customer and associate experiences at checkout and onboarding."},
        {"id": "fintech-010", "name": "FINTECH: Deliver Agentic AI Strategy", "fte": 46.86, "percent": 3.33, "description": "Deliver a unified agentic AI strategy for finance that makes agents discoverable, governable, and reusable across the portfolio. Includes an open agent and tool registry, semantic routing aligned to finance user personas and access controls, and a standardized evaluation framework to monitor quality and performance. This work enables knowledge agents and process agents to be deployed safely inside existing workflows while improving consistency and auditability. Benefits: faster delivery of AI powered experiences, reduced duplicated builds across teams, stronger controls, and measurable productivity gains for associates."},
    ]
}

# Business unit breakdown for reference
BUSINESS_UNITS = [
    {"name": "Enterprise Business Services", "fte": 1391.77, "percent": 98.92},
    {"name": "U.S. Omni Tech", "fte": 5.12, "percent": 0.36},
    {"name": "Technology Platform", "fte": 3.87, "percent": 0.28},
    {"name": "International Tech", "fte": 1.99, "percent": 0.14},
    {"name": "Sams Club Tech", "fte": 1.00, "percent": 0.07},
    {"name": "Information Security", "fte": 0.25, "percent": 0.02},
]

@app.get("/", response_class=HTMLResponse)
async def get_dashboard():
    template = env.get_template("index.html")
    return template.render(data=DATA)

@app.get("/api/roles", response_class=HTMLResponse)
async def get_roles():
    template = env.get_template("roles.html")
    return template.render(roles=DATA["roles"])

@app.get("/api/products", response_class=HTMLResponse)
async def get_products():
    template = env.get_template("products.html")
    return template.render(product_areas=DATA["product_areas"])

@app.get("/api/initiatives", response_class=HTMLResponse)
async def get_initiatives():
    template = env.get_template("initiatives.html")
    return template.render(initiatives=DATA["top_initiatives"])

@app.get("/api/business-units", response_class=HTMLResponse)
async def get_business_units():
    template = env.get_template("business-units.html")
    return template.render(business_units=BUSINESS_UNITS)

@app.get("/api/data.json")
async def get_data():
    data = DATA.copy()
    data["business_units"] = BUSINESS_UNITS
    return data

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
