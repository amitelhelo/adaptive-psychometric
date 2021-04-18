# TODO solved questions and mistakes to fix should be dictionaries with categories as keys
# TODO create GUI for student's page. should be the main page for the website
# TODO mistakes to check: remember at what date the mistake occurred


class Student:

    def __init__(self, name):
        self.name = name
        self.solved_questions = None
        self.practice_sessions_results = None
        self.levels_per_subject = None
        self.mistakes_to_fix = None

    def update_solved_questions(self, question):
        if self.solved_questions is None:
            self.solved_questions = {}
        if question.difficulty not in self.solved_questions:
            self.solved_questions[question.difficulty] = set()
        self.solved_questions[question.difficulty].add(question)

    def have_not_solved_question(self, question):
        if (self.solved_questions is None) \
                or (question.difficulty not in self.solved_questions) \
                or (question not in self.solved_questions[question.difficulty]):
            return True
        return False

    def update_session_results(self, session_results):
        if self.practice_sessions_results is None:
            self.practice_sessions_results = set()
        self.practice_sessions_results.add(session_results)

    def __repr__(self):
        return "Student: " + self.name + "\n" + "Practice Sessions: " + str(self.practice_sessions_results)
