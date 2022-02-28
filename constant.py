# Change token
TOKEN = os.getenv('BOTAPIKEY')

SCOPE = [
    "https://spreadsheets.google.com/feeds",
    'https://www.googleapis.com/auth/spreadsheets',
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

JSON_ROUTE = "CheQuest.json"

MAIN_TABLE = 'test_sheet_'
