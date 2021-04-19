from PsychoProject.Classes.CheckedQuestion import CheckedQuestion
from PsychoProject.PracticeSessions.GeneralPracticeSession import GeneralPracticeSession, get_item_from_set
from PsychoProject.PracticeSessions.DecisionsAndTimingPracticeSessionGUI import TimerPracticeSessionGUI
from PsychoProject.PracticeSessions.DecisionsAndTimingPracticeSessionResults import TimerPracticeSessionResults

db_address1 = r'C:\Users\amit7\PsychoRes\former_tests\PsychoProjectDatabase.xlsx'


class TimerPracticeSession(GeneralPracticeSession):
    def __init__(self, student, category, db_address=db_address1, how_many_questions=20):
        super().__init__(student, category, db_address, gui=TimerPracticeSessionGUI(self),
                         how_many_questions=how_many_questions, session_results=TimerPracticeSessionResults(self),
                         is_graph_session=True)
        self.category = "Timer"
        self.current_checked_question = None
        self.next_checked_question = None
        self.students_time = 0
        self.old_students_time = None
        self.answered_current_question = None
        self.time_left_for_current_question = 0  # what's written on the timer right now
        self.time_spent_on_current_question = 0
        self.no_time_questions_indices = []
        self.students_time_spent_on_current_question = 0
        self.old_time_left_for_current_question = 0
        self.questions_set = {get_item_from_set(self.questions_dict[k]) for k in range(1, 21)}
        self.session_results.set_checked_questions_dict()
        self.session_results.create_students_time_spent_on_questions()

    def get_first_question(self):
        return get_item_from_set(self.questions_dict[1])

    def choose_next_question(self):
        if self.try_to_set_closest_unanswered_question_as_next_question(self.current_difficulty + 1, 21):
            return
        if self.try_to_set_closest_unanswered_question_as_next_question(1, self.current_difficulty):
            return
        self.set_closest_answered_question_as_next_question()

    def set_closest_answered_question_as_next_question(self):
        if self.current_difficulty == 20:
            self.next_difficulty = 1
            self.next_question = get_item_from_set(self.questions_dict[self.next_difficulty])
        else:
            self.next_difficulty += 1
            self.next_question = get_item_from_set(self.questions_dict[self.next_difficulty])

    def try_to_set_closest_unanswered_question_as_next_question(self, min_difficulty, max_difficulty):
        for difficulty in range(min_difficulty, max_difficulty):
            next_question = get_item_from_set(self.questions_dict[difficulty])
            if (not self.answered_question_already(next_question)) and (self.have_time_for_question(next_question)):
                self.next_difficulty, self.next_question = difficulty, next_question
                return True  # found a question
        return False

    def answered_question_already(self, next_question):
        checked_question = self.session_results.checked_questions_dict[next_question]
        if checked_question.answer_chosen is None:
            return False
        return True

    def force_skipping(self):
        self.add_to_no_time_questions_indices()
        self.gui.disable_question_button(self.current_question.difficulty)
        self.skip()

    def add_to_no_time_questions_indices(self):
        self.no_time_questions_indices.append(self.current_question.difficulty)

    def skip(self):
        super().skip()
        self.update_question_info_after_skipping_or_switching()
        self.choose_and_set_next_question()

    def switch_to_question(self, question_number):
        self.gui.deselect_question(question_number)
        self.update_question_info_after_skipping_or_switching()
        self.set_next_question_after_switching(question_number)

    def update_question_info_after_skipping_or_switching(self):
        self.gui.decide_question_color()
        self.update_times_after_skipping_or_switching()
        self.answered_current_question = False
        self.add_to_checked_questions()

    def set_next_question_after_switching(self, question_number):
        self.current_difficulty = question_number
        self.last_question = self.current_question
        self.next_question = get_item_from_set(self.questions_dict[question_number])
        self.set_current_question()

    def set_current_question(self):
        self.set_next_checked_question()
        self.next_checked_question.set_visiting_question_first_time()
        self.set_time_left_for_current_question()
        self.old_time_left_for_current_question = self.time_left_for_current_question
        super().set_current_question()

    def set_time_left_for_current_question(self):
        if self.next_checked_question.visiting_question_first_time():
            self.time_left_for_current_question = self.next_question.time_for_question + self.students_time
        else:
            self.time_left_for_current_question = self.session_results.checked_questions_dict[self.next_question].\
                                                      time_remaining + self.students_time

    def check_answer(self, answer_chosen):
        self.set_answered_current_question(True)
        self.update_times_after_answering_question()
        self.gui.stop_old_timer()  # TODO take to time_remaining from the old timer and stop it before calculations
        self.disable_or_enable_questions()
        self.gui.color_answered_questions()
        super().check_answer(answer_chosen)

    def set_answered_current_question(self, true_or_false):
        self.answered_current_question = true_or_false

    def set_students_time_after_skipping(self):
        time_left = self.time_left_for_current_question
        if time_left <= self.students_time:
            self.students_time = time_left
            self.set_students_time_spent_on_question()

    def set_students_time_after_answering(self):
        if self.time_left_for_current_question > self.students_time:
            self.students_time += self.time_left_for_current_question - self.students_time
        else:
            self.students_time = self.time_left_for_current_question
            self.set_students_time_spent_on_question()
        if self.gui.never_earned_students_time and self.students_time > 0:  # TODO check if needed
            self.gui.never_earned_students_time = False

    def update_times_after_answering_question(self):
        self.update_time_spent_and_old_students_times()
        self.add_to_no_time_questions_indices()
        self.current_checked_question.set_time_remaining(0)
        self.set_students_time_after_answering()

    def update_times_after_skipping_or_switching(self):
        self.update_time_spent_and_old_students_times()
        self.set_time_remaining_for_question()
        self.set_students_time_after_skipping()
        self.gui.stop_old_timer()
        self.disable_or_enable_questions()

    def update_time_spent_and_old_students_times(self):
        self.set_time_spent_on_current_question()
        self.set_old_students_time()

    def set_old_students_time(self):
        self.old_students_time = self.students_time
        return None

    def set_students_time_spent_on_question(self):
        self.students_time_spent_on_current_question = self.old_students_time - self.students_time

    def set_time_remaining_for_question(self):
        if not self.answered_question_already(self.current_question):
            time_remaining = max(self.current_checked_question.time_remaining - self.time_spent_on_current_question, 0)
            self.current_checked_question.set_time_remaining(time_remaining)

    def set_time_spent_on_current_question(self):
        self.time_spent_on_current_question = self.old_time_left_for_current_question \
                                              - self.time_left_for_current_question

    def set_question_number_in_session(self):
        self.question_number_in_session = self.next_question.difficulty
        return None

    def should_end_session(self):
        return False

    def have_time_for_question(self, next_question):
        if self.session_results.checked_questions_dict[next_question].get_time_remaining() > 0 \
                or self.students_time > 0:
            return True
        else:
            return False

    def disable_or_enable_questions(self):
        if self.old_students_time == 0 and self.students_time > 0:
            self.gui.enable_disabled_buttons()
        if self.students_time == 0:
            if (self.old_students_time > 0) or (self.gui.never_earned_students_time and self.gui.never_disabled):
                self.gui.never_disabled = False
                self.gui.disable_questions_buttons()
        return None

    def add_to_checked_questions(self):
        if self.should_only_update_time():
            self.update_time_spent_on_question_in_checked_question()
        else:
            arguments = self.get_arguments_for_checked_question()
            self.current_checked_question.update_checked_question(*arguments)

    def should_only_update_time(self):
        if self.answered_question_already(self.current_question) and self.answered_current_question is False:
            return True
        return False

    def add_to_checked_questions_dict_first_time(self, arguments):
        checked_question = CheckedQuestion(self.current_question, *arguments)
        self.session_results.add_question_to_questions_dict(checked_question)

    def get_arguments_for_checked_question(self):
        if self.answered_current_question:
            arguments = self.answered_right_or_wrong, self.answer_chosen, None, self.question_number_in_session, \
                        self.time_spent_on_current_question
        else:
            arguments = (None, None, None, self.question_number_in_session, self.time_spent_on_current_question)
        return arguments

    def update_time_spent_on_question_in_checked_question(self):
        self.current_checked_question.time_spent_on_question += \
            self.time_spent_on_current_question

    def end_session(self):
        self.set_final_times()
        self.stop_timers()
        self.set_session_results_checked_questions_data_structures()
        super().end_session()

    def set_final_times(self):
        self.set_time_spent_on_current_question()
        self.update_time_spent_on_question_in_checked_question()
        self.gui.run_timer = False

    def stop_timers(self):
        self.gui.stop_old_timer()
        if self.gui.current_call_to_timer is not None:
            self.gui.timer.after_cancel(self.gui.current_call_to_timer)
        if self.gui.current_call_to_session_timer is not None:
            self.gui.session_timer.after_cancel(self.gui.current_call_to_session_timer)

    def set_session_results_checked_questions_data_structures(self):
        self.session_results.set_unanswered_checked_questions()
        self.session_results.set_ordered_checked_questions()

    def set_current_checked_question(self):
        self.current_checked_question = self.session_results.checked_questions_dict[self.current_question]

    def set_next_checked_question(self):
        self.next_checked_question = self.session_results.checked_questions_dict[self.next_question]
