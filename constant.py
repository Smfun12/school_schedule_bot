from model import Group

# Change token
TOKEN = '1180381593:AAHsyJIZad7OQG99LHrb2mAubmeQynaCDA0'

SCOPE = [
    "https://spreadsheets.google.com/feeds",
    'https://www.googleapis.com/auth/spreadsheets',
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

JSON_ROUTE = "CheQuest.json"

MAIN_TABLE = 'test_sheet_'

admin_telegram_ids = ['serdyuuuk','481036873']
groups = [Group(1, '01/03 15:00-17:00', 'link', 25, []), Group(2, '02/03 10:00-12:00', 'link', 30, [])]
commands = ('Записатись', 'Аккаунт з Minecraft', 'Ввести дані')