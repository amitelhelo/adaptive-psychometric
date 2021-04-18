

class Question:
    equivalence_classes_dict = {}

    def __init__(self, question_id, category, difficulty, right_answer, address, equivalence_class=None, graph=None):
        self.question_id = question_id
        self.category = category
        self.difficulty = difficulty
        self.right_answer = right_answer
        self.address = address
        self.equivalence_class = equivalence_class
        if graph == "None":
            graph = None
        self.graph = graph
        self.time_for_question = self.get_time_for_question()

    def __repr__(self):
        return "question id: " + self.question_id

    def print_question_details(self):
        print("question id: " + self.question_id + ", category: " + self.category + ", difficulty: " +
              str(self.difficulty) + ", right answer: " + str(self.right_answer) +
              ", equivalence class: " + str(self.equivalence_class))

    def is_answer_correct(self, answer):
        if answer == self.right_answer:
            return True
        else:
            return False

    def __eq__(self, other):
        if self.question_id == other.question_id:
            return True
        else:
            return False

    def __hash__(self) -> int:
        return hash(self.question_id)

    def get_time_for_question(self):
        times = {40: (1, 2, 3, 4, 5), 50: (6, 7, 8, 9, 10), 70: (11, 12, 13, 14, 15), 80: (16, 17, 18, 19, 20)}
        for time in times:
            if self.difficulty in times[time]:
                return time
