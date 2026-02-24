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
        {"name": "Deliver MX-CAM Financial Transformation", "fte": 219.27, "percent": 15.58},
        {"name": "Deliver Continuous Operational Excellence", "fte": 182.74, "percent": 12.99},
        {"name": "Deliver Cost Optimization Experience", "fte": 125.02, "percent": 8.89},
        {"name": "Reduce Supplier Friction (Payments & Collections)", "fte": 113.08, "percent": 8.04},
        {"name": "Improve Budgeting, Forecasting, Analytics", "fte": 112.81, "percent": 8.02},
        {"name": "Deliver Unified Financial Flow", "fte": 111.98, "percent": 7.96},
        {"name": "Deliver Tax Transformation & Modernization", "fte": 87.15, "percent": 6.19},
        {"name": "Deliver Agentic AI Strategy", "fte": 46.86, "percent": 3.33},
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
