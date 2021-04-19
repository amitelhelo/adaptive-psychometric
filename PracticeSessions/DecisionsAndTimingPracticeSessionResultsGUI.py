from PsychoProject.PracticeSessions.GeneralPracticeSessionResultsGUI import GeneralPracticeSessionResultsGUI
from tkinter import *


class DecisionsAndTimingPracticeSessionResultsGUI(GeneralPracticeSessionResultsGUI):
    def __init__(self, session_results, graph_session=True):
        super().__init__(session_results, graph_session)
        self.time_spent = None
        self.time_should_have_spent = None

    def set_status_bar(self):
        super().set_status_bar()
        self.set_time_spent_on_question()
        self.set_time_should_have_spent_on_question()

    def set_time_spent_on_question(self):
        self.answers_frame.configure(height=65)
        text = "Time spent on question: "
        text += str(self.practice_session.current_checked_question.time_spent_on_question) + " seconds"
        self.set_time_spent_label(text)

    def set_time_spent_label(self, text):
        if self.time_spent is None:
            self.initiate_time_spent_label(text)
        else:
            self.time_spent.configure(text=text)

    def initiate_time_spent_label(self, text):
        self.time_spent = Label(self.answers_frame, text=text, font=self.small_buttons_font,
                                bg=self.main_frame_color)
        self.time_spent.grid(row=1, column=0, padx=15, columnspan=3)

    def set_time_should_have_spent_on_question(self):
        text = "Time should have spent on question: "
        text += str(self.practice_session.current_question.time_for_question) + " seconds"
        self.set_time_should_have_spent_label(text)

    def set_time_should_have_spent_label(self, text):
        if self.time_should_have_spent is None:
            self.initiate_time_should_have_spent_label(text)
        else:
            self.time_should_have_spent.configure(text=text)

    def initiate_time_should_have_spent_label(self, text):
        time_should_have_spent = Label(self.answers_frame, text=text, font=self.small_buttons_font,
                                       bg=self.main_frame_color)
        time_should_have_spent.grid(row=1, column=2, padx=15, columnspan=4)
