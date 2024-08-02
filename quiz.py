# https://www.w3schools.com/python/python_classes.asp

class Quiz:
    def __init__(self, introduction, questions, answers, grade, feedback, disclaimer):
        self.introduction = introduction
        self.questions = questions
        self.answers = answers
        self.grade = grade
        self.feedback = feedback
        self.disclaimer = disclaimer

    # Should be returned when the class object is represented as a string.
    def __str__(self):
        return f"{self.introduction})"


