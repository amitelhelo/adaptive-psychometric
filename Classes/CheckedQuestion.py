print(5)

class CheckedQuestion:

    def __init__(self, question, answered_right_or_wrong=None, answer_chosen=None, fixing_a_mistake=None,
                 number_in_session=None, time_spent_on_question=0, visit_question_already=False):
        self.question = question
        self.answered_right_or_wrong = answered_right_or_wrong
        self.answer_chosen = answer_chosen
        self.fixing_a_mistake = fixing_a_mistake
        self.number_in_session = number_in_session
        self.time_spent_on_question = time_spent_on_question
        self.visit_question_already = visit_question_already
        self.time_remaining = self.question.time_for_question
        self.draft_answers = {k: 0 for k in range(1, 5)}

    def update_checked_question(self, answered_right_or_wrong, answer_chosen, fixing_a_mistake=None,
                                number_in_session=None, time_spent_on_question=0):
        self.answered_right_or_wrong = answered_right_or_wrong
        self.answer_chosen = answer_chosen
        self.fixing_a_mistake = fixing_a_mistake
        self.number_in_session = number_in_session
        self.time_spent_on_question += time_spent_on_question

    def get_time_remaining(self):
        return self.time_remaining

    def set_time_remaining(self, time_remaining):
        self.time_remaining = time_remaining

    def visiting_question_first_time(self):  # TODO check why we visit this method twice every question
        return not self.visit_question_already

    def set_visiting_question_first_time(self):
        self.visit_question_already = True

    def set_draft_wrong_answer(self, draft_wrong_answer):
        self.draft_answers[draft_wrong_answer] += 1
        self.draft_answers[draft_wrong_answer] %= 3
