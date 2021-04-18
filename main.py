from PsychoProject.Classes.Student import Student
from PsychoProject.PracticeSessions.CATPracticeSession import CATPracticeSession
# check why the import takes so much time (about 0.5 seconds)
from PsychoProject.PracticeSessions.TimerPracticeSession import TimerPracticeSession


def start_practice_timer():
    student = Student("Haim Moshe")
    practice_session = TimerPracticeSession(student, "general")
    practice_session.initiate_session()
    practice_session.session_results.initiate_results_presentation()


def start_practice_cat():
    student = Student("Haim Moshe")
    practice_session = CATPracticeSession(student, "geometry")
    practice_session.initiate_session()
    practice_session.session_results.initiate_results_presentation()


start_practice_cat()
start_practice_timer()
