from tkinter import *
from PsychoProject.PracticeSessions.GeneralPracticeSessionGUI import GeneralPracticeSessionGUI


class TimerPracticeSessionGUI(GeneralPracticeSessionGUI):
    def __init__(self, practice_session):
        super().__init__(practice_session, graph_session=True)
        self.run_timer = True
        self.timer = None
        self.timer_text = None
        self.current_call_to_timer = None
        self.default_button_color = None
        self.never_earned_students_time = True
        self.never_disabled = True
        self.time_left_for_session = 20
        self.time_left_for_session_last_minute = 60
        self.session_timer = None
        self.current_call_to_session_timer = None
        self.pace = 0.1

    def set_status_bar(self):
        super().set_status_bar()
        self.status_frame.configure(height=60)
        self.set_timer(True)
        self.set_questions_menu_frame()
        if self.run_first_time:
            self.set_session_timer()

    def set_timer(self, create_new_timer):
        if create_new_timer:
            self.initiate_timer()
        self.configure_timer_text()
        self.call_timer_again()
        if self.practice_session.time_left_for_current_question == 0:
            self.practice_session.force_skipping()

    def call_timer_again(self):
        if self.practice_session.time_left_for_current_question > 0 and self.run_timer is True:
            self.current_call_to_timer = self.timer.after(int(1000 * self.pace), self.set_timer_and_adjust_time, False)

    def configure_timer_text(self):
        self.set_timer_text()
        self.timer.configure(text=self.timer_text)

    def set_timer_text(self):
        self.timer_text = "Time left for question: " + str(self.practice_session.time_left_for_current_question)

    def initiate_timer(self):
        self.timer = Label(self.status_frame, bg=self.status_frame_color)
        self.timer.grid(row=1, column=1)

    def set_timer_and_adjust_time(self, create_new_timer):
        self.practice_session.time_left_for_current_question -= 1
        self.set_timer(create_new_timer)

    def set_question_gui(self):
        super().set_question_gui()

    def start_program(self):
        self.practice_session.set_current_checked_question()  # TODO should be in TimerPracticeSession
        super().start_program()

    def set_session_timer(self):
        if self.session_timer is None:
            self.initiate_session_timer()
        if self.time_left_for_session >= 1:
            self.update_time_in_minutes()
        elif self.time_left_for_session_last_minute > 0:
            self.update_time_in_seconds()
        else:  # self.time_left_for_session_last_minute == 0
            return self.session_timer.after(1500, self.end_session())

    def update_time_in_minutes(self):
        text, time_for_next_call = self.get_time_in_minutes()
        self.time_left_for_session -= 1
        self.call_session_timer(text, time_for_next_call)

    def update_time_in_seconds(self):
        text, time_for_next_call = self.get_time_in_seconds()
        self.time_left_for_session_last_minute -= 1
        self.call_session_timer(text, time_for_next_call)

    def call_session_timer(self, text, time_for_next_call):
        self.session_timer.configure(text=text)
        self.current_call_to_session_timer = self.session_timer.after(time_for_next_call, self.set_session_timer)

    def get_time_in_minutes(self):
        text = "Time left for session: " + str(self.time_left_for_session) + " minutes"
        time_for_next_call = int(60 * 1000 * self.pace)
        return text, time_for_next_call

    def get_time_in_seconds(self):
        text = "Time left for session: " + str(self.time_left_for_session_last_minute) + " seconds"
        time_for_next_call = int(1000 * self.pace)
        return text, time_for_next_call

    def initiate_session_timer(self):
        self.session_timer = Label(self.status_frame, bg=self.status_frame_color)
        self.session_timer.grid(row=1, column=3)

    def set_answers_buttons(self):
        super().set_answers_buttons()
        self.select_button_in_answered_question()

    def select_button_in_answered_question(self):
        question = self.practice_session.current_question
        checked_question = self.practice_session.current_checked_question
        if self.practice_session.answered_question_already(question):
            self.answer_chosen_gui.set(checked_question.answer_chosen)

    def disable_questions_buttons(self):
        for index in self.practice_session.no_time_questions_indices:
            self.disable_question_button(index)

    def disable_question_button(self, k):
        self.questions_buttons[k].configure(state=DISABLED)

    def enable_disabled_buttons(self):
        for index in self.practice_session.no_time_questions_indices:
            self.questions_buttons[index].configure(state=NORMAL)

    def set_answers_frame(self):
        super().set_answers_frame()
        self.set_finish_session_button()

    def set_finish_session_button(self):
        finish_str = "finish"
        if finish_str not in self.buttons:
            self.buttons[finish_str] = Button(self.answers_frame, command=self.practice_session.end_session,
                                              bg=self.status_frame_color)
        self.set_and_configure_button_image("finish")
        self.buttons[finish_str].grid(row=0, column=2, padx=7, sticky=E)

    def stop_old_timer(self):
        self.timer.destroy()
