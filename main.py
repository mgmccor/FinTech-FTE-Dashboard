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
    "all_initiatives": [
        {"id": "fintech-003", "name": "FINTECH: Deliver MX-CAM Financial Transformation", "fte": 219.27, "percent": 15.58, "description": "Modernize Mexico and Central America finance platforms and processes to create a simpler, finance grade backbone that scales. This includes the Finance 2.0 program elements like S4 enablement, common e invoicing capabilities, master data readiness, and the integrations required to eliminate brittle middleware dependencies. It also supports regional adoption of global tools such as MyGNFR and standard invoicing, enabling more consistent controls and reporting across MX and CAM. Benefits: faster and more reliable close and reporting, reduced integration and operational risk, and a foundation that supports market growth with fewer one off fixes."},
        {"id": "fintech-012", "name": "FINTECH: Deliver Continuous Operational Excellence", "fte": 182.74, "percent": 12.99, "description": "Deliver continuous operational excellence across the finance product portfolio through disciplined sustainment and reliability practices. Covers tech debt and vulnerability remediation, end to end test support, smaller enhancements, incident triage and resolution, and ongoing platform hygiene such as certificate updates and access renewals. This ensures critical finance capabilities remain stable and performant while major transformations are underway. Benefits: fewer production issues, faster recovery when incidents occur, reduced compliance risk, and more predictable delivery for business partners."},
        {"id": "fintech-002", "name": "FINTECH: Deliver Cost Optimization Experience", "fte": 125.02, "percent": 8.89, "description": "Deliver a unified cost optimization experience for associates and business partners by standardizing indirect procurement and expense workflows on common platforms. Includes launching GENIE and IDEA to automate support and contract intelligence, expanding MyGNFR, Catalog, and Concur, and improving ApprovalHub and GNFR data products for better visibility and governance. Also covers targeted process and platform improvements that close financial integrity gaps across real estate and ERP related procurement flows. Benefits: lower cost to serve through automation, clearer spend and contract insights for better savings decisions, and a smoother associate experience from request to payment."},
        {"id": "fintech-001", "name": "FINTECH: Reduce Supplier Friction (payments & collections)", "fte": 113.08, "percent": 8.04, "description": "Reduce supplier friction across the end to end invoice to pay and bill to cash lifecycle for GFR and GNFR. This work strengthens supplier payment accuracy and transparency, modernizes disputes and collections, and improves upstream imports and matching signals so issues are prevented not worked downstream. Includes supplier self service and explainability experiences, payables and receivables workflow automation, and post payment audit integration to accelerate recoveries. Benefits: fewer exceptions and inquiries, faster on time payments and collections, lower manual effort, and improved supplier and merchant trust."},
        {"id": "fintech-008", "name": "FINTECH: Improve Budgeting, Forecasting, and Analytic Capabilities", "fte": 112.81, "percent": 8.02, "description": "Improve budgeting, forecasting, and analytics by connecting forecasting and planning platforms to the signals that drive business performance. This includes scaling Forecast Intelligence (F1), progressing the future of OneStream and planning migrations, expanding Walmart Machine Learning for forecasting baselines, and strengthening BI reporting and total cost of ownership insights. The focus is on better scenario and driver modeling, clearer governance, and more automation so teams spend less time reconciling and more time acting. Benefits: higher forecast accuracy, faster planning cycles, better capital and spend decisions, and reduced manual effort across finance and business teams."},
        {"id": "fintech-006", "name": "FINTECH: Deliver Unified Financial Flow", "fte": 111.98, "percent": 7.96, "description": "Deliver a unified financial flow that moves the enterprise toward a single, trusted source of finance grade data at the right grain and frequency. Includes MetaHub for master data governance, Helix plus DoP standards for compliant data logistics, and unified accounting and reconciliation services that reduce parallel pipelines and manual matching. The program also advances Digital Accountant capabilities to automate validation and close activities across finance operations. Benefits: higher data trust and faster decision making, increased auto reconciliation, fewer manual adjustments, and a faster, more reliable close."},
        {"id": "fintech-005", "name": "FINTECH: Deliver Tax Transformation and Modernization", "fte": 87.15, "percent": 6.19, "description": "Modernize enterprise tax capabilities across management, exemption, determination, compliance, and analytics to keep pace with omni channel growth and changing regulations. Includes advancing Tax Mod and related item categorization and determination services, expanding Omni Tax Exemption capabilities, and improving audit and compliance tooling and reporting. Also covers foundational upgrades such as Vertex modernization and targeted regulatory readiness work across markets. Benefits: more accurate and consistent tax outcomes, lower audit and compliance risk, reduced manual touch points for tax ops, and better customer and associate experiences at checkout and onboarding."},
        {"id": "fintech-010", "name": "FINTECH: Deliver Agentic AI Strategy", "fte": 46.86, "percent": 3.33, "description": "Deliver a unified agentic AI strategy for finance that makes agents discoverable, governable, and reusable across the portfolio. Includes an open agent and tool registry, semantic routing aligned to finance user personas and access controls, and a standardized evaluation framework to monitor quality and performance. This work enables knowledge agents and process agents to be deployed safely inside existing workflows while improving consistency and auditability. Benefits: faster delivery of AI powered experiences, reduced duplicated builds across teams, stronger controls, and measurable productivity gains for associates."},
        {"name": "FINTECH: FPA Finance Data Hub-Platform Interface", "fte": 24.77, "percent": 1.76},
        {"name": "FINTECH: FDF-Data Allocation Engine", "fte": 21.68, "percent": 1.54},
        {"name": "FINTECH: GNFR Procurement - Travel and Expense Management", "fte": 20.22, "percent": 1.44},
        {"id": "fintech-007", "name": "FINTECH: Maintain Customer Trust Claims", "fte": 17.66, "percent": 1.26, "description": "Maintain customer trust in claims by modernizing the end to end Walmart Claims Services experience from intake through resolution. Includes improvements to incident intake, evidence capture and retrieval, claims lifecycle workflows, claimant self service, and analytics that strengthen prevention and defense. Where appropriate, AI assisted workflows help reduce manual research and improve consistency in communications and task execution. Benefits: faster resolution and better claimant experience, improved compliance and defensibility, and higher productivity for adjusters and operations teams."},
        {"name": "FINTECH: FDF-WMUS Data Foundation", "fte": 16.28, "percent": 1.16},
        {"name": "FINTECH: FDF-International Data Foundation", "fte": 14.51, "percent": 1.03},
        {"name": "FINTECH: FDF-Finance Data Factory Architecture", "fte": 12.25, "percent": 0.87},
        {"id": "fintech-011", "name": "FINTECH: Deliver Finance Technology Re-Platform", "fte": 11.91, "percent": 0.85, "description": "Re platform core finance technologies by moving legacy infrastructure and dependencies to modern, scalable platforms. Includes mainframe to cloud migrations, SMART modernization, and GTP migrations, along with the engineering work needed to keep critical financial flows stable during transition. The focus is to simplify the landscape, reduce fragility, and create a cleaner foundation for future automation and analytics. Benefits: improved reliability and performance, lower run costs and tech debt, and faster delivery of new capabilities with less operational risk."},
        {"name": "NGTS: Finance 2.0", "fte": 10.96, "percent": 0.78},
        {"name": "FINTECH: FDF-Sam's Data Foundation", "fte": 10.83, "percent": 0.77},
        {"name": "FINTECH: GNFR Procurement - Data Management and Visualization", "fte": 10.81, "percent": 0.77},
        {"name": "FINTECH: FDF-Foundational Agentic Stream", "fte": 10.60, "percent": 0.75},
        {"name": "FINTECH: SAP Accounts Payable Sustain", "fte": 9.93, "percent": 0.71},
        {"name": "FINTECH: FRE-ACCTG-Business Unit Accounting (BUA) Sustain", "fte": 9.17, "percent": 0.65},
        {"name": "FINTECH: FDF-Enterprise Location", "fte": 8.95, "percent": 0.64},
        {"name": "FINTECH: FDF-Digital Data", "fte": 8.73, "percent": 0.62},
        {"name": "FINTECH: FRE-Acctg-Inventory Sustain", "fte": 8.49, "percent": 0.60},
        {"name": "FINTECH: GNFR Procurement - Sustain", "fte": 8.10, "percent": 0.58},
        {"name": "FINTECH: FPA-OneStream-Nexus", "fte": 7.60, "percent": 0.54},
        {"name": "FINTECH: Financial Consolidation and Close (FCCS)", "fte": 6.92, "percent": 0.49},
        {"id": "fintech-013", "name": "FINTECH: Deliver Financial System Governance", "fte": 6.38, "percent": 0.45, "description": "Strengthen financial system governance to ensure audit readiness and regulatory compliance across finance platforms and data. Includes SOX and ITGC support, legal and privacy requests such as CPRA and CCPA, and the controls and reporting needed to demonstrate secure and compliant operations. This work aligns policy, process, and technical controls so governance is consistent across markets and products. Benefits: reduced compliance and audit risk, clearer accountability, and fewer disruptions to business operations during regulatory events."},
        {"name": "FINTECH: FRE-Tax-Tax Modernization", "fte": 6.15, "percent": 0.44},
        {"name": "GNFR Procurement", "fte": 6.00, "percent": 0.43},
        {"name": "FINTECH: FDF-Enterprise Location Sustain", "fte": 5.62, "percent": 0.40},
        {"name": "FINTECH: FDF-WMUS Data Sustain", "fte": 5.57, "percent": 0.40},
        {"name": "FINTECH: FRE-AP-Reports and Analytics - Payables Insights Hub", "fte": 5.19, "percent": 0.37},
        {"name": "FINTECH: FRE-AP-Matching Evolution", "fte": 4.91, "percent": 0.35},
        {"name": "FINTECH: FDF-Master Data Automation", "fte": 4.75, "percent": 0.34},
        {"name": "FINTECH: FDF-Data Allocation Engine Sustain", "fte": 4.48, "percent": 0.32},
        {"id": "fintech-009", "name": "FINTECH: Enable Retail Services to Drive New Revenue Streams", "fte": 4.45, "percent": 0.32, "description": "Enable Retail Services platforms that drive new revenue and reduce leakage by modernizing lottery and add on services capabilities. Includes scaling the Lottery Digital Platform with stronger reconciliation and end of day automation, and expanding Vendor Data Platform APIs so suppliers can access accurate store and dotcom transaction data. Also supports targeted settlement controls and analytics to improve operational decision making and reduce write offs. Benefits: scalable revenue growth, better supplier partnerships through data transparency, and improved control and automation for store and home office teams."},
        {"id": "fintech-004", "name": "FINTECH: Deliver Chile Financial Transformation", "fte": 4.07, "percent": 0.29, "description": "Advance Chile finance transformation by rolling out key enterprise platforms that standardize expense, lease, and omni enablement capabilities. This includes implementing ReimburseMe for expense management, delivering core omni acceleration milestones, and deploying Lucernex to modernize lease accounting and related controls. The intent is to simplify the tool landscape, reduce manual work, and align Chile with global patterns so future upgrades are faster and less risky. Benefits: improved associate experience and control, reduced manual processing and rework, and smoother platform adoption as Chile scales."},
        {"name": "FINTECH: FRE-Risk Casualty Claims-Customer and Associate Portal", "fte": 3.47, "percent": 0.25},
        {"name": "FINTECH: FPA-Total Cost of Ownership (TCO)", "fte": 3.46, "percent": 0.25},
        {"name": "FINTECH: FRE-Risk Casualty Claims Sustain", "fte": 3.20, "percent": 0.23},
        {"name": "(blank)", "fte": 3.00, "percent": 0.21},
        {"name": "FINTECH: FRE-Tax-Tax Exemption-Omni Tax Exemption Enrollment Platform", "fte": 3.00, "percent": 0.21},
        {"name": "FINTECH: FPA Finance Data Hub-Platform Sustain", "fte": 2.90, "percent": 0.21},
        {"name": "FINTECH: FRE-ACCTG-Reconciliations and Accounting Services-MJE Transformation", "fte": 2.80, "percent": 0.20},
        {"name": "FINTECH: SAP General Ledger Sustain", "fte": 2.67, "percent": 0.19},
        {"name": "FINTECH: FRE-ACCTG-Reconciliations and Accounting Services Sustain", "fte": 2.60, "percent": 0.18},
        {"name": "FINTECH: FRE-AP-Reports and Analytics Sustain", "fte": 2.19, "percent": 0.16},
        {"name": "FINTECH: FDF-Corporate Data Foundation", "fte": 2.16, "percent": 0.15},
        {"name": "INVEST: PEOPLE: PAYROLL MONDERNIZATION", "fte": 2.10, "percent": 0.15},
        {"name": "FINTECH: FRE-AR-Invoicing, Collection and Dispute Management Sustain", "fte": 2.10, "percent": 0.15},
        {"name": "FINTECH: GenAI-Platform Agents Sustain", "fte": 2.05, "percent": 0.15},
        {"name": "FINTECH: FRE-Tax-Tax Determination Dotcom Sustain", "fte": 2.00, "percent": 0.14},
        {"name": "FINTECH: Intl Program Management and Tech Ops - Back Office", "fte": 2.00, "percent": 0.14},
        {"name": "FINTECH: FRE-Exceptions, Disputes and Self Service Sustain", "fte": 1.90, "percent": 0.14},
        {"name": "NGTS: MAINFRAME TO CLOUD", "fte": 1.90, "percent": 0.14},
        {"name": "FINTECH: FRE-Acctg-General Ledger Sustain", "fte": 1.89, "percent": 0.13},
        {"name": "FINTECH: FRE-AP-Invoices and Payments Sustain", "fte": 1.80, "percent": 0.13},
        {"name": "FINTECH: Master Data Hub (MetaHub)", "fte": 1.65, "percent": 0.12},
        {"name": "FINTECH: FRE-Risk Casualty Claims-Riskconnect Intake Solution", "fte": 1.63, "percent": 0.12},
        {"name": "FINTECH: FRE-ACCTG-Inventory-GIS 2.0", "fte": 1.61, "percent": 0.11},
        {"name": "FINTECH: FRE-Treasury and Investment Management Sustain", "fte": 1.61, "percent": 0.11},
        {"name": "FINTECH: FRE-ACCTG-External Reporting Sustain", "fte": 1.50, "percent": 0.11},
        {"name": "FY27: Merch: Trust: Merchant Trust: Visibility to metrics, reduce exception-execution via Wally", "fte": 1.47, "percent": 0.10},
        {"name": "FINTECH: FRE-Tax-Tax Exemption Sustain", "fte": 1.40, "percent": 0.10},
        {"name": "FINTECH: FDF-Sam's Data Sustain", "fte": 1.37, "percent": 0.10},
        {"name": "FINTECH: SAP Extended Warehouse Management Sustain", "fte": 1.30, "percent": 0.09},
        {"name": "FINTECH: FRE-AP-Imports - Imports 2.0", "fte": 1.30, "percent": 0.09},
        {"name": "FINTECH: FRE-Disputes and Self Service - AP Disputes", "fte": 1.22, "percent": 0.09},
        {"name": "FINTECH: FRE-Retail Services-Vendor Data Platform Sustain", "fte": 1.20, "percent": 0.09},
        {"name": "FINTECH: FRE-AP-Invoices and Payments - R2P", "fte": 1.16, "percent": 0.08},
        {"name": "FINTECH: FDF-FDLH-Helix Platform Onboarding", "fte": 1.10, "percent": 0.08},
        {"name": "FINTECH:  GenAI-Finance Data Factory (FDF) Insights Engine", "fte": 1.10, "percent": 0.08},
        {"name": "FINTECH: FDF-Digital Data Sustain", "fte": 1.08, "percent": 0.08},
        {"name": "NGTS: SMART Transformation", "fte": 1.05, "percent": 0.07},
        {"name": "FINTECH: FRE-Tax-Tax Determination Brick and Mortar Sustain", "fte": 1.00, "percent": 0.07},
        {"name": "FINTECH: SAPCC-ERP-Application Security Sustain", "fte": 1.00, "percent": 0.07},
        {"name": "EBS FP and A", "fte": 1.00, "percent": 0.07},
        {"name": "Data Ventures: Horizontal Capabilities - Core Services", "fte": 1.00, "percent": 0.07},
        {"name": "FY26: Intl Customer Focus and Growth - SPA Walmart Connect -- Diversify and Expand: Increase Ad Revenue", "fte": 1.00, "percent": 0.07},
        {"name": "EBS: GG Tech: INVEST: Aviation Next Gen", "fte": 1.00, "percent": 0.07},
        {"name": "Modernize Replenishment Planning, Order Management and Inventory systems", "fte": 1.00, "percent": 0.07},
        {"name": "FINTECH: FPA-OneStream-International Applications", "fte": 0.88, "percent": 0.06},
        {"name": "eCommerce: WCP: Foundational Platform", "fte": 0.85, "percent": 0.06},
        {"name": "FINTECH: FRE-Tax-Tax Compliance-Property Tax", "fte": 0.81, "percent": 0.06},
        {"name": "FINTECH: FRE-Acctg-Lease Accounting and Mgmt Sustain", "fte": 0.74, "percent": 0.05},
        {"name": "FY26: Intl Core Supply Chain - Transportation -- Run Business Efficiently: Reduce Transportation Cost", "fte": 0.74, "percent": 0.05},
        {"name": "FINTECH: FDF-International Data Sustain", "fte": 0.65, "percent": 0.05},
        {"name": "FINTECH: FRE-Exceptions, Disputes and Self Service-ResolvHub Platform", "fte": 0.65, "percent": 0.05},
        {"name": "FINTECH: SAP-EAM-Enterprise Asset Management Sustain", "fte": 0.63, "percent": 0.04},
        {"name": "FINTECH: FPA-SAP BI Sustain", "fte": 0.61, "percent": 0.04},
        {"name": "FINTECH: FDF-Data Enablement", "fte": 0.60, "percent": 0.04},
        {"name": "INVEST: PEOPLE: People.Data: Data Enablement", "fte": 0.58, "percent": 0.04},
        {"name": "FINTECH: SAP Accounts Receivable Sustain", "fte": 0.55, "percent": 0.04},
        {"name": "FINTECH: Matching as a Service (MaaS)", "fte": 0.54, "percent": 0.04},
        {"name": "FINTECH: SAP Treasury Sustain", "fte": 0.54, "percent": 0.04},
        {"name": "FINTECH: FRE-ACCTG-Global Audit Sustain", "fte": 0.53, "percent": 0.04},
        {"name": "eCommerce: E2E: Platform (shared components, E2E testing, release eng)", "fte": 0.50, "percent": 0.04},
        {"name": "FINTECH: FDF-Data Enablement Sustain", "fte": 0.50, "percent": 0.04},
        {"name": "FINTECH: FRE-ACCTG-Unified Accounting", "fte": 0.50, "percent": 0.04},
        {"name": "FINTECH: FRE-AP-Upstream Data Processing and Services Sustain", "fte": 0.50, "percent": 0.04},
        {"name": "FINTECH: FRE-AR-Health and Wellness Sustain", "fte": 0.50, "percent": 0.04},
        {"name": "Marketplace: Data Platforms", "fte": 0.50, "percent": 0.04},
        {"name": "GTP: AI Factory & AI/ML Platform", "fte": 0.50, "percent": 0.04},
        {"name": "FINTECH: FPA-OneStream-Domestic Applications", "fte": 0.48, "percent": 0.03},
        {"name": "GTP: Strategy and Business Ops", "fte": 0.42, "percent": 0.03},
        {"name": "FINTECH: FDF-Master Data Sustain", "fte": 0.37, "percent": 0.03},
        {"name": "FINTECH: FDF-Corporate Data Sustain", "fte": 0.31, "percent": 0.02},
        {"name": "FINTECH: FRE-Tax-Tax Management Sustain", "fte": 0.30, "percent": 0.02},
        {"name": "FINTECH: FRE-AR-Invoicing Collection and Dispute Management-Billing Automation", "fte": 0.25, "percent": 0.02},
        {"name": "FINTECH: FRE-Intellidoc - Document digitization", "fte": 0.25, "percent": 0.02},
        {"name": "FINTECH: FRE-NA SBO Automations", "fte": 0.25, "percent": 0.02},
        {"name": "FINTECH: FRE-Tax-Tax Management-Tax Resilience (Intelligence / Anomaly Detection)", "fte": 0.25, "percent": 0.02},
        {"name": "FINTECH: GenAI-Procurement Enablement", "fte": 0.25, "percent": 0.02},
        {"name": "FY26: Intl Mergers Acquisitions and Divestitures - CTA -- Enablers: Enabler", "fte": 0.25, "percent": 0.02},
        {"name": "IT GENERAL CONTROLS: ITGC - KTLO", "fte": 0.25, "percent": 0.02},
        {"name": "FINTECH: FRE-Treasury-Cash Recycler Devices and Integrations Sustain", "fte": 0.25, "percent": 0.02},
        {"name": "FINTECH: FRE-Risk Casualty Claims-Casualty Allocation System (CAS)", "fte": 0.25, "percent": 0.02},
        {"name": "FINTECH: Channel Data Enhancements", "fte": 0.23, "percent": 0.02},
        {"name": "FINTECH: SAP Master Data Governance Finance (MDG-F) Sustain", "fte": 0.22, "percent": 0.02},
        {"name": "FINTECH: FPA-OneStream-International Applications Sustain", "fte": 0.20, "percent": 0.01},
        {"name": "FINTECH: FRE-AP-Direct Imports Sustain", "fte": 0.20, "percent": 0.01},
        {"name": "FINTECH: FRE-AR-Invoicing Collection and Dispute Management-Cash Match Automation", "fte": 0.20, "percent": 0.01},
        {"name": "Unified Reconciliation and Settlement (URS)", "fte": 0.20, "percent": 0.01},
        {"name": "FY27: E2E: Digital Growth: Growth : QSR", "fte": 0.20, "percent": 0.01},
        {"name": "FINTECH: FRE-Tax-Tax Compliance-Use Tax", "fte": 0.19, "percent": 0.01},
        {"name": "FINTECH: FRE-Disputes and Self Service - Cycle Tracking", "fte": 0.18, "percent": 0.01},
        {"name": "FINTECH: FRE-Finance Data Services (AP/AR)", "fte": 0.16, "percent": 0.01},
        {"name": "FINTECH: FRE-ACCTG-Lease Accounting and Mgmt - Lease Accounting System Rationalization", "fte": 0.15, "percent": 0.01},
        {"name": "FINTECH: FRE-ACCTG-Lease Accounting and Mgmt - Lease Abstraction Intelligence", "fte": 0.15, "percent": 0.01},
        {"name": "FINTECH: FPA-FDH-International Reporting & Analytics", "fte": 0.12, "percent": 0.01},
        {"name": "FINTECH: FDF-Governance - Data Management and Literacy", "fte": 0.10, "percent": 0.01},
        {"name": "FINTECH: FPA-OneStream-Functional Application Sustain", "fte": 0.10, "percent": 0.01},
        {"name": "FINTECH: FRE-SAP-Treasury - Materiality thresholds and Rules", "fte": 0.10, "percent": 0.01},
        {"name": "Marketplace: Seller Growth", "fte": 0.10, "percent": 0.01},
        {"name": "FINTECH: FRE-Exceptions, Disputes and Self Service - AP Disputes", "fte": 0.10, "percent": 0.01},
        {"name": "Account Payables", "fte": 0.10, "percent": 0.01},
        {"name": "MerchTools: Manufacturing: ERP Rollout", "fte": 0.10, "percent": 0.01},
        {"name": "Marketplace: Category Strategic Initiatives", "fte": 0.10, "percent": 0.01},
        {"name": "Marketplace: Seller Acquisition - Onboarding & Assortment Growth", "fte": 0.10, "percent": 0.01},
        {"name": "Marketplace: Search & Experience", "fte": 0.10, "percent": 0.01},
        {"name": "Marketplace: Local Finds", "fte": 0.10, "percent": 0.01},
        {"name": "FINTECH: FPA-OneStream-SML", "fte": 0.08, "percent": 0.01},
        {"name": "FINTECH: FPA-FDH-WMUS Reporting & Analytics", "fte": 0.05, "percent": 0.00},
        {"name": "FINTECH: SAP - Treasury -Global Cash position", "fte": 0.05, "percent": 0.00},
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
    return template.render(initiatives=DATA["all_initiatives"])

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
