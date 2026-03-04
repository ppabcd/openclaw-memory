# Google Sheets - Spending Structure

## Sheet Info
- **Spreadsheet ID**: 1wcnQ2DMwQfC6C9h05xEOGqwNqnB0pbAPiG0oEDEEfE8
- **Tab Name**: Spending

## Column Structure (Row 6 = Header, Data starts Row 8)
| Column | Name | Description |
|--------|------|-------------|
| A | - | Empty column |
| B | ✓ | Checkbox/Status (TRUE/FALSE) |
| C | Date | Transaction date |
| D | Description | Transaction description/notes |
| E | - | Empty column |
| F | Category | Spending category (Transport, Food, Entertainment, etc.) |
| G | Total | Amount in Rp |
| H | Bank Account | Which bank account used |

## How to Add Entry
**IMPORTANT**: Don't use append_row - it goes to row 1019. Find first empty row instead.
**Column G (Total)**: Must be NUMBER not string (no apostrophe prefix)

Example code:
```python
# Find first empty row after header (row 6)
all_values = worksheet.get_all_values()
for i in range(7, 100):
    if len(all_values[i]) < 3 or all_values[i][2] == '':
        first_empty_row = i + 1
        break

# Write with Total as integer
row_data = ["", "FALSE", "2026-02-24", "Description", "", "Category", 50000, "BCA"]
worksheet.update(values=[row_data], range_name=f'A{first_empty_row}:H{first_empty_row}', value_input_option='USER_ENTERED')
```

## Expected Categories (based on budget template)
- Transport
- Food (diluar)
- Healthcare
- Utilities
- Subscription
- Shopping
- Entertainment
- Travel
- Girlfriend
- Zakat
- Savings (Bibit)
- Emas (Gold)
