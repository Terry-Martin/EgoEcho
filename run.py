import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('ego_echo')

psychopathy_sheet = SHEET.worksheet('psychopathy')



print("Instructions")
print("This quiz is designed to help give you some idea about whether or not you may be a psychopath or sociopath, or have psychopathic tendencies. This quiz is not meant to diagnose psychopathy or tell you definitively whether or not you’re a psychopath. But it will give you a pretty good idea, based upon the research. For each item, indicate how much you agree or disagree with the statement. Take your time and answer truthfully for the most accurate results.")
data = psychopathy_sheet.get_all_values()
question = str(data[1])
print(question)

