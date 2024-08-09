# https://www.w3schools.com/python/python_classes.asp

class Quiz:
    def __init__(self, title, introduction, questions, answers, score, feedback):
        self.title = title
        self.introduction = introduction
        self.questions = questions
        self.answers = answers
        self.score = score
        self.feedback = feedback
        self.disclaimer = "This is just an online quiz, dont take it seriously!!! \n"

    # Should be returned when the class object is represented as a string.
    def __str__(self):
        return f"{self.title} - {self.introduction}"

    


