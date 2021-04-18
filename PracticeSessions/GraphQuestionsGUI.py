from PIL import ImageTk, Image as PIL_Image
from tkinter import *
from PsychoProject.functions import get_question_label, resize


class GraphQuestionsGUI:
    def __init__(self, practice_session_and_results_gui):
        self.session_gui = practice_session_and_results_gui
        self.question_canvas = None
        self.question_canvas_frame = None
        self.scrollbar = None
        self.graph_label = None
        self.graph_image = None
        self.full_graph_window = None
        self.full_graph_label = None
        self.full_graph_exit_button = None
        self.full_graph_window_is_open = False

    # manual override - LATER CHANGE IMPLEMENTATION
    def set_question_frame(self):
        if not self.session_gui.run_first_time:
            self.forget_last_question_widgets()
        if self.solving_a_graph_question():
            self.set_question_frame_for_graph_question()
        else:
            self.session_gui.initiate_question_frame()
        self.session_gui.set_question_label()

    # manual override
    def forget_last_question_widgets(self):
        if self.solved_a_graph_question():
            self.question_canvas_frame.grid_forget()
            if not self.solving_a_graph_question():
                self.forget_all_graph_widgets()
        else:
            self.session_gui.forget_question_frame_widget()

    def forget_all_graph_widgets(self):
        self.unstretch_frames()
        if self.full_graph_window_is_open:
            self.exit_full_graph_window()

    def solved_a_graph_question(self):
        if self.session_gui.practice_session.last_question.graph is None:
            return False
        return True

    # manual override
    def set_question_gui(self):
        self.session_gui.set_gui_frames()
        if self.solving_a_graph_question():
            if self.solving_a_graph_question():
                self.set_full_graph_label()

    # manual override
    def re_grid_frames_for_presenting_menu_frame(self):
        if self.solving_a_graph_question():
            self.question_canvas_frame.grid(column=1)
        else:
            self.session_gui.question_frame.grid(column=1)
        self.session_gui.re_grid_answers_and_status_frames()

    def set_question_frame_for_graph_question(self):
        self.set_question_canvas()
        self.set_question_graph_frame()
        self.set_question_graph_label()
        self.set_scrollbar()
        self.stretch_frames()

    def set_question_canvas(self):
        self.initiate_question_canvas_frame()
        if self.question_canvas_frame.winfo_ismapped() == 0:
            self.question_canvas_frame.grid(row=1, column=0, sticky=NSEW)

    def initiate_question_canvas_frame(self):
        self.question_canvas_frame = Frame(self.session_gui.main_frame)
        self.question_canvas = Canvas(self.question_canvas_frame, height=400, width=1000)
        self.question_canvas.grid(row=0, column=0, sticky=NSEW)
        self.question_canvas.bind('<Configure>', lambda e: self.question_canvas.configure(
            scrollregion=self.question_canvas.bbox(ALL)))

    def set_question_graph_frame(self):
        self.session_gui.question_frame = LabelFrame(self.question_canvas)
        self.question_canvas.create_window((0, 0), window=self.session_gui.question_frame, anchor=NW)

    def set_question_graph_label(self):
        if self.graph_image is None:
            self.set_graph_image()
        self.create_graph_label()
        if self.graph_label.winfo_ismapped() == 0:
            self.graph_label.grid(row=0, column=0)

    def set_graph_image(self):
        graph = self.session_gui.practice_session.questions_dict["graph"]
        tmp_graph_img = PIL_Image.open(graph.graph_address)
        graph_img = resize(tmp_graph_img, length=600)
        self.graph_image = ImageTk.PhotoImage(graph_img)

    def create_graph_label(self):
        self.graph_label = Label(self.session_gui.question_frame, image=self.graph_image)
        self.graph_label.photo = self.graph_image

    def set_scrollbar(self):
        self.scrollbar = Scrollbar(self.question_canvas_frame, orient=VERTICAL, command=self.question_canvas.yview)
        self.scrollbar.grid(row=0, column=1, rowspan=4, sticky=NSEW)
        self.question_canvas.configure(yscrollcommand=self.scrollbar.set)

    def set_full_graph_label(self):
        present_str = "present"
        self.session_gui.buttons[present_str] = Button(self.question_canvas_frame, command=self.open_full_graph)
        self.session_gui.set_and_configure_button_image("present", resize_length=120)
        self.add_to_canvas(self.session_gui.buttons[present_str])

    def open_full_graph(self):
        if self.full_graph_window_is_open:
            self.full_graph_window.lift()
        else:
            self.open_full_graph_first_time()

    def open_full_graph_first_time(self):
        self.full_graph_window = Toplevel(self.session_gui.root)
        args = self.session_gui.practice_session.questions_dict["graph"].full_graph_address, self.full_graph_window
        self.full_graph_label = get_question_label(*args, resize_length=800)
        self.set_full_graph_exit_button()
        self.full_graph_window_is_open = True

    def set_full_graph_exit_button(self):
        exit_str_for_full_graph = "exit_results_color_full_graph"
        self.session_gui.buttons[exit_str_for_full_graph] = Button(self.full_graph_window,
                                                                   command=self.exit_full_graph_window)
        self.session_gui.set_and_configure_button_image(exit_str_for_full_graph, resize_length=90)
        self.session_gui.buttons[exit_str_for_full_graph].grid(row=0, column=0)

    def exit_full_graph_window(self):
        self.full_graph_window.withdraw()
        self.full_graph_window_is_open = False

    def solving_a_graph_question(self):
        if self.session_gui.practice_session.current_question.graph is not None:
            return True
        return False

    def add_to_canvas(self, full_graph_button):
        self.question_canvas.create_window((0, 1), window=full_graph_button, anchor=NW)

    def stretch_frames(self):
        self.session_gui.root.grid_rowconfigure(0, weight=1)
        self.session_gui.main_frame.grid_rowconfigure(1, weight=1)
        self.question_canvas.grid_rowconfigure(0, weight=1)
        self.question_canvas_frame.grid_rowconfigure(0, weight=1)

    def unstretch_frames(self):
        self.session_gui.root.grid_rowconfigure(0, weight=0)
        self.session_gui.main_frame.grid_rowconfigure(1, weight=0)
        self.question_canvas.grid_rowconfigure(0, weight=0)
        self.question_canvas_frame.grid_rowconfigure(0, weight=0)
