from PsychoProject.PracticeSessions.GeneralPracticeSessionResults import GeneralPracticeSessionResults


class CATPracticeSessionResults(GeneralPracticeSessionResults):

    def __init__(self, practice_session):
        self.category = None
        super().__init__(practice_session)

    def set_status(self):
        super().set_status()
        self.status += ", equivalence class: " + str(self.current_question.equivalence_class)
        self.status += ", fixing a mistake: " + str(self.current_checked_question.fixing_a_mistake)
