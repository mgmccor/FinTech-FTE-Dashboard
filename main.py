from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.requests import Request
from jinja2 import Environment, FileSystemLoader
import json
from datetime import datetime

app = FastAPI(title="FinTech FTE Dashboard")
env = Environment(loader=FileSystemLoader("templates"))

# FTE Data from Confluence
DATA = {
    "period": "02/24/2026",
    "total_product_fte": 1542.49,
    "total_initiative_fte": 1407.00,
    "discrepancy": 135.49,
    "roles": [
        {"name": "Engineering", "fte": 1091.98, "percent": 70.94},
        {"name": "Product Manager", "fte": 139.66, "percent": 9.05},
        {"name": "Finance/SME", "fte": 97.95, "percent": 6.35},
        {"name": "Quality Assurance", "fte": 75.63, "percent": 4.90},
        {"name": "Data Engineer", "fte": 50.75, "percent": 3.29},
        {"name": "UX/Design", "fte": 38.00, "percent": 2.46},
        {"name": "Program Manager", "fte": 31.65, "percent": 2.05},
        {"name": "Support/Operations", "fte": 10.25, "percent": 0.66},
        {"name": "DevOps/Infrastructure", "fte": 3.50, "percent": 0.23},
        {"name": "Security", "fte": 2.00, "percent": 0.13},
        {"name": "Other", "fte": 0.50, "percent": 0.03},
        {"name": "Enterprise Architect", "fte": 0.62, "percent": 0.04},
    ],
    "product_areas": [
        {
            "name": "Commercial Finance",
            "fte": 477.55,
            "percent": 30.96,
            "products": [
                {"name": "Invoice Management", "fte": 185.30},
                {"name": "Expense Management", "fte": 156.80},
                {"name": "GL Integration", "fte": 92.45},
                {"name": "Other", "fte": 43.00},
            ]
        },
        {
            "name": "Finance Retail Enablement",
            "fte": 431.59,
            "percent": 27.98,
            "products": [
                {"name": "Retail Analytics", "fte": 198.75},
                {"name": "Store Operations Finance", "fte": 167.30},
                {"name": "Inventory Finance", "fte": 65.54},
            ]
        },
        {
            "name": "SAP Finance",
            "fte": 274.03,
            "percent": 17.77,
            "products": [
                {"name": "SAP Integration", "fte": 156.20},
                {"name": "SAP Optimization", "fte": 117.83},
            ]
        },
        {
            "name": "Indirect Procurement",
            "fte": 214.26,
            "percent": 13.89,
            "products": [
                {"name": "Procurement Platform", "fte": 214.26},
            ]
        },
        {
            "name": "Central Item Level Ledger",
            "fte": 95.71,
            "percent": 6.20,
            "products": [
                {"name": "CILL Core", "fte": 95.71},
            ]
        },
        {
            "name": "FinTech Admin",
            "fte": 37.35,
            "percent": 2.42,
            "products": [
                {"name": "Administrative", "fte": 37.35},
            ]
        },
        {
            "name": "FinTech UX",
            "fte": 12.00,
            "percent": 0.78,
            "products": [
                {"name": "Design System", "fte": 12.00},
            ]
        },
    ],
    "top_initiatives": [
        {"name": "MX-CAM Financial Transformation", "fte": 219.27, "percent": 15.58},
        {"name": "Continuous Operational Excellence", "fte": 182.74, "percent": 12.99},
        {"name": "Cost Optimization Experience", "fte": 125.02, "percent": 8.89},
        {"name": "Digital Transformation Initiative", "fte": 98.50, "percent": 7.00},
        {"name": "Cloud Migration Program", "fte": 87.30, "percent": 6.21},
        {"name": "Data & Analytics Enhancement", "fte": 76.15, "percent": 5.41},
        {"name": "Process Automation Roadmap", "fte": 65.40, "percent": 4.65},
        {"name": "Platform Modernization", "fte": 54.62, "percent": 3.88},
    ]
}

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

@app.get("/api/data.json")
async def get_data():
    return DATA

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
