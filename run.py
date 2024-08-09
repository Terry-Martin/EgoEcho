import os
import gspread
from google.oauth2.service_account import Credentials
from quiz import Quiz
from colorama import Fore, Back, Style
import pyfiglet


# Main Heading
ascii_banner = pyfiglet.figlet_format("Ego Echo")
print(ascii_banner)
 
print("Hmmm" + Fore.RED + 'some red text')
print(Fore.BLACK + 'some red text')
print(Back.RED + 'some red text')
print(Back.WHITE + 'some red text')
print(Style.BRIGHT + 'some red text')
print(Style.DIM + 'some red text')
print(Style.RESET_ALL)


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

    print("Welcome to " + Fore.RED + Style.BRIGHT + "Ego Echo \n")
    print(Style.RESET_ALL)
    print("We have three psychological self-assessment tests for you to choose from. \n")

    # https://psychcentral.com/quizzes/self-esteem-test

    print("1 - Psychopathy Self Assessment")
    print("2 - Emotional Intelligence Self Assessment")
    print("3 - Self-Esteem Self Assessment\n")

    # https://stackoverflow.com/questions/23294658/asking-the-user-for-input-until-they-give-a-valid-response

    min_val = 1
    max_val = 3

    while True:
        try:
            menu_choice = int(input("Please select 1, 2 or 3\n"))

        except ValueError:
            print("Sorry, I didn't understand that.")
            continue

        if menu_choice < min_val:
            print(f"Please enter an integer within the range of {min_val} to {max_val}.")
        
        elif menu_choice > max_val:
            print(f"Please enter an integer within the range of {min_val} to {max_val}.")
        
        else:
            # Input successfully parsed
            break

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
    
    print(Fore.RED + Style.BRIGHT + current_quiz.title)
    print(Style.RESET_ALL)
    print(current_quiz.introduction)

    current_quiz.score = []
    question_count = 1

    while question_count < row_count:
        
        os.system('clear')
        current_quiz.questions = data[question_count][0]
        print(f"\nQuestion {question_count}: {current_quiz.questions}\n")

        answer_count = 0
        number_of_possible_answers = len(current_quiz.answers)

        while answer_count < number_of_possible_answers: 
            print(f"{answer_count + 1}: {current_quiz.answers[answer_count]}\n")
            answer_count = answer_count + 1

        question_count = question_count + 1

        min_val = 1
        max_val = len(current_quiz.answers)

        while True:
            try:
                user_answer = int(input("Please make a selection\n"))

            except ValueError:
                print("Sorry, I didn't understand that.")
                continue

            if user_answer < min_val:
                print(f"Please enter an integer within the range of {min_val} to {max_val}.")
            
            elif user_answer > max_val:
                print(f"Please enter an integer within the range of {min_val} to {max_val}.")
            
            else:
                # Input successfully parsed
                break

        current_quiz.score.append(int(user_answer))

    return current_quiz


"""
Function details
"""
def user_result(current_quiz):

    os.system('clear')

    if current_quiz.title == "Psychopathy Self Assessment":

        total_score = sum(current_quiz.score)

        if total_score < 13:
            print("No psychopathy\n")
            print("You answered this quiz consistent with people who would not generally be considered a psychopath by research methods currently used to quickly screen for psychopathy in the population.\n")

        elif total_score < 18:
            print("Psychopathy possible\n")
            print("You answered this quiz consistent with people who have moderately elevated scores on measures of psychopathy and psychopathic behavior. This may suggest a tendency for some psychopathic behaviors, especially when such behaviors result in your personal gain.\n")

        else :
            print("Psychopathy Likely\n")
            print("You answered this quiz consistent with people who score high on measures of psychopathy and psychopathic behavior. This high score suggests that you likely have psychopathic tendencies.\n")
    
    elif current_quiz.title == "Self-Esteem Self Assessment":

        total_score = sum(current_quiz.score)

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
        print(f"Your Relationship Management score is {relationship_management_total}\n")

    else:
        print("Something not quite right")
    
    print("\n")

    print(Fore.RED + Style.BRIGHT + current_quiz.disclaimer)
    print(Style.RESET_ALL)


"""
Function details
"""
def main():
    
    display_menu()
    exit()
   
main()