from flask import Flask, jsonify
from flask_cors import CORS
import time, random

app = Flask(__name__)
CORS(app)

AGENTS = {
    "customer_support": {
        "id": "customer_support", "name": "Customer Support Agent", "shortName": "Support",
        "color": "blue", "hex": "#3b82f6", "status": "online",
        "description": "Handles 24/7 FAQs, triages complex tickets to humans, and provides instant order tracking.",
        "howItWorks": [
            "Ingests your FAQ database and product documentation",
            "Uses NLP to classify questions by intent & urgency",
            "Responds instantly to known FAQs with pre-approved answers",
            "Escalates complex tickets to humans with context summary",
            "Tracks orders via shipping API for real-time status",
            "Learns from resolved tickets to improve accuracy"
        ],
        "metrics": {"Resolved": "1,847", "Avg Response": "1.2s", "Satisfaction": "94%", "Escalation": "8%"},
        "weeklyChart": [65, 78, 82, 71, 90, 85, 88],
        "scenarios": [
            {"title": "FAQ Resolution", "query": "What is your return policy for electronics?",
             "steps": ["Receiving customer query...", "Classifying intent → [RETURN_POLICY]", "Searching knowledge base...", "Match: FAQ #127 (confidence: 97.3%)", "Generating response..."],
             "response": "Great question! Our electronics return policy allows returns within 30 days with original packaging. Items must be working. Refunds process in 5-7 business days. Would you like me to start a return?"},
            {"title": "Order Tracking", "query": "Where is my order #ORD-29471?",
             "steps": ["Receiving query...", "Classifying → [ORDER_TRACKING]", "Querying shipping API...", "Carrier: FedEx | FX-8827364", "Compiling timeline..."],
             "response": "📦 Order #ORD-29471 shipped via FedEx (FX-8827364). Left Memphis this morning, in transit to Montgomery, AL. Delivery: Tomorrow by 5 PM."},
            {"title": "Ticket Escalation", "query": "I'm frustrated! Product broke after 2 days!",
             "steps": ["Receiving query...", "Classifying → [COMPLAINT_DEFECT]", "Sentiment: NEGATIVE (-0.87)", "⚠ Escalation triggered", "Creating ticket #TK-4921...", "Routing to Sarah M."],
             "response": "I understand your frustration. Priority ticket #TK-4921 created — Sarah will reach out within 30 minutes. Your order is flagged for immediate replacement."}
        ]
    },
    "sales_lead": {
        "id": "sales_lead", "name": "Sales & Lead Agent", "shortName": "Sales",
        "color": "purple", "hex": "#8b5cf6", "status": "online",
        "description": "Qualifies website visitors, drafts personalized follow-up emails, and schedules meetings on your calendar.",
        "howItWorks": [
            "Monitors visitor behavior (pages, time, scroll depth)",
            "Scores leads on engagement and firmographic data",
            "Initiates chat with high-intent visitors",
            "Asks qualifying questions (budget, timeline, authority)",
            "Drafts personalized follow-up emails",
            "Books meetings via calendar scheduling API"
        ],
        "metrics": {"Leads": "324", "Conversion": "18.7%", "Meetings": "67", "Emails": "892"},
        "weeklyChart": [42, 55, 48, 62, 58, 71, 65],
        "scenarios": [
            {"title": "Lead Qualification", "query": "New visitor on pricing — TechStart Inc (4 pages, 8 min)",
             "steps": ["Detecting high-intent visitor...", "Enriching: TechStart, Series A, 45 employees", "Lead score: 82/100 (HOT)", "ICP match ✓", "Initiating chat..."],
             "response": "👋 Hi! I see you're exploring our Business plan. Companies like TechStart love our Growth tier — API access + team features. Want a walkthrough or a 15-min call?"},
            {"title": "Follow-up Email", "query": "Draft follow-up for Sarah Chen (CTO @ DataFlow)",
             "steps": ["Retrieving history...", "Topics: API limits, webhooks, SSO", "Analyzing tech stack...", "Template: Technical DM", "Personalizing..."],
             "response": "Subject: API Integration Details for DataFlow\n\nHi Sarah,\n• API: 10K req/min — handles your volume\n• Webhooks: Full streaming\n• SSO: SAML 2.0 + OAuth 2.0\n\nSandbox ready. Thursday 2 PM?\n\nBest, Alex"},
            {"title": "Meeting Scheduler", "query": "Book demo with Mark Rivera, CEO GreenLeaf",
             "steps": ["Checking calendar...", "Slots: Tue 10am, Wed 2pm, Thu 11am", "Timezone: PST", "Creating Zoom invite...", "Preparing brief..."],
             "response": "✅ Booked!\n📅 Wed 2 PM EST (11 AM PST)\n👤 Mark Rivera, CEO\n🔗 Zoom generated\nBrief: Packaging, 120 employees, $8M ARR"}
        ]
    },
    "finance_ops": {
        "id": "finance_ops", "name": "Finance & Operations Agent", "shortName": "Finance",
        "color": "green", "hex": "#10b981", "status": "online",
        "description": "Automatically categorizes expenses, flags late invoices, and generates weekly cash flow reports.",
        "howItWorks": [
            "Connects to bank & accounting APIs",
            "ML auto-categorizes every transaction",
            "Monitors A/R and flags past-due invoices",
            "Sends reminders at 7, 14, 30 day intervals",
            "Generates weekly cash flow with trends",
            "Alerts on unusual spending or overruns"
        ],
        "metrics": {"Categorized": "4,521", "Late Invoices": "23", "Accuracy": "96.8%", "Saved": "12h/wk"},
        "weeklyChart": [30, 45, 38, 52, 41, 60, 55],
        "scenarios": [
            {"title": "Expense Categorization", "query": "Process 47 transactions from Chase",
             "steps": ["Connecting to Chase API...", "Fetching 47 txns ($28,450.67)...", "Running ML categorization...", "45/47 classified (95.7%)", "2 flagged for review", "Updating QuickBooks..."],
             "response": "✅ 47 Processed ($28,450.67)\n• SaaS: $4,200 (8) • Supplies: $1,847 (12)\n• Marketing: $8,500 (5) • Payroll: $11,200 (2)\n• Travel: $1,453 (15) • Utilities: $750 (3)\n\n⚠ Flagged: $350 unknown vendor, $150 duplicate"},
            {"title": "Late Invoice Detection", "query": "Scan for overdue payments",
             "steps": ["Scanning A/R...", "34 outstanding ($142,800)", "Checking due dates...", "5 overdue found", "Sending reminders..."],
             "response": "🔴 5 Overdue — $34,200\n1. Meridian $12,500 (21d)\n2. BlueSky $8,700 (14d)\n3. TechBridge $6,200 (12d)\n4. Oakwood $4,300 (7d)\n5. Summit $2,500 (3d)"},
            {"title": "Cash Flow Report", "query": "Weekly report Feb 10-16, 2026",
             "steps": ["Aggregating income...", "Compiling expenses...", "Net calculation...", "Week-over-week comparison...", "Summary..."],
             "response": "📈 Feb 10-16\n💰 Income: $67,340 | 💸 Expenses: $41,280\n📊 Net: +$26,060 (+12%)\n🏦 Balance: $184,520 | Runway: 6.2 months"}
        ]
    },
    "content_marketing": {
        "id": "content_marketing", "name": "Content Marketing Agent", "shortName": "Content",
        "color": "orange", "hex": "#f59e0b", "status": "online",
        "description": "Monitors trends, drafts SEO-friendly blog posts, and adapts content for various social media platforms.",
        "howItWorks": [
            "Monitors Google Trends, social & industry news",
            "Identifies content gaps via competitor analysis",
            "Generates SEO-optimized blog drafts",
            "Adapts content for each social platform",
            "Suggests optimal posting times",
            "Tracks performance and recommends improvements"
        ],
        "metrics": {"Posts": "156", "SEO Score": "87/100", "Social": "624", "Trends": "89"},
        "weeklyChart": [20, 35, 28, 42, 38, 50, 45],
        "scenarios": [
            {"title": "Trend Monitoring", "query": "Trending SaaS/B2B topics?",
             "steps": ["Scanning Google Trends...", "Twitter/X #B2B analysis...", "Competitor monitoring...", "Calendar cross-ref...", "Ranking potential..."],
             "response": "🔥 Trending:\n1. 'AI Agent Orchestration' ↑340% — Gap!\n2. 'SOC 2 Automation' — Refresh post\n3. 'Vertical AI SaaS' — Emerging\n4. 'Success Metrics' — #8 → top 3"},
            {"title": "Blog Post Draft", "query": "Draft: AI Agent Orchestration for SMBs",
             "steps": ["Keyword research...", "'AI agent orchestration' (1,800/mo)", "SERP analysis...", "Outline generation...", "Writing 1,800 words...", "SEO pass..."],
             "response": "✅ Draft Ready! SEO: 91/100\n'AI Agent Orchestration: SMB Guide 2026'\n1,847 words | Grade 8 | 6 keyword uses\n6 sections, 3 internal links, 4 images"},
            {"title": "Social Adaptation", "query": "Adapt blog for LinkedIn, Twitter/X, Instagram",
             "steps": ["Extracting takeaways...", "LinkedIn post...", "Twitter/X thread...", "Instagram carousel...", "Scheduling..."],
             "response": "📱 Pack Ready!\n🔵 LinkedIn (Tue 9am): Professional post\n🐦 Twitter/X (Wed 12pm): 5-tweet thread\n📸 Instagram (Thu 6pm): 6-slide carousel\n✅ Scheduled in Buffer"}
        ]
    },
    "tax_compliance": {
        "id": "tax_compliance", "name": "Tax & Compliance Agent", "shortName": "Tax",
        "color": "red", "hex": "#ef4444", "status": "online",
        "description": "Manages sales tax calculations, tracks deductions, prepares filing summaries, and monitors compliance deadlines across jurisdictions.",
        "howItWorks": [
            "Connects to your POS, invoicing, and payroll systems to aggregate taxable transactions",
            "Calculates sales tax rates per jurisdiction (state, county, city) using real-time tax tables",
            "Scans all expenses and categorizes potential tax deductions by IRS schedule",
            "Tracks quarterly estimated tax deadlines and sends proactive filing reminders",
            "Generates pre-filled filing worksheets for federal, state, and local returns",
            "Monitors regulatory changes and flags new compliance requirements for your business"
        ],
        "metrics": {"Deductions Found": "$42,800", "Filing Accuracy": "99.2%", "Jurisdictions": "12", "Deadlines Met": "100%"},
        "weeklyChart": [15, 22, 18, 35, 28, 45, 40],
        "scenarios": [
            {
                "title": "Sales Tax Calculation",
                "query": "Calculate sales tax collected across all channels for Q4 2025",
                "steps": [
                    "Connecting to Shopify POS and invoicing systems...",
                    "Aggregating Q4 2025 transactions: 3,847 orders across 12 states...",
                    "Loading current tax rate tables for each jurisdiction...",
                    "Calculating nexus obligations by state...",
                    "Cross-referencing exemption certificates on file...",
                    "Compiling jurisdiction-level summary..."
                ],
                "response": "🧾 Q4 2025 Sales Tax Summary\n\n📊 Total Taxable Revenue: $487,320\n💰 Total Sales Tax Collected: $38,214.67\n\nTop Jurisdictions:\n• Alabama (state + county): $12,480.22 (rate: 4.0% + avg 5.1% local)\n  → Montgomery Co: $8,240.11 | Madison Co: $4,240.11\n• Georgia: $8,945.30 (rate: 4.0% + local)\n• Florida: $6,122.88 (rate: 6.0%, no income tax state)\n• Tennessee: $4,880.40 (rate: 7.0%)\n• 8 other states: $5,785.87\n\n⚠ Action Items:\n→ Alabama monthly filing due Jan 20 — $4,160.07 for December\n→ Georgia quarterly return due Jan 31\n→ 2 new nexus thresholds approaching in Texas and New York\n→ 14 exemption certificates expiring in Q1 — renewal notices sent\n\n✅ All collected amounts reconciled. No undercollection detected."
            },
            {
                "title": "Deduction Tracker",
                "query": "Scan all 2025 expenses and identify potential tax deductions",
                "steps": [
                    "Loading 2025 expense data from QuickBooks...",
                    "Categorizing 6,284 transactions by IRS deduction schedule...",
                    "Applying Section 179 depreciation analysis to asset purchases...",
                    "Identifying home office and vehicle deductions...",
                    "Cross-referencing against prior year deductions for consistency...",
                    "Flagging missed deductions and new opportunities...",
                    "Generating deduction summary by schedule..."
                ],
                "response": "💡 2025 Tax Deduction Analysis\n\n📋 Total Potential Deductions: $142,860\n💵 Estimated Tax Savings: $42,858 (at 30% effective rate)\n\nBy Category:\n┌─────────────────────────────────────────────┐\n│ Schedule C — Business Expenses              │\n│  • Office rent & utilities: $36,000         │\n│  • Software & subscriptions: $14,400        │\n│  • Professional services: $18,200           │\n│  • Advertising & marketing: $22,800         │\n│  • Insurance premiums: $8,400               │\n│                                             │\n│ Section 179 — Equipment Depreciation        │\n│  • 3 laptops + monitors: $8,700             │\n│  • Office furniture: $4,200                 │\n│  • Server equipment: $12,500                │\n│                                             │\n│ Vehicle & Travel                            │\n│  • Business mileage (8,420 mi × $0.67): $5,641│\n│  • Business travel: $6,840                  │\n│                                             │\n│ Home Office (280 sq ft / 1,800 sq ft)       │\n│  • Simplified method: $1,500                │\n│  • Actual method: $5,180 ← RECOMMENDED      │\n└─────────────────────────────────────────────┘\n\n🔍 3 Missed Deductions Found:\n→ $2,400 in business meals not categorized (50% deductible)\n→ $890 professional development courses\n→ $1,200 charitable donations from business account\n\n⚡ Recommendation: Switch home office to actual method = $3,680 additional savings"
            },
            {
                "title": "Filing Preparation",
                "query": "Prepare my Q4 estimated tax filing and annual return checklist",
                "steps": [
                    "Calculating Q4 estimated tax obligation...",
                    "Comparing to safe harbor thresholds (110% prior year)...",
                    "Aggregating all income sources (1099s, W-2s, K-1s)...",
                    "Applying 2025 tax brackets and standard/itemized comparison...",
                    "Generating filing timeline with all deadlines...",
                    "Preparing document checklist for CPA handoff..."
                ],
                "response": "📅 Tax Filing Preparation — 2025\n\n🔵 Q4 ESTIMATED PAYMENT (Due Jan 15, 2026)\n  Estimated annual income: $392,400\n  Total tax liability est.: $98,100\n  Payments made (Q1-Q3): $73,575\n  → Q4 payment due: $24,525\n  → Safe harbor met: ✅ (110% of 2024 = $88,000)\n\n🔴 ANNUAL RETURN — Key Dates\n  • Jan 31: W-2s and 1099s due to contractors\n  • Mar 15: S-Corp/Partnership returns (Form 1120-S/1065)\n  • Apr 15: Individual return (Form 1040 + Schedule C)\n  • Apr 15: Q1 2026 estimated payment\n\n📋 DOCUMENT CHECKLIST\n  ✅ Income: All 1099-NEC received (7 of 7)\n  ✅ Expenses: QuickBooks reconciled through Dec 31\n  ✅ Payroll: W-2s generated for 8 employees\n  ⬜ Pending: K-1 from investment partnership (ETA: Feb 28)\n  ⬜ Pending: Final bank statement reconciliation\n  ⬜ Review: Home office measurements need verification\n\n💰 ESTIMATED REFUND/OWED\n  If itemized + all deductions claimed: OWE $2,340\n  If standard deduction: OWE $18,720\n  → Recommendation: ITEMIZE (saves $16,380)\n\n📎 CPA-ready packet exported to Google Drive."
            },
            {
                "title": "Compliance Monitor",
                "query": "Check multi-state tax compliance status and upcoming obligations",
                "steps": [
                    "Scanning active state registrations...",
                    "Checking nexus thresholds for all 50 states...",
                    "Reviewing filing frequency requirements...",
                    "Verifying all prior filings are current...",
                    "Monitoring legislative changes affecting your business..."
                ],
                "response": "🏛️ Multi-State Compliance Dashboard\n\n✅ CURRENT & COMPLIANT (8 states)\n  AL, GA, FL, TN, NC, SC, VA, TX\n  All filings current. No outstanding liabilities.\n\n⚠️ ACTION REQUIRED (2 states)\n  • New York: Economic nexus threshold reached ($498K of $500K)\n    → Must register by Q2 2026. Filing application prepared.\n  • California: Approaching $500K threshold ($467K)\n    → Monitoring. Projected to trigger by April 2026.\n\n📋 UPCOMING FILINGS (Next 30 Days)\n  • AL Monthly — Due Feb 20 → Amount: $4,812.33\n  • GA Quarterly — Due Feb 28 → Amount: $3,220.18\n  • FL Semi-Annual — Due Mar 1 → Amount: $2,890.44\n\n🔔 REGULATORY ALERTS\n  • Alabama: New marketplace facilitator rules effective Mar 1\n  • Tennessee: SaaS taxability ruling pending — may affect your products\n  • Federal: BOI reporting deadline extended to Mar 21, 2026\n\n✅ All 2025 annual returns filed on time. No penalties assessed."
            }
        ]
    },
    "profit_loss": {
        "id": "profit_loss", "name": "P&L & Financial Filing Agent", "shortName": "P&L",
        "color": "cyan", "hex": "#06b6d4", "status": "online",
        "description": "Generates profit & loss statements, auto-prepares financial filings, tracks margins, and produces investor-ready financial reports.",
        "howItWorks": [
            "Aggregates revenue streams, COGS, and operating expenses from all connected systems",
            "Generates real-time P&L statements with month-over-month and year-over-year comparisons",
            "Calculates gross margin, operating margin, and net margin with trend analysis",
            "Auto-prepares financial statements for quarterly and annual filings (GAAP-compliant)",
            "Produces board-ready financial packages with charts, commentary, and forecasts",
            "Monitors key financial ratios and alerts on deviations from targets"
        ],
        "metrics": {"Reports Generated": "48", "Margin Accuracy": "99.4%", "Filing Prep": "< 2 hrs", "Ratio Alerts": "7"},
        "weeklyChart": [25, 30, 42, 38, 55, 48, 52],
        "scenarios": [
            {
                "title": "Monthly P&L Statement",
                "query": "Generate the January 2026 Profit & Loss statement with comparisons",
                "steps": [
                    "Aggregating January 2026 revenue from all channels...",
                    "Pulling COGS from inventory and vendor systems...",
                    "Compiling operating expenses by department...",
                    "Calculating gross, operating, and net margins...",
                    "Running month-over-month and year-over-year comparisons...",
                    "Generating variance analysis and commentary..."
                ],
                "response": "📊 PROFIT & LOSS — January 2026\n\n═══════════════════════════════════════════\n                          Jan 2026    Dec 2025    Jan 2025\n───────────────────────────────────────────\n💰 REVENUE\n  Product Sales            $168,400    $182,100    $142,300\n  Service Revenue           $74,200     $68,500     $61,800\n  Recurring/SaaS            $45,800     $44,200     $32,600\n  ─────────────────────────────────────────\n  Total Revenue            $288,400    $294,800    $236,700\n                                        (-2.2%)    (+21.8%)\n\n💸 COST OF GOODS SOLD\n  Product Costs             $58,940     $63,735     $52,651\n  Service Delivery          $22,260     $20,550     $18,540\n  ─────────────────────────────────────────\n  Total COGS               $81,200     $84,285     $71,191\n\n📈 GROSS PROFIT            $207,200    $210,515    $165,509\n   Gross Margin              71.8%       71.4%       69.9%  ✅\n\n🏢 OPERATING EXPENSES\n  Payroll & Benefits        $89,600     $89,600     $78,400\n  Marketing & Ads           $24,800     $32,100     $18,200\n  Rent & Utilities          $12,400     $12,400     $11,800\n  Software & Tools           $8,900      $8,400      $6,200\n  Professional Services      $6,200      $4,800      $5,100\n  Other OpEx                 $7,340      $8,920      $6,800\n  ─────────────────────────────────────────\n  Total OpEx              $149,240    $156,220    $126,500\n\n📊 OPERATING INCOME         $57,960     $54,295     $39,009\n   Operating Margin          20.1%       18.4%       16.5%  📈\n\n   Interest & Other          ($1,200)    ($1,200)    ($1,400)\n   ─────────────────────────────────────────\n💵 NET INCOME               $56,760     $53,095     $37,609\n   Net Margin                19.7%       18.0%       15.9%  📈\n\n⚡ KEY INSIGHTS\n  • Revenue dipped 2.2% MoM (seasonal post-holiday) but up 21.8% YoY\n  • Gross margin expanded 40bps — COGS optimization paying off\n  • Marketing spend down $7,300 with only $6,400 revenue impact = better efficiency\n  • Operating margin crossed 20% threshold for first time 🎉\n  • SaaS revenue growing 40.5% YoY — strongest segment"
            },
            {
                "title": "Quarterly Financial Filing",
                "query": "Auto-prepare Q4 2025 financial statements for filing",
                "steps": [
                    "Aggregating Q4 2025 data (Oct-Dec)...",
                    "Generating Income Statement (GAAP format)...",
                    "Building Balance Sheet as of Dec 31, 2025...",
                    "Preparing Cash Flow Statement (indirect method)...",
                    "Running GAAP compliance checks...",
                    "Adding management notes and disclosures...",
                    "Formatting for filing and CPA review..."
                ],
                "response": "📋 Q4 2025 FINANCIAL FILING PACKAGE — Ready\n\n═══════════════════════════════════════════\n📄 1. INCOME STATEMENT (Q4 2025)\n  Total Revenue:           $892,400\n  Total COGS:              $254,380  (28.5%)\n  Gross Profit:            $638,020  (71.5%)\n  Operating Expenses:      $462,180\n  Operating Income:        $175,840  (19.7%)\n  Net Income:              $168,240  (18.9%)\n\n📄 2. BALANCE SHEET (as of Dec 31, 2025)\n  ASSETS\n    Cash & Equivalents:    $184,520\n    Accounts Receivable:   $142,800\n    Inventory:              $67,200\n    Fixed Assets (net):     $89,400\n    Total Assets:          $483,920\n  LIABILITIES\n    Accounts Payable:       $48,200\n    Accrued Expenses:       $22,800\n    Long-term Debt:         $85,000\n    Total Liabilities:     $156,000\n  EQUITY\n    Owner's Equity:        $327,920\n\n📄 3. CASH FLOW STATEMENT\n  Operating Activities:    +$192,400\n  Investing Activities:     -$34,200\n  Financing Activities:     -$18,000\n  Net Change in Cash:     +$140,200\n\n✅ GAAP COMPLIANCE CHECKS\n  • Revenue recognition: ASC 606 compliant ✅\n  • Lease accounting: ASC 842 applied ✅\n  • Depreciation: Straight-line, schedules current ✅\n  • Accruals: All Q4 accruals posted ✅\n\n📎 Filed to: Google Drive → Finance → Q4 2025 Filing\n👤 CPA review packet sent to Anderson & Associates\n📅 10-K filing deadline: Mar 31, 2026 — ON TRACK"
            },
            {
                "title": "Margin & Ratio Analysis",
                "query": "Run full financial ratio analysis and flag any concerns",
                "steps": [
                    "Calculating profitability ratios...",
                    "Computing liquidity and solvency ratios...",
                    "Analyzing efficiency metrics (DSO, DPO, inventory turns)...",
                    "Comparing to industry benchmarks (SaaS/B2B)...",
                    "Identifying trends and red flags...",
                    "Generating executive summary..."
                ],
                "response": "📊 FINANCIAL RATIO ANALYSIS — FY 2025\n\n═══════════════════════════════════════════\n📈 PROFITABILITY           Yours    Industry    Status\n  Gross Margin              71.5%     68.0%      ✅ Above\n  Operating Margin          19.7%     15.2%      ✅ Above\n  Net Margin                18.9%     12.8%      ✅ Strong\n  Return on Equity          51.3%     22.0%      ✅ Excellent\n  Return on Assets          34.8%     14.0%      ✅ Excellent\n\n💧 LIQUIDITY\n  Current Ratio              3.12      2.10      ✅ Healthy\n  Quick Ratio                2.69      1.80      ✅ Strong\n  Cash Ratio                 1.18      0.85      ✅ Solid\n\n⚙️ EFFICIENCY\n  Days Sales Outstanding     42 days   38 days   ⚠️ Slightly High\n  Days Payable Outstanding   28 days   32 days   ✅ Good\n  Inventory Turnover         8.2x      7.5x      ✅ Good\n  Revenue per Employee      $148K     $125K      ✅ Efficient\n\n📉 LEVERAGE\n  Debt-to-Equity             0.26      0.45      ✅ Conservative\n  Interest Coverage         146.5x     12.0x     ✅ Very Strong\n\n⚠️ ALERTS (2 items)\n  1. DSO trending up: 38 → 42 days over 3 months\n     → 5 overdue invoices contributing $34,200\n     → Collections agent notified. Expected recovery: 2 weeks.\n\n  2. Marketing ROI declining: $4.80 → $3.92 per $1 spent\n     → Q4 ad CPM increased 22% industry-wide\n     → Recommend shifting 15% budget to content/SEO\n\n💡 OVERALL HEALTH: STRONG\n  Your business is outperforming industry benchmarks across\n  profitability, liquidity, and leverage. Address DSO trend\n  and marketing efficiency for continued growth."
            },
            {
                "title": "Annual Report Prep",
                "query": "Prepare the 2025 annual financial report for board and investors",
                "steps": [
                    "Compiling 12-month P&L with quarterly breakdowns...",
                    "Generating year-over-year comparison (2024 vs 2025)...",
                    "Building segment analysis by revenue stream...",
                    "Creating forward-looking projections for 2026...",
                    "Designing executive summary with key highlights...",
                    "Formatting board-ready presentation package..."
                ],
                "response": "📑 2025 ANNUAL FINANCIAL REPORT — Board Package\n\n═══════════════════════════════════════════\n🏆 EXECUTIVE SUMMARY\n  FY 2025 was a breakout year. Revenue grew 34% to $3.2M,\n  we achieved operating profitability (19.7% margin), and\n  SaaS recurring revenue crossed $500K ARR.\n\n📊 ANNUAL P&L HIGHLIGHTS\n  Total Revenue:         $3,218,400  (+34% YoY)\n  Gross Profit:          $2,301,156  (71.5% margin)\n  Operating Income:        $634,025  (19.7% margin)\n  Net Income:              $608,425  (18.9% margin)\n  EBITDA:                  $712,025  (22.1% margin)\n\n📈 REVENUE BY SEGMENT\n  Product Sales:  $1,842,000 (57%) — +28% YoY\n  Services:         $876,400 (27%) — +31% YoY\n  SaaS/Recurring:   $500,000 (16%) — +67% YoY  🚀\n\n📅 QUARTERLY PROGRESSION\n  Q1: $712K | Q2: $788K | Q3: $826K | Q4: $892K\n  Sequential growth every quarter ✅\n\n🔮 2026 PROJECTIONS\n  Conservative:   $3.86M (+20%)  | Net margin: 19%\n  Base case:      $4.18M (+30%)  | Net margin: 21%\n  Aggressive:     $4.83M (+50%)  | Net margin: 23%\n\n👥 KEY METRICS\n  Employees: 8 → 12 (50% growth)\n  Revenue/employee: $148K → target $160K\n  Customer count: 342 → 485 (+42%)\n  Churn rate: 4.2% (industry avg: 6.8%)\n\n📎 Full report (42 pages) exported to:\n  → Google Drive: Finance/Annual Reports/2025\n  → Board portal: Updated with latest deck\n  → Investor data room: Refreshed\n\n📅 Board meeting: Mar 15 — presentation deck ready."
            }
        ]
    }
}

