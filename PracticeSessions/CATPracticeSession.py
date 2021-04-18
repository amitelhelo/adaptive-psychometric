from PsychoProject.PracticeSessions.CATPracticeSessionGUI import CATPracticeSessionGUI
from PsychoProject.PracticeSessions.CATPracticeSessionResults import CATPracticeSessionResults
from PsychoProject.PracticeSessions.GeneralPracticeSession import GeneralPracticeSession
from PsychoProject.functions import choose_difficulties, choose_similar_questions_by_difficulties

db_address1 = r'C:\PsychometricProjectData\PsychoProjectDatabase.xlsx'


class CATPracticeSession(GeneralPracticeSession):

    def __init__(self, student, category, db_address=db_address1, current_difficulty=1):
        super().__init__(student, category, db_address, current_difficulty=current_difficulty,
                         gui=CATPracticeSessionGUI(self), session_results=CATPracticeSessionResults(self))
        self.fixing_a_mistake_stage = False  # stages: False, 1, 2, 3
        self.fixing_a_mistake_questions = None
        self.recently_mistaken = None

    def decide_and_add_to_checked_questions(self):
        if not (self.recently_mistaken is not None and self.recently_mistaken == self.current_question):
            self.add_to_checked_questions()

    def add_to_checked_questions(self):
        super().add_to_checked_questions()
        self.session_results.checked_questions_dict[self.current_question].fixing_a_mistake = \
            self.fixing_a_mistake_stage

    def get_first_question(self):
        return self.find_next_question()

    def choose_next_question(self):
        if self.answered_right_or_wrong == 1:
            self.choose_next_question_after_right_answer()
        else:
            self.choose_next_question_after_wrong_answer()
            return None

    def choose_next_question_after_right_answer(self):
        if self.fixing_a_mistake_stage:
            self.choose_next_question_for_fixing_a_mistake()
        else:
            self.set_difficulty_and_find_more_difficult_question()
        return None

    def choose_next_question_after_wrong_answer(self):
        if self.fixing_a_mistake_stage:
            self.stop_fixing_a_mistake()
        else:
            if self.can_fix_mistake():
                return self.start_fixing_mistake()
        self.set_difficulty_and_find_easier_question()
        return None

    def set_difficulty_and_find_easier_question(self):
        self.next_difficulty = max(self.current_question.difficulty - 1, 1)
        self.next_question = self.find_next_question()
        return None

    def set_difficulty_and_find_more_difficult_question(self):
        self.next_difficulty = min(self.current_question.difficulty + 2, 20)
        self.next_question = self.find_next_question()
        return None

    def find_question_by_difficulty(self, difficulty):
        if difficulty in self.questions_dict:
            for question in self.questions_dict[int(difficulty)]:
                if (self.student.have_not_solved_question(question)) \
                        and ((self.current_question is None) or (question != self.current_question)) and \
                        not self.mistook_question_already(question):
                    return question
        return None

    def find_next_question(self):
        res = self.find_question_by_difficulty(self.next_difficulty)
        if res is not None:
            return res
        else:
            if self.answered_right_or_wrong == 1:
                res = self.find_more_difficult_question(self.next_difficulty)
                if res is None:
                    res = self.find_easier_question(self.next_difficulty)
            else:
                res = self.find_easier_question(self.next_difficulty)
                if res is None:
                    res = self.find_more_difficult_question(self.next_difficulty)
        return res

    def find_more_difficult_question(self, difficulty):
        for i in range(difficulty + 1, 21):
            question = self.find_question_by_difficulty(i)
            if question is not None:
                self.next_difficulty = i
                return question

    def find_easier_question(self, difficulty):
        for i in range(difficulty - 1, 0, -1):
            question = self.find_question_by_difficulty(i)
            if question is not None:
                self.next_difficulty = i
                return question

    def set_status(self):
        super().set_status()
        self.status += ", fixing a mistake: " + str(self.fixing_a_mistake_stage)
        return None

    def fix_the_mistake(self, three_similar_questions):
        for question in three_similar_questions:
            self.next_question = question
            self.set_current_question()

    def choose_next_question_for_fixing_a_mistake(self):
        if self.fixing_a_mistake_stage == 3:
            self.fixing_a_mistake_stage = False
            self.next_question = self.recently_mistaken
        else:
            self.next_question = self.fixing_a_mistake_questions[self.fixing_a_mistake_stage]
            self.fixing_a_mistake_stage += 1

    def can_fix_mistake(self):
        if self.can_fix_mistake_primal_conditions():
            three_similar_questions = self.get_3_similar_questions()
            if three_similar_questions is not None:
                self.fixing_a_mistake_questions = three_similar_questions
                return True
        return False

    def can_fix_mistake_primal_conditions(self):
        if ((self.recently_mistaken is None) or (self.recently_mistaken != self.current_question)) \
                and (self.fixing_a_mistake_stage is False) \
                and (self.current_question.difficulty >= 10):
            return True
        return False

    def start_fixing_mistake(self):
        self.recently_mistaken = self.current_question
        self.fixing_a_mistake_stage = 1
        self.next_question = self.fixing_a_mistake_questions[0]
        return None

    def get_3_similar_questions(self):
        all_similar_questions = self.get_similar_questions()
        if (all_similar_questions is None) or (len(all_similar_questions.values()) < 3):  # .values() -> bad complexity?
            return None
        chosen_difficulties = self.get_difficulties(all_similar_questions)
        three_similar_questions = choose_similar_questions_by_difficulties(chosen_difficulties, all_similar_questions)
        return three_similar_questions

    def get_difficulties(self, all_similar_questions):
        difficulties = sorted(list(all_similar_questions.keys()))
        chosen_difficulties = choose_difficulties(difficulties, self.current_question.difficulty)
        return chosen_difficulties

    def stop_fixing_a_mistake(self):
        self.fixing_a_mistake_stage = False
        self.fixing_a_mistake_questions = None
        self.session_results.add_to_results(self.recently_mistaken, 0)
        self.recently_mistaken = None
        return None

    def skip(self):
        self.next_difficulty = self.current_question.difficulty
        self.question_number_in_session -= 1
        self.next_question = self.find_next_question()
        self.set_current_question()

    def should_end_session(self):
        if self.question_number_in_session >= self.num_of_questions_in_session and not self.fixing_a_mistake_stage:
            return True
        return False
