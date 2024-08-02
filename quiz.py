# https://www.w3schools.com/python/python_classes.asp

class Quiz:
    def __init__(self, introduction, questions, answers, score, feedback):
        self.introduction = introduction
        self.questions = questions
        self.answers = answers
        self.score = score
        self.feedback = feedback
        self.disclaimer = "This is just an online quix, dont take it serious"

    # Should be returned when the class object is represented as a string.
    def __str__(self):
        return f"{self.introduction}"

    


