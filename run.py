# Import
import os
import gspread
from google.oauth2.service_account import Credentials
from quiz import Quiz
from colorama import Fore, Back, Style
import pyfiglet

# Main Heading
ascii_banner = pyfiglet.figlet_format("Ego Echo")
print(ascii_banner)

# Set up scope and authenication
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

# Set variables to connect to google sheet
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('ego_echo')


"""
Display menu with 3 options to the user.
Validate that user chooses an interget between 1 and 3.
Return the choice made by user
"""


def display_menu():

    print("Welcome to " + Fore.RED + Style.BRIGHT +
          "Ego Echo \n")
    print(Style.RESET_ALL)
    print("We have three psychological self-assessment tests \
           for you to choose from. \n")

    # https://psychcentral.com/quizzes/self-esteem-test

    print("1 - Psychopathy Self Assessment")
    print("2 - Emotional Intelligence Self Assessment")
    print("3 - Self-Esteem Self Assessment\n")

    # Adapted from
    # https://stackoverflow.com/questions/23294658/asking-the-user-for-input-until-they-give-a-valid-response
    # Input vaidation
    min_val = 1
    max_val = 3

    while True:
        try:
            menu_choice = int(input("Please select 1, 2 or 3\n"))

        except ValueError:
            print("Sorry, I didn't understand that.")
            continue
        if menu_choice < min_val:
            print(f"Please enter an integer within the range of \
                  {min_val} to {max_val}.")
        elif menu_choice > max_val:
            print(f"Please enter an integer within the range of\
                                  {min_val} to {max_val}.")
        else:
            # Input successfully parsed
            break

    # Set quiz based on user choice
    if menu_choice == 1:
        quiz_choice = "psychopathy"
    elif menu_choice == 2:
        quiz_choice = "emotional_intelligence"
    elif menu_choice == 3:
        quiz_choice = "self_esteem"

    # call display_questions function passing it user selection
    user_grade = display_questions(quiz_choice)
    # call user_result function
    user_result(user_grade)


"""
Accept the quiz choice made by user.
Access google sheet based on that choice
Create instance of Quiz class based on choice
Display quiz questions
Validate user input
Saved user resposes and add these to current instance of Quiz
Return instance of class
"""


def display_questions(quiz_choice):

    # Set variable to access google sheet based on user choice
    data_sheet = SHEET.worksheet(quiz_choice)
    data = data_sheet.get_all_values()

    # Set initaial variables for class
    title = data[0][2]
    introduction = data[0][0]
    questions = ""
    answers = data_sheet.col_values(2)
    score = []
    feedback = ""

    # Create instance of Quiz based on user choice
    current_quiz = Quiz(title, introduction, questions, answers,
                        score, feedback)

    row_count = len(data)

    print(Fore.RED + Style.BRIGHT + current_quiz.title)
    print(Style.RESET_ALL)
    print(current_quiz.introduction)

    current_quiz.score = []
    question_count = 1

    # Display questions and prompt for user reply
    while question_count < row_count:

        current_quiz.questions = data[question_count][0]
        print(f"\nQuestion {question_count}: {current_quiz.questions}\n")

        answer_count = 0
        number_of_possible_answers = len(current_quiz.answers)

        while answer_count < number_of_possible_answers:
            print(f"{answer_count + 1}: \
                  {current_quiz.answers[answer_count]}\n")
            answer_count = answer_count + 1

        question_count = question_count + 1

        # Validate user input
        min_val = 1
        max_val = len(current_quiz.answers)

        while True:
            try:
                user_answer = int(input("Please make a selection\n"))

            except ValueError:
                print("Sorry, I didn't understand that.")
                continue

            if user_answer < min_val:
                print(f"Please enter an integer within the range of \
                      {min_val} to {max_val}.")
            elif user_answer > max_val:
                print(f"Please enter an integer within the range of \
                      {min_val} to {max_val}.")
            else:
                # Input successfully parsed
                break

        # Save user scores in a list
        current_quiz.score.append(int(user_answer))

    # Return instance of class
    return current_quiz


"""
Accept instance of Quiz
Score quiz based on user respones already stored in instance
Display resuls and feedback to user
"""


