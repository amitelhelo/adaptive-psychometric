from PsychoProject.PracticeSessions.GeneralPracticeSessionAndResultsGUI import GeneralPracticeSessionAndResultsGUI
from tkinter import *


class GeneralPracticeSessionResultsGUI(GeneralPracticeSessionAndResultsGUI):

    def __init__(self, session_results, graph_session=False):
        super().__init__(session_results, graph_session)
        self.session_results = self.practice_session
        self.wrong_answer_checkbox_color = "#CB4335"
        self.right_answer_checkbox_color = "#28B463"
        self.wrong_answer_radio_color = "#F5B7B1"
        self.right_answer_radio_color = "#ABEBC6"
        self.no_answer_checkbox_color = "#FEF5E7"
        self.exit_str = "exit_results_color"
        self.exit_button_resize_length = 90

    def set_root_title_text(self):
        super().set_root_title_text()
        self.root_title_text += ", " + self.practice_session.practice_session.start_date

    def columns_configure_answers_frame(self):
        self.answers_frame.grid_columnconfigure(0, weight=1)
        self.answers_frame.grid_columnconfigure(4, weight=1)

    def set_answers_buttons(self):
        if self.run_first_time:
            self.initiate_answers_buttons()
            self.disable_buttons()
            self.buttons["skip"].grid_forget()
        else:
            self.undo_former_answers_colors()
        self.select_and_color_current_answers_for_question()
        self.set_prev_and_next_buttons()

    def disable_buttons(self):
        for k in range(1, 5):
            self.answers_buttons[k].configure(state=DISABLED)

    def set_prev_and_next_buttons(self):
        self.set_prev_button()
        self.set_next_button()

    def set_prev_button(self):
        prev_str = "prev"
        if prev_str not in self.buttons:
            self.initiate_prev_button(prev_str)
        if self.session_results.question_number_in_session == 1:
            self.buttons[prev_str].configure(state=DISABLED)
        else:
            if str(self.buttons[prev_str]['state']) == 'disabled':
                self.buttons[prev_str].configure(state=NORMAL)

    def initiate_prev_button(self, prev_str):
        self.buttons[prev_str] = Button(self.answers_frame, bg=self.status_frame_color,
                                        activebackground=self.status_frame_color,
                                        command=lambda: self.session_results.switch_to_next_or_prev_question(0))
        self.set_and_configure_button_image(prev_str)
        self.buttons[prev_str].grid(row=0, column=1, padx=20)

    def grid_answers_buttons_frame(self):
        self.answers_buttons_frame.grid(row=0, column=2, sticky=NSEW)
        self.answers_buttons_final_answers_frame.grid(row=1, column=0, sticky=NSEW)

    def set_next_button(self):
        next_str = "next"
        if next_str not in self.buttons:
            self.initiate_next_button(next_str)
        if self.session_results.question_number_in_session == len(self.session_results.ordered_checked_questions):
            self.buttons[next_str].configure(state=DISABLED)
        else:
            if str(self.buttons[next_str]['state']) == 'disabled':
                self.buttons[next_str].configure(state=NORMAL)

    def initiate_next_button(self, next_str):
        if next_str not in self.buttons:
            self.buttons[next_str] = Button(self.answers_frame, activebackground=self.status_frame_color,
                                            command=lambda: self.session_results.switch_to_next_or_prev_question(1),
                                            bg=self.status_frame_color)
            self.set_and_configure_button_image(next_str, height=30)
            self.buttons[next_str].grid(row=0, column=3, padx=20)
            self.buttons[next_str].grid_propagate(False)

    def undo_former_answers_colors(self):
        former_right_answer = self.session_results.last_checked_question.question.right_answer
        former_answer_chosen = self.session_results.last_checked_question.answer_chosen
        if former_answer_chosen is not None and former_right_answer != former_answer_chosen:
            self.answers_buttons[former_answer_chosen].configure(bg=self.answers_buttons_color)
        self.answers_buttons[former_right_answer].configure(bg=self.answers_buttons_color)

    def select_and_color_current_answers_for_question(self):
        right_answer = self.session_results.current_checked_question.question.right_answer
        self.color_right_answer(right_answer)
        answer_chosen = self.session_results.current_checked_question.answer_chosen
        if answer_chosen is None:
            self.answer_chosen_gui.set(None)
        else:
            self.select_and_color_chosen_answer(answer_chosen, right_answer)
        self.color_draft_answers_when_setting_question()

    def color_right_answer(self, right_answer):
        self.answers_buttons[right_answer].configure(bg=self.right_answer_radio_color)

    def set_draft_answer_after_pressing_button(self, answer_marked_as_right_or_wrong):
        self.draft_checkbuttons[answer_marked_as_right_or_wrong].deselect()

    def select_and_color_chosen_answer(self, answer_chosen, right_answer):
        self.answers_buttons[answer_chosen].select()
        if answer_chosen != right_answer:
            self.answers_buttons[answer_chosen].configure(bg=self.wrong_answer_radio_color)

    def set_question_button(self, question_num_in_session):
        super().set_question_button(question_num_in_session)
        checked_question = self.practice_session.ordered_checked_questions[question_num_in_session - 1]
        self.set_question_button_color(checked_question.answered_right_or_wrong, question_num_in_session)

    def undo_question_color(self):
        checked_question = self.practice_session.current_checked_question
        self.set_question_button_color(checked_question, checked_question.number_in_session)

    def set_question_button_color(self, answered_right_or_wrong, question_num_in_session):
        if answered_right_or_wrong == 1:
            self.questions_buttons[question_num_in_session].configure(selectcolor=self.right_answer_checkbox_color)
        elif answered_right_or_wrong == 0:
            self.questions_buttons[question_num_in_session].configure(selectcolor=self.wrong_answer_checkbox_color)
        else:
            self.questions_buttons[question_num_in_session].configure(selectcolor=self.no_answer_checkbox_color)

    def set_question_gui(self):
        super().set_question_gui()
        self.deselect_question()

    def set_status_bar(self):
        super().set_status_bar()
        self.set_questions_menu_frame()