ACTIVITY = [
    {"agent": "customer_support", "action": "Resolved ticket #TK-4918", "time": "2 min ago", "status": "success"},
    {"agent": "tax_compliance", "action": "Alabama monthly filing prepared — $4,812", "time": "3 min ago", "status": "success"},
    {"agent": "sales_lead", "action": "Qualified lead: DataVault Inc", "time": "5 min ago", "status": "success"},
    {"agent": "profit_loss", "action": "January 2026 P&L statement generated", "time": "6 min ago", "status": "success"},
    {"agent": "finance_ops", "action": "Categorized 12 transactions", "time": "8 min ago", "status": "success"},
    {"agent": "content_marketing", "action": "Published blog to CMS", "time": "15 min ago", "status": "success"},
    {"agent": "tax_compliance", "action": "⚠ 2 new state nexus thresholds approaching", "time": "18 min ago", "status": "warning"},
    {"agent": "customer_support", "action": "Escalated #TK-4920 to Sarah M.", "time": "22 min ago", "status": "warning"},
    {"agent": "profit_loss", "action": "Gross margin alert: crossed 72% 📈", "time": "25 min ago", "status": "info"},
    {"agent": "sales_lead", "action": "Drafted 3 follow-up emails", "time": "30 min ago", "status": "success"},
    {"agent": "tax_compliance", "action": "Found $2,400 in missed meal deductions", "time": "35 min ago", "status": "info"},
    {"agent": "finance_ops", "action": "Flagged overdue INV-1089", "time": "45 min ago", "status": "warning"},
    {"agent": "profit_loss", "action": "Q4 financial filing package ready for CPA", "time": "50 min ago", "status": "success"},
    {"agent": "content_marketing", "action": "Trending: AI Orchestration", "time": "1 hr ago", "status": "info"},
    {"agent": "tax_compliance", "action": "Q4 estimated tax payment calculated: $24,525", "time": "1.5 hr ago", "status": "success"},
    {"agent": "profit_loss", "action": "DSO trending up: 38→42 days ⚠", "time": "2 hr ago", "status": "warning"},
]