def user_result(current_quiz):

    os.system('clear')

    # Diaplay results and fedback to user depnding
    # on quiz chosen
    if current_quiz.title == "Psychopathy Self Assessment":

        # Add all scores together from list
        total_score = sum(current_quiz.score)

        # Display feedback based on score range
        if total_score < 13:
            print("No psychopathy\n")
            print("You answered this quiz consistent with people who would \
            not generally be considered a psychopath by research methods \
            currently used to quickly screen for psychopathy in the \
            population.\n")

        elif total_score < 18:
            print("Psychopathy possible\n")
            print("You answered this quiz consistent with people who have \
            moderately elevated scores on measures of psychopathy \
            and psychopathic behavior. This may suggest a tendency \
            for some psychopathic behaviors, especially when such \
            behaviors result in your personal gain.\n")

        else:
            print("Psychopathy Likely\n")
            print("You answered this quiz consistent with people who score \
            high on measures of psychopathy and psychopathic behavior. \
            This high score suggests that you likely have psychopathic \
            tendencies.\n")

    elif current_quiz.title == "Self-Esteem Self Assessment":

        # Add all scores together from list
        total_score = sum(current_quiz.score)

        # Display feedback based on score range
        if total_score < 11:
            print("Your Results: Low Self-Esteem\n")
            print("You scored in the 0-10 range, which indicates you may have \
            low self-esteem. You may have trouble liking yourself or \
            feeling confident about who you are. As a result, you may turn \
            to others and outside sources (career, relationship, \
            financial status) to judge yourself and your worth. You likely \
            compare yourself to others and fear you’re not good enough as \
            you are. \n")
            print("Although you show signs of low self-esteem, this is just \
            your starting point. Anyone can develop high self-esteem and \
            learn to accept who they are.\n")
        elif total_score < 22:
            print("Your Results: Mid Self-Esteem\n")
            print("You scored in the 11-21 range, which indicates you have \
            moderate self-esteem. Although you may likely seek outside \
            validation and can be your own harshest critic at times, you \
            have begun to identify some things you like about yourself.\n")
            print("You’re still developing your sense of self and discovering \
            where you fit in the world.\n")
            print("You can work on your self-esteem through any combination \
            of selfhelp tools, journal prompts, and therapy.\n")
        else:
            print("Your Results: High Self-Esteem\n")
            print("You scored in the 22-32 range, which indicates you have \
            high self-esteem. Confidence and self-worth either come \
            naturally to you or you’ve already begun the work of accepting \
            who you are and discovering what you have to offer.\n")
            print("You understand that what matters most is how you view \
            yourself and are able to recover when outside perspectives shake \
            your confidence at times. You’re OK with making mistakes and \
            don’t judge yourself too harshly for being imperfect. You may \
            still have insecurities but you’re aware of them and don’t let \
            them control your life.\n")

    elif current_quiz.title == "Emotional Intelligence Self Assessment":

        # https://stackoverflow.com/questions/6632188/explicitly-select-items-from-a-list-or-tuple

        print("Your score on these four components of Emotional \
        Intelligence can range from a low of 5 to a high of 25. \
        Any component where your score is below 18 is an area in \
        which you could improve.\n")

        # Score for this quiz is split into 4 categories,
        # with a seperate score for each.
        # 5 set questions relate to category.
        # Split overall score list into 4 seperate lists
        # (one of each category)
        # Get the sum of each of these lists for users scores
        self_aware = [current_quiz.score[index] for
                      index in [0, 4, 18, 11, 14]]
        self_aware_total = sum(self_aware)
        print(f"Your Self Aware score is {self_aware_total}")

        self_manage = [current_quiz.score[index] for
                       index in [2, 5, 9, 12, 17]]
        self_manage_total = sum(self_manage)
        print(f"Your Self Manage score is {self_manage_total}")

        social_awareness = [current_quiz.score[index] for
                            index in [3, 6, 13, 16, 18]]
        social_awareness_total = sum(social_awareness)
        print(f"Your Social Awareness score is {social_awareness_total}")

        relationship_management = [current_quiz.score[index] for
                                   index in [1, 7, 10, 15, 19]]
        relationship_management_total = sum(relationship_management)
        print(f"Your Relationship Management score is \
              {relationship_management_total}\n")

    else:
        print("Something not quite right")

    print("\n")

    # Display disclaimer to user
    # (from Quiz class. Same disclaimer for all quizes)
    print(Fore.RED + Style.BRIGHT + current_quiz.disclaimer)
    print(Style.RESET_ALL)


"""
Main function
"""


def main():

    display_menu()
    exit()


main()
