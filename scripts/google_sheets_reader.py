#!/usr/bin/env python3
"""
Google Sheets Reader - Read and write Google Sheets using Service Account
"""

import gspread
from google.oauth2.service_account import Credentials
import sys
import json

# Path to service account credentials
CREDS_FILE = "/root/.openclaw/workspace/.gcloud_service_account.json"

# Define the scopes
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

def get_client():
    """Initialize and return gspread client"""
    creds = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPES)
    return gspread.authorize(creds)

def read_sheet(sheet_url_or_id, worksheet_name=None, range_name=None):
    """
    Read data from a Google Sheet
    
    Args:
        sheet_url_or_id: Google Sheets URL or ID
        worksheet_name: Name of the worksheet (default: first sheet)
        range_name: Range in A1 notation (e.g., 'A1:D10', default: all data)
    """
    client = get_client()
    
    # Open the spreadsheet
    try:
        if sheet_url_or_id.startswith('http'):
            sheet = client.open_by_url(sheet_url_or_id)
        else:
            sheet = client.open_by_key(sheet_url_or_id)
    except Exception as e:
        print(f"Error opening spreadsheet: {e}")
        print(f"\nMake sure you've shared the sheet with: spendingmanagement@spending-management-441616.iam.gserviceaccount.com")
        return None
    
    # Get the worksheet
    if worksheet_name:
        worksheet = sheet.worksheet(worksheet_name)
    else:
        worksheet = sheet.get_worksheet(0)  # First sheet
    
    # Get the data
    if range_name:
        data = worksheet.get(range_name)
    else:
        data = worksheet.get_all_values()
    
    return data

def write_sheet(sheet_url_or_id, data, worksheet_name=None, start_cell='A1'):
    """
    Write data to a Google Sheet
    
    Args:
        sheet_url_or_id: Google Sheets URL or ID
        data: List of lists containing the data
        worksheet_name: Name of the worksheet (default: first sheet)
        start_cell: Starting cell (default: 'A1')
    """
    client = get_client()
    
    # Open the spreadsheet
    if sheet_url_or_id.startswith('http'):
        sheet = client.open_by_url(sheet_url_or_id)
    else:
        sheet = client.open_by_key(sheet_url_or_id)
    
    # Get the worksheet
    if worksheet_name:
        worksheet = sheet.worksheet(worksheet_name)
    else:
        worksheet = sheet.get_worksheet(0)
    
    # Write the data
    worksheet.update(start_cell, data)
    return True

def append_row(sheet_url_or_id, row_data, worksheet_name=None):
    """
    Append a row to the end of a Google Sheet
    
    Args:
        sheet_url_or_id: Google Sheets URL or ID
        row_data: List containing the row data
        worksheet_name: Name of the worksheet (default: first sheet)
    """
    client = get_client()
    
    # Open the spreadsheet
    if sheet_url_or_id.startswith('http'):
        sheet = client.open_by_url(sheet_url_or_id)
    else:
        sheet = client.open_by_key(sheet_url_or_id)
    
    # Get the worksheet
    if worksheet_name:
        worksheet = sheet.worksheet(worksheet_name)
    else:
        worksheet = sheet.get_worksheet(0)
    
    # Append the row
    worksheet.append_row(row_data)
    return True

def get_sheet_info(sheet_url_or_id):
    """Get information about a spreadsheet"""
    client = get_client()
    
    if sheet_url_or_id.startswith('http'):
        sheet = client.open_by_url(sheet_url_or_id)
    else:
        sheet = client.open_by_key(sheet_url_or_id)
    
    info = {
        'title': sheet.title,
        'id': sheet.id,
        'url': sheet.url,
        'worksheets': []
    }
    
    for ws in sheet.worksheets():
        info['worksheets'].append({
            'title': ws.title,
            'id': ws.id,
            'rows': ws.row_count,
            'cols': ws.col_count
        })
    
    return info

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  Read sheet:  python3 google_sheets_reader.py read <sheet_url_or_id> [worksheet_name] [range]")
        print("  Write sheet: python3 google_sheets_reader.py write <sheet_url_or_id> <json_data> [worksheet_name]")
        print("  Append row:  python3 google_sheets_reader.py append <sheet_url_or_id> <json_row_data> [worksheet_name]")
        print("  Get info:    python3 google_sheets_reader.py info <sheet_url_or_id>")
        sys.exit(1)
    
    action = sys.argv[1]
    
    if action == "read":
        sheet_id = sys.argv[2]
        worksheet = sys.argv[3] if len(sys.argv) > 3 else None
        range_name = sys.argv[4] if len(sys.argv) > 4 else None
        
        data = read_sheet(sheet_id, worksheet, range_name)
        if data:
            print(json.dumps(data, indent=2))
    
    elif action == "write":
        sheet_id = sys.argv[2]
        data = json.loads(sys.argv[3])
        worksheet = sys.argv[4] if len(sys.argv) > 4 else None
        
        if write_sheet(sheet_id, data, worksheet):
            print("Data written successfully")
    
    elif action == "append":
        sheet_id = sys.argv[2]
        row_data = json.loads(sys.argv[3])
        worksheet = sys.argv[4] if len(sys.argv) > 4 else None
        
        if append_row(sheet_id, row_data, worksheet):
            print("Row appended successfully")
    
    elif action == "info":
        sheet_id = sys.argv[2]
        info = get_sheet_info(sheet_id)
        print(json.dumps(info, indent=2))
    
    else:
        print(f"Unknown action: {action}")
        sys.exit(1)
