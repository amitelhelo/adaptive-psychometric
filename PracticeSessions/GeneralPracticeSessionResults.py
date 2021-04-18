from PsychoProject.Classes.CheckedQuestion import CheckedQuestion
from PsychoProject.PracticeSessions.GeneralPracticeSessionResultsGUI import GeneralPracticeSessionResultsGUI
from PsychoProject.general_functions_for_picking_questions import get_item_from_set


class GeneralPracticeSessionResults:

    def __init__(self, practice_session, gui=None):
        self.practice_session = practice_session
        self.ordered_checked_questions = []
        self.checked_questions_dict = {}
        self.num_of_questions_in_session = None
        self.status = None
        self.session_mistakes = None
        self.current_question = None
        self.current_checked_question = None
        self.last_checked_question = None
        self.answered_questions = None
        self.last_question = None
        self.questions_dict = None
        self.question_number_in_session = 1
        if gui is None:
            self.gui = GeneralPracticeSessionResultsGUI(self)
        else:
            self.gui = gui

    def __repr__(self):
        res = "practice session results, date: " + self.practice_session.start_date
        return res

    def initiate_results_presentation(self):
        if len(self.ordered_checked_questions) == 0:
            return None
        self.questions_dict = self.practice_session.questions_dict
        self.set_answered_questions()
        self.set_first_question()
        self.gui.initiate_session()
        self.gui.set_question_gui()

    def set_first_question(self):
        self.current_checked_question = self.ordered_checked_questions[0]
        self.current_question = self.current_checked_question.question
        return None

    def add_to_session_mistakes(self, question):
        if self.session_mistakes is None:
            self.session_mistakes = set()
        self.session_mistakes.add(question)

    def set_status(self):
        self.status = "Results: " + "question " + str(self.question_number_in_session)
        self.status += "/" + str(len(self.ordered_checked_questions)) + ", ""question difficulty: "
        self.status += str(self.current_question.difficulty) + "/20, question id: " + self.current_question.question_id

    def switch_to_next_or_prev_question(self, next_or_prev):
        if next_or_prev == 1:
            k = 1
        else:
            k = -1
        self.switch_to_question(self.question_number_in_session + k)

    def update_info_and_gui_about_last_question(self):
        self.set_last_checked_question()
        args = self.current_checked_question.answered_right_or_wrong, self.current_checked_question.number_in_session
        self.gui.set_question_button_color(*args)
        return None

    def switch_to_question(self, question_number):
        self.update_info_and_gui_about_last_question()
        self.current_checked_question = self.ordered_checked_questions[question_number - 1]
        self.current_question = self.current_checked_question.question
        self.question_number_in_session = self.current_checked_question.number_in_session
        self.gui.set_question_gui()

    def add_question_to_questions_dict(self, checked_question):
        self.checked_questions_dict[checked_question.question] = checked_question

    def set_num_of_questions_in_session(self):
        self.num_of_questions_in_session = len(self.ordered_checked_questions)

    def set_answered_questions(self):  # TODO delete or change into set
        self.answered_questions = {}
        for checked_question in self.ordered_checked_questions:
            self.answered_questions[checked_question.question] = True
        return None

    def set_last_checked_question(self):
        self.last_checked_question = self.current_checked_question
        self.last_question = self.last_checked_question.question
        return None

    def generate_unanswered_checked_question(self, question):
        unanswered_checked_question = CheckedQuestion(question, None, None, number_in_session=question.difficulty)
        self.checked_questions_dict[question] = unanswered_checked_question
        return None

    def set_unanswered_checked_questions(self):  # only relevant for 20 questions chapters
        for difficulty in range(1, 21):
            question = get_item_from_set(self.practice_session.questions_dict[difficulty])
            if question not in self.checked_questions_dict:
                self.generate_unanswered_checked_question(question)
