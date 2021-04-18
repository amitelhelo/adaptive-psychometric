class Graph:

    def __init__(self, graph_id, full_graph_address, graph_address, questions=None):
        self.graph_id = graph_id
        self.questions = questions
        self.full_graph_address = full_graph_address
        self.graph_address = graph_address

    def __repr__(self):
        return str(self.graph_id)
