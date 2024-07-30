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
def display_menu():

    #https://psychcentral.com/quizzes/self-esteem-test
    menu_choice = int(input("Please select 1, 2 or 3: \n"))
    if menu_choice == 1:
        user_grade = display_psychopathy_questions()
        user_result(user_grade)
    elif menu_choice == 2:
        emotional_intelligence_grade = display_emotional_intelligence_questions()
        emotional_intelligence_result(emotional_intelligence_grade)
    elif menu_choice == 3:
        self_esteem_grade = display_self_esteem_questions()
        self_esteem_result(self_esteem_grade)


"""
Function details
"""
def display_psychopathy_questions():

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
    all_scores = []

    while question_count < 21:
        question = data[question_count][0]
        print(f"\nQuestion {question_count}: {question}\n")
        question_count = question_count + 1

        print("1: Never")
        print("2: Rarely")
        print("3: Sometimes")
        print("4: Usually")
        print("5: Always")

        user_answer = input("Please select 1, 2, 3, 4 or 5\n")
        print(f"You have chosen: {user_answer}")

        if int(user_answer) == 1:
            score_this_question = 1
        elif int(user_answer) == 2:
            score_this_question = 2
        elif int(user_answer) == 3:
            score_this_question = 3
        elif int(user_answer) == 4:
            score_this_question = 4
        elif int(user_answer) == 5:
            score_this_question = 5
        else :
            print("Input Error")

        print(f"Your score this question is {score_this_question}\n")

        all_scores.append(score_this_question)

    return all_scores


def emotional_intelligence_result(data):

    #https://stackoverflow.com/questions/6632188/explicitly-select-items-from-a-list-or-tuple
    self_aware = [data[index] for index in [0,4,18,11,14]]
    self_aware_total = sum(self_aware)
    print(self_aware_total)

    self_manage = [data[index] for index in [2,5,9,12,17]]
    print(self_manage)

    social_awareness = [data[index] for index in [3,6,13,16,18]]
    print(social_awareness)

    relationship_management = [data[index] for index in [1,7,10,15,19]]
    print(relationship_management)


"""
Function details
"""
def display_self_esteem_questions():
    self_esteem_sheet = SHEET.worksheet('self_esteem')

    data = self_esteem_sheet.get_all_values()

    print("Instructions")
    print("Self-Esteem")

    question_count = 1
    overall_score = 0

    while question_count < 17:
        question = data[question_count][0]
        print(f"\nQuestion {question_count}: {question}\n")
        question_count = question_count + 1

        print("1: Often")
        print("2: Sometimes")
        print("3: Almost never")


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
def self_esteem_result(data):
    if data < 11:
        print("Low Self-Esteem\n")

    elif data < 22:
        print("Mid Self-Esteem\n")

    else :
        print("High Self-Esteem\n")



"""
Function details
"""
def main():

    display_menu()
    

main()