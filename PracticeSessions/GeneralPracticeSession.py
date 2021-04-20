from PsychoProject.Classes.CheckedQuestion import CheckedQuestion
from PsychoProject.LoadQuestions.GenerateQuestions import add_to_dict
from PsychoProject.LoadQuestions.LoadQuestionsFromDatabase import load_questions_from_database
from PsychoProject.PracticeSessions.GeneralPracticeSessionGUI import GeneralPracticeSessionGUI
from PsychoProject.PracticeSessions.GeneralPracticeSessionResults import GeneralPracticeSessionResults
from datetime import datetime
from PsychoProject.general_functions_for_picking_questions import get_item_from_set


# TODO move current_checked_question here from TimerPracticeSession
class GeneralPracticeSession:

    def __init__(self, student, category, db_address, how_many_questions=12, current_difficulty=1,
                 gui=None, session_results=None, is_graph_session=False):
        self.questions_dict, self.equivalence_classes_dict = load_questions_from_database(db_address, category)
        self.student = student
        if gui is None:
            self.gui = GeneralPracticeSessionGUI(self)
        else:
            self.gui = gui
        self.category = category
        self.start_date = None
        self.set_start_date()
        self.current_difficulty = current_difficulty
        self.status = None
        self.num_of_questions_in_session = how_many_questions
        self.current_question = None
        self.last_question = None
        self.question_number_in_session = None
        self.next_difficulty = None
        self.answer_chosen = None
        self.answered_right_or_wrong = None
        self.next_question = None
        self.current_checked_question = None
        self.session_has_ended = False
        if session_results is None:
            self.session_results = GeneralPracticeSessionResults(self)
        else:
            self.session_results = session_results
        self.graph_index = None
        self.is_graph_session = is_graph_session

    def set_start_date(self):
        start_date = datetime.now()
        self.start_date = str(start_date).split('.')[0]

    def initiate_session(self):
        self.gui.initiate_session()
        if self.is_graph_session:
            self.set_graph_index()
        self.next_difficulty = self.current_difficulty
        self.next_question = self.get_first_question()
        self.question_number_in_session = 0
        self.set_current_question()

    def set_current_question(self):
        self.set_question_number_in_session()
        self.current_question = self.next_question
        if self.current_question is not None:
            self.current_difficulty = self.current_question.difficulty
        self.next_question = None
        self.set_current_checked_question()
        self.gui.set_question_gui()

    def set_question_number_in_session(self):
        self.question_number_in_session += 1

    def check_answer_choose_and_set_next(self, answer_chosen):
        self.check_answer(answer_chosen)
        self.decide_and_add_to_checked_questions()
        if self.should_end_session():
            self.end_session()
        else:
            self.choose_and_set_next_question()

    def decide_and_add_to_checked_questions(self):
        self.add_to_checked_questions()

    def choose_and_set_next_question(self):
        self.choose_next_question()
        self.set_current_question()

    def check_answer(self, answer_chosen):
        self.last_question = self.current_question
        self.answer_chosen = answer_chosen
        if self.current_question.is_answer_correct(self.answer_chosen):
            self.student.update_solved_questions(self.current_question)
            self.answered_right_or_wrong = 1
        else:
            self.answered_right_or_wrong = 0
            self.session_results.add_to_session_mistakes(self.current_question)

    def get_first_question(self):
        pass

    def choose_next_question(self):
        pass

    def skip(self):
        self.last_question = self.current_question

    def set_status(self):
        self.status = "question " + str(self.question_number_in_session) + "/" + str(self.num_of_questions_in_session)
        self.status += ", ""question difficulty: " + str(self.current_question.difficulty) + "/20, "
        self.status += "question id: " + self.current_question.question_id
        self.status += ", equivalence class: " + str(self.current_question.equivalence_class)

    def end_session(self):
        self.session_has_ended = True
        self.student.update_session_results(self.session_results)
        self.gui.end_session()

    def __repr__(self):
        return "Practice Session" + '\n' + str(self.student) + "\n" + "date: " + str(self.start_date)

    def mistook_question_already(self, question):
        if self.session_results.session_mistakes is not None and question in self.session_results.session_mistakes:
            return True
        return False

    def add_to_checked_questions(self):
        self.current_checked_question.update_checked_question(self.answered_right_or_wrong, self.answer_chosen,
                                                              number_in_session=self.question_number_in_session)
        self.session_results.add_question_to_questions_dict(self.current_checked_question)
        self.add_to_ordered_checked_questions(self.current_checked_question)

    def add_to_ordered_checked_questions(self, checked_question):
        self.session_results.ordered_checked_questions.append(checked_question)
        return None

    def should_end_session(self):
        if self.question_number_in_session >= self.num_of_questions_in_session:
            return True
        else:
            return False

    def set_graph_index(self):
        if not self.is_graph_session:
            return None
        for difficulty in range(1, 21):
            question = get_item_from_set(self.questions_dict[difficulty])
            if question.graph is not None:
                self.graph_index = difficulty
                break
        return None

    def get_similar_questions(self):
        return self.equivalence_classes_dict[self.current_question.equivalence_class]

    def set_current_checked_question(self):
        self.current_checked_question = CheckedQuestion(self.current_question)
