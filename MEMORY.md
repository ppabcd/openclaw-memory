# MEMORY.md - Long-Term Memory

## Financial Profile

### Current Status (Feb 2026)
- **Total Assets**: Rp 107,947,213 (~108M)
- **Monthly Income**: Rp 12,000,000 (gross), Rp 11,375,000 (net after tax)
- **Tax**: Self-paid PPh 21, Rp 625,000/month
- **Savings Rate**: 57% (Rp 6.5M/month) - established Feb 24, 2026

### Asset Breakdown
- **Crypto**: Rp 16,181,236
- **Emas (Gold)**: Rp 32,090,044
- **Reksa Dana (Bibit)**: Rp 18,125,025
- **Saham (Stocks)**: Rp 1,877,828
- **Bank Accounts**: BCA, Mandiri, Jago, Jenius (currently Rp 0)

### Financial Goal
- **Target**: Rp 3,000,000,000 (3B)
- **Gap**: Rp 2.9B (27.8x current assets)
- **Timeline**: 9-11 years with aggressive strategy
- **Strategy**: 40% savings rate + 15-20% investment returns

### Budget Allocation (Monthly)
**Template stored in:** `budget_template.md`

- **Emas & Fixed**: 62.0% (Rp 7,050,000)
  - Emas 2 gram: 6M
  - Food diluar: 1M (makan rumah ditanggung ortu)
  - Utilities: 50K
- **Needs**: 6.9% (Rp 787,000)
  - Transport: 300K, Healthcare: 200K
  - Zakat: 287K
- **Wants**: 26.6% (Rp 3,025,000)
  - Girlfriend: 1.705M
  - Pet & Flowers: 620K
  - Shopping: 300K, Entertainment: 200K, Travel: 200K
- **Savings**: 4.4% (Rp 500,000)
  - Bibit (emergency + investment): 500K

## Google Sheets
- **Main Sheet**: Asset Management
  - ID: 1wcnQ2DMwQfC6C9h05xEOGqwNqnB0pbAPiG0oEDEEfE8
  - Tabs: Assets, Budgeting, Spending, Gold, Crypto, etc.
- **Daily Asset Tracking**: memory/asset_history.csv
- **Service Account**: .gcloud_service_account.json (workspace root)
  - Email: spendingmanagement@spending-management-441616.iam.gserviceaccount.com
  - Script: scripts/google_sheets_reader.py
  - Usage: `python3 scripts/google_sheets_reader.py [read|write|append|info] <sheet_id> [args]`

### Spending Sheet Structure
- **Tab**: Spending
- **Header Row**: 6 (data starts row 8)
- **Columns**: B=Checkbox, C=Date, D=Description, F=Category, G=Total, H=Bank Account
- **Categories**: Transport, Food (diluar), Healthcare, Utilities, Subscription, Shopping, Entertainment, Travel, Girlfriend, Zakat, Savings (Bibit), Emas (Gold), Business
- **IMPORTANT**: Always write numbers as integers/floats, NOT strings. Use `value_input_option='USER_ENTERED'` to avoid apostrophe prefix

## Kyla-Go Infrastructure
- **Endpoints**: go.kyla.my.id, go-test.kyla.my.id, go-prod.kyla.my.id
- **Database**: PostgreSQL on Supabase (500MB limit)
  - Host: aws-1-ap-southeast-1.pooler.supabase.com
  - Current usage: ~263MB (52.7%) as of Feb 24
  - Cleaned up from 487MB using VACUUM FULL
- **Storage**: R2 bucket (Cloudflare)

## Monitoring & Automation
- **Health checks**: Every 30min on 3 Kyla-Go endpoints
- **DB size monitoring**: Every 3 hours
- **Daily asset report**: 8 AM (with historical tracking)
- **Gold price update**: 5 AM daily

## Lessons Learned
- PostgreSQL DELETE doesn't reclaim space - need VACUUM FULL
- Miscellaneous budget category = money black hole (avoid!)
- 700K/month savings won't reach 3B target
- Need aggressive 40%+ savings rate for wealth building
- Budget by paycheck period (25th-24th) cleaner than calendar month
- Use percentage-based template for flexible salary adjustments
- Emas 2 gram/month = 52% of net income (very aggressive but intentional)
