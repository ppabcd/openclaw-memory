import sys
sys.path.insert(0, '/root/.openclaw/workspace/scripts')
from google_sheets_reader import write_sheet

# Write ONLY to cell E2
write_sheet("1wcnQ2DMwQfC6C9h05xEOGqwNqnB0pbAPiG0oEDEEfE8", [["2847000"]], "Gold", "E2")