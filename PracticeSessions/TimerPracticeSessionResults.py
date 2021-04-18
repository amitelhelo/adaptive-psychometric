from PsychoProject.Classes.CheckedQuestion import CheckedQuestion
from PsychoProject.PracticeSessions.GeneralPracticeSessionResults import GeneralPracticeSessionResults
from PsychoProject.PracticeSessions.TimerPracticeSessionResultsGUI import TimerPracticeSessionResultsGUI
from PsychoProject.general_functions_for_picking_questions import get_item_from_set


class TimerPracticeSessionResults(GeneralPracticeSessionResults):

    def __init__(self, practice_session):
        super().__init__(practice_session, gui=TimerPracticeSessionResultsGUI(self))
        self.category = "Timer"
        self.students_time_spent_on_questions = None
        self.checked_questions_dict = None

    def set_checked_questions_dict(self):  # created when initiating practice session
        self.checked_questions_dict = {question: CheckedQuestion(question, number_in_session=question.difficulty)
                                       for question in self.practice_session.questions_set}

    def create_students_time_spent_on_questions(self):
        self.students_time_spent_on_questions = {question: 0 for question in self.practice_session.questions_set}

    def set_ordered_checked_questions(self):
        for difficulty in range(1, 21):
            question = get_item_from_set(self.practice_session.questions_dict[difficulty])
            if question in self.checked_questions_dict:
                self.ordered_checked_questions.append(self.checked_questions_dict[question])

    def set_time_spent_on_questions(self):
        for question in self.practice_session.questions_set:
            self.checked_questions_dict[question].time_spent_on_question += (
                    question.time_for_question - self.practice_session.time_remaining_for_questions[question])
        return None
