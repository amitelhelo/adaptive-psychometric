from PsychoProject.Classes.Student import Student
from PsychoProject.PracticeSessions.CATPracticeSession import CATPracticeSession
from PsychoProject.PracticeSessions.DecisionsAndTimingPracticeSession import DecisionsAndTimingPracticeSession

# TODO check why the CATPracticeSession import takes so long (about 0.5 seconds)


def start_practice_timer():
    student = Student("Haim Moshe")
    practice_session = DecisionsAndTimingPracticeSession(student, "general")
    practice_session.initiate_session()
    practice_session.session_results.initiate_results_presentation()


def start_practice_cat():
    student = Student("Haim Moshe")
    practice_session = CATPracticeSession(student, "geometry")
    practice_session.initiate_session()
    practice_session.session_results.initiate_results_presentation()


start_practice_cat()
start_practice_timer()