DASHBOARD = {
    "totalInteractions": 9428, "avgResponseTime": "1.6s", "satisfaction": "93%",
    "costSavings": "$21,800/mo", "activeAgents": 6, "uptime": "99.97%"
}

@app.route('/api/agents')
def get_agents():
    return jsonify(AGENTS)

@app.route('/api/agents/<agent_id>')
def get_agent(agent_id):
    return jsonify(AGENTS.get(agent_id, {"error": "not found"}))

@app.route('/api/dashboard')
def get_dashboard():
    return jsonify(DASHBOARD)

@app.route('/api/activity')
def get_activity():
    return jsonify(ACTIVITY)

@app.route('/api/simulate/<agent_id>/<int:idx>', methods=['POST'])
def simulate(agent_id, idx):
    agent = AGENTS.get(agent_id)
    if not agent or idx >= len(agent["scenarios"]):
        return jsonify({"error": "not found"}), 404
    scenario = agent["scenarios"][idx]
    time.sleep(0.3)
    return jsonify({
        "agent": agent_id, "scenario": scenario["title"],
        "query": scenario["query"], "steps": scenario["steps"],
        "response": scenario["response"],
        "processingTime": f"{random.uniform(2, 4.5):.1f}s",
        "confidence": f"{random.uniform(92, 99):.1f}%"
    })

@app.route('/api/health')
def health():
    return jsonify({"status": "healthy", "agents": 6})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
