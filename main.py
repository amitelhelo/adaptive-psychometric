from PsychoProject.Classes.Student import Student
from PsychoProject.PracticeSessions.CATPracticeSession import CATPracticeSession
from PsychoProject.PracticeSessions.DecisionsAndTimingPracticeSession import DecisionsAndTimingPracticeSession

# TODO check why the CATPracticeSession import takes so long (about 0.5 seconds)


student1 = Student("Haim Moshe")


def start_timing_and_decisions_practice(student):
    practice_session = DecisionsAndTimingPracticeSession(student, "general")
    practice_session.initiate_session()
    practice_session.session_results.initiate_results_presentation()


def start_cat_practice(student):
    practice_session = CATPracticeSession(student, "geometry")
    practice_session.initiate_session()
    practice_session.session_results.initiate_results_presentation()


start_cat_practice(student1)
start_timing_and_decisions_practice(student1)
