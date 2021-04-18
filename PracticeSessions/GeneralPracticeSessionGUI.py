from PsychoProject.PracticeSessions.GeneralPracticeSessionAndResultsGUI import GeneralPracticeSessionAndResultsGUI


class GeneralPracticeSessionGUI(GeneralPracticeSessionAndResultsGUI):

    def __init__(self, practice_session, graph_session=False):
        super().__init__(practice_session, graph_session)
        self.practice_session = practice_session

    def set_answers_buttons(self):
        super().set_answers_buttons()
        if self.run_first_time:
            self.configure_buttons_commands()
        self.select_draft_answers()
        return None

    def configure_buttons_commands(self):
        for k in range(1, 5):
            self.answers_buttons[k].configure(
                command=lambda: self.practice_session.check_answer_choose_and_set_next(self.answer_chosen_gui.get()))
            self.buttons["skip"].configure(command=self.practice_session.skip)
        return None
