from PsychoProject.PracticeSessions.GeneralPracticeSessionGUI import GeneralPracticeSessionGUI


class CATPracticeSessionGUI(GeneralPracticeSessionGUI):

    def __init__(self, practice_session):
        super().__init__(practice_session)
        self.exit_str = "exit_results"
        self.exit_button_resize_length = 90

    def initiate_status_frame(self):
        super().initiate_status_frame()
        self.status_frame.grid_columnconfigure(2, weight=1)
