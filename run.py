import os
import gspread
from google.oauth2.service_account import Credentials
from quiz import Quiz


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
    menu_choice = int(input("Please select 1 - psychopathy Test, 2 - Emotional Intelligence Test or 3 - Self-Esteem Test \n"))

    test_validation(menu_choice)

    if menu_choice == 1:
        quiz_choice = "psychopathy"
    elif menu_choice == 2:
        quiz_choice = "emotional_intelligence"
    elif menu_choice == 3:
        quiz_choice = "self_esteem"
    
    user_grade = display_questions(quiz_choice)
    user_result(user_grade)

"""
Function details
"""
def display_questions(quiz_choice):

    data_sheet = SHEET.worksheet(quiz_choice)
    data = data_sheet.get_all_values()

    title = data[0][2]
    introduction = data[0][0]
    questions = ""
    answers = data_sheet.col_values(2)
    score = []
    feedback = ""

    current_quiz = Quiz(title, introduction, questions, answers, score, feedback)

    row_count = len(data)
    print(row_count)
    
    print(current_quiz.introduction)
    print(current_quiz.title)
    print(current_quiz.disclaimer)

    current_quiz.score = []
    question_count = 1

    while question_count < row_count:
        
        #os.system('clear')
        current_quiz.questions = data[question_count][0]
        print(f"\nQuestion {question_count}: {current_quiz.questions}\n")

        answer_count = 0
        number_of_possible_answers = len(current_quiz.answers)

        while answer_count < number_of_possible_answers: 
            print(f"{answer_count + 1}: {current_quiz.answers[answer_count]}\n")
            answer_count = answer_count + 1

        question_count = question_count + 1

        user_answer = input("Please select from the below:\n")
        print(f"You have chosen: {user_answer}\n")

        current_quiz.score.append(int(user_answer))

    return current_quiz


"""
Function details
"""
def user_result(current_quiz):

    if current_quiz.title == "Psychopathy Self Assessment":

        total_score = sum(current_quiz.score)
        print(total_score)

        if total_score < 13:
            print("No psychopathy\n")
            print("You answered this quiz consistent with people who would not generally be considered a psychopath by research methods currently used to quickly screen for psychopathy in the population.")

        elif total_score < 18:
            print("Psychopathy possible\n")
            print("You answered this quiz consistent with people who have moderately elevated scores on measures of psychopathy and psychopathic behavior. This may suggest a tendency for some psychopathic behaviors, especially when such behaviors result in your personal gain.")

        else :
            print("Psychopathy Likely\n")
            print("You answered this quiz consistent with people who score high on measures of psychopathy and psychopathic behavior. This high score suggests that you likely have psychopathic tendencies.")
    
    elif current_quiz.title == "Self-Esteem Self Assessment":

        total_score = sum(current_quiz.score)
        print(total_score)

        if total_score < 11:
            print("Low Self-Esteem\n")

        elif total_score < 22:
            print("Mid Self-Esteem\n")

        else :
            print("High Self-Esteem\n")

    elif current_quiz.title == "Emotional Intelligence Self Assessment":

        #https://stackoverflow.com/questions/6632188/explicitly-select-items-from-a-list-or-tuple
        self_aware = [current_quiz.score[index] for index in [0,4,18,11,14]]
        self_aware_total = sum(self_aware)
        print(f"Your Self Aware score is {self_aware_total}")

        self_manage = [current_quiz.score[index] for index in [2,5,9,12,17]]
        self_manage_total = sum(self_manage)
        print(f"Your Self Manage score is {self_manage_total}")

        social_awareness = [current_quiz.score[index] for index in [3,6,13,16,18]]
        social_awareness_total = sum(social_awareness)
        print(f"Your Social Awareness score is {social_awareness_total}")

        relationship_management = [current_quiz.score[index] for index in [1,7,10,15,19]]
        relationship_management_total = sum(relationship_management)
        print(f"Your Relationship Management score is {relationship_management_total}")

    else:
        print("Something nor quite right")

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
    print(f"Your Self Aware score is {self_aware_total}")

    self_manage = [data[index] for index in [2,5,9,12,17]]
    self_manage_total = sum(self_manage)
    print(f"Your Self Manage score is {self_manage_total}")

    social_awareness = [data[index] for index in [3,6,13,16,18]]
    social_awareness_total = sum(social_awareness)
    print(f"Your Social Awareness score is {social_awareness_total}")

    relationship_management = [data[index] for index in [1,7,10,15,19]]
    relationship_management_total = sum(relationship_management)
    print(f"Your Relationship Management score is {relationship_management_total}")


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
def test_validation(data):
    #Adapted from https://learningdaily.dev/how-to-take-integer-input-in-python-09decb2b129e
    min_val = 1
    max_val = 3

    try:
        number = int(input())
        if min_val <= number <= max_val:
            print(f"Valid input: {number}")
        else:
            print(f"Please enter an integer within the range of {min_val} to {max_val}.")
    except ValueError:
        print("This is not an integer. Please enter a valid integer.")


"""
Function details
"""
def main():
    
    display_menu()
    

main()