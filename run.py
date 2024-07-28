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




"""
Function details
"""
def display_test_questions():

    psychopathy_sheet = SHEET.worksheet('psychopathy')

    data = psychopathy_sheet.get_all_values()

    print("Instructions")
    print("This quiz is designed to help give you some idea about whether or not you may be a psychopath or sociopath, or have psychopathic tendencies. This quiz is not meant to diagnose psychopathy or tell you definitively whether or not you’re a psychopath. But it will give you a pretty good idea, based upon the research. For each item, indicate how much you agree or disagree with the statement. Take your time and answer truthfully for the most accurate results.")

    question_count = 1
    overall_score = 0

    while question_count < 13:
        question = data[question_count][0]
        print(f"\nQuestion {question_count}: {question}\n")
        question_count = question_count + 1

        option_one = data[0][1]
        print(f"1: {option_one}")
        option_two = data[1][1]
        print(f"2: {option_two}")
        option_three = data[2][1]
        print(f"3: {option_three}\n")

        user_answer = input("Please select 1, 2 or 3: \n")
        print(f"You have chosen: {user_answer}")

        if int(user_answer) == 1:
            score_this_question = 0
        elif int(user_answer) == 2:
            score_this_question = 1
        elif int(user_answer) == 3:
            score_this_question = 2
        else :
            print("Input Error")
        print(f"Your score this question is {score_this_question}\n")

        
        overall_score = int(overall_score) + int(score_this_question)
        print(f"Your overall score so far is {overall_score}\n")

    return overall_score

"""
Function details
"""
def user_result(data):
    if data < 13:
        print("No psychopathy\n")
        print("You answered this quiz consistent with people who would not generally be considered a psychopath by research methods currently used to quickly screen for psychopathy in the population.")

    elif data < 18:
        print("Psychopathy possible\n")
        print("You answered this quiz consistent with people who have moderately elevated scores on measures of psychopathy and psychopathic behavior. This may suggest a tendency for some psychopathic behaviors, especially when such behaviors result in your personal gain.")

    else :
        print("Psychopathy Likely\n")
        print("You answered this quiz consistent with people who score high on measures of psychopathy and psychopathic behavior. This high score suggests that you likely have psychopathic tendencies.")


"""
Function details
"""
def display_emotional_intelligence_questions():
    emotional_intelligence_sheet = SHEET.worksheet('emotional_intelligence')
    data = emotional_intelligence_sheet.get_all_values()

    question_count = 1
    overall_score = 0

    while question_count < 21:
        question = data[question_count][0]
        print(f"\nQuestion {question_count}: {question}\n")
        question_count = question_count + 1

        option_one = data[0][1]
        print(f"1: {option_one}")
        option_two = data[1][1]
        print(f"2: {option_two}")
        option_three = data[2][1]
        print(f"3: {option_three}\n")

        user_answer = input("Please select 1, 2 or 3: \n")
        print(f"You have chosen: {user_answer}")

        if int(user_answer) == 1:
            score_this_question = 0
        elif int(user_answer) == 2:
            score_this_question = 1
        elif int(user_answer) == 3:
            score_this_question = 2
        else :
            print("Input Error")
        print(f"Your score this question is {score_this_question}\n")

        
        overall_score = int(overall_score) + int(score_this_question)
        print(f"Your overall score so far is {overall_score}\n")


def main():
    #user_grade = display_test_questions()
    #user_result(user_grade)
    display_emotional_intelligence_questions()


main()