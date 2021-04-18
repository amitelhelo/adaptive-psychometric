from tkinter import *
from PsychoProject.PracticeSessions.GraphQuestionsGUI import GraphQuestionsGUI
from PsychoProject.general_functions_for_picking_questions import get_question_label, get_question_image

buttons_address = r'C:\PsychometricProjectData\buttons'


class GeneralPracticeSessionAndResultsGUI:

    def __init__(self, practice_session, graph_session=False):
        self.practice_session = practice_session
        self.is_graph_session = graph_session
        self.graph_gui = None
        self.root = None
        self.root_title_text = None
        self.main_frame = None
        self.status_frame = None
        self.status_bar = None
        self.question_frame = None
        self.question_label = None
        self.answers_frame = None
        self.answers_buttons_frame = None
        self.answers_buttons_final_answers_frame = None
        self.answers_buttons_draft_answers_frame = None
        self.answers_buttons = {}
        self.show_draft_answers_button = None
        self.now_showing_draft_answers = False
        self.draft_checkbuttons = {}
        self.pick_answer_lbl = None
        self.draft_lbl = None
        self.draft_answers_initiated = False
        self.answer_chosen_gui = None
        self.run_first_time = True
        self.questions_menu_frame = None
        self.questions_menu_frame_height = None
        self.questions_buttons = {}
        self.variables = {m: 0 for m in range(1, 21)}
        self.orange_button_color = "#dd661e"
        self.main_frame_color = "#D5D8DC"
        self.status_frame_color = self.main_frame_color
        self.questions_menu_frame_color = "#e5e6eb"
        self.answers_frame_color = self.status_frame_color
        self.answers_buttons_color = self.questions_menu_frame_color
        self.answers_buttons_frame_color = self.questions_menu_frame_color
        self.buttons_font = "Tahoma 13"
        self.small_buttons_font = "Tahoma 11 italic"
        self.very_small_buttons_font = "Tahoma 8 italic"
        self.buttons_address = buttons_address
        self.buttons = {}
        self.buttons_images = {}
        self.exit_str = "exit"
        self.exit_button_resize_length = 130
        self.show_draft_bar_str = "show_draft"
        self.hide_draft_bar_str = "hide_draft"

    def initiate_session(self):
        self.root = Tk()
        self.main_frame = LabelFrame(self.root, highlightbackground="red", highlightthickness=0,
                                     bg=self.main_frame_color)
        self.main_frame.grid(row=0, column=0, sticky=NSEW)
        self.set_root_title()
        if self.is_graph_session:
            self.graph_gui = GraphQuestionsGUI(self)

    def set_root_title(self):
        self.set_root_title_text()
        self.root.title(self.root_title_text)

    def set_root_title_text(self):
        category = self.practice_session.category
        if category is None:
            category = self.practice_session.practice_session.category
        self.root_title_text = "Practice Session: " + category

    def set_question_frame(self):
        if self.is_graph_session:
            self.graph_gui.set_question_frame()
            return
        if not self.run_first_time:
            self.forget_last_question_widgets()
        self.initiate_question_frame()
        self.set_question_label()

    def initiate_question_frame(self):
        self.question_frame = LabelFrame(self.main_frame, bg='white')
        self.question_frame.grid(row=1, column=0, sticky=NSEW)

    def forget_last_question_widgets(self):
        if self.is_graph_session:
            self.graph_gui.forget_last_question_widgets()
            return
        self.forget_question_frame_widget()

    def forget_question_frame_widget(self):
        self.question_frame.grid_forget()

    def set_question_label(self):
        self.question_label = get_question_label(self.practice_session.current_question.address, self.question_frame)

    def set_answers_frame(self):
        if self.run_first_time:
            self.initiate_answers_frames()

    def initiate_answers_frames(self):
        self.initiate_answers_frame()
        self.initiate_answers_buttons_frame()
        self.columns_configure_answers_frame()

    def initiate_answers_frame(self):
        self.initiate_answers_buttons_frame()
        self.answers_frame = LabelFrame(self.main_frame, bg=self.status_frame_color)
        self.answers_frame.grid(row=2, column=0, columnspan=2, sticky=EW)

    def initiate_answers_buttons_frame(self):  # TODO fix the label on the side bug
        self.answers_buttons_frame = LabelFrame(self.answers_frame)
        self.answers_buttons_final_answers_frame = LabelFrame(self.answers_buttons_frame,
                                                              bg=self.answers_buttons_frame_color)
        self.grid_answers_buttons_frame()
        self.set_draft_answers_frame()

    def set_draft_answers_frame(self):
        self.answers_buttons_draft_answers_frame = LabelFrame(self.answers_buttons_frame,
                                                              bg=self.answers_buttons_frame_color)

    def grid_answers_buttons_draft_answers_frame(self):
        self.answers_buttons_draft_answers_frame.grid(row=0, column=0)

    def grid_answers_buttons_frame(self):
        self.answers_buttons_frame.grid(row=0, column=1, sticky=NSEW)
        self.answers_buttons_final_answers_frame.grid(row=1, column=0, sticky=NSEW)

    def columns_configure_answers_frame(self):
        self.answers_frame.grid_columnconfigure(0, weight=4)
        self.answers_frame.grid_columnconfigure(2, weight=3)

    def set_answers_buttons(self):
        if self.run_first_time:
            self.initiate_answers_buttons()
        else:
            self.answer_chosen_gui.set(None)  # deselect button answer from last question

    def color_draft_answers_when_setting_question(self):
        for answer in range(1, 5):
            self.set_answer_draft_button(answer)

    def set_draft_white_buttons(self):
        for answer in range(1, 5):
            self.set_draft_button_color(answer, "white")

    def set_answer_draft_button(self, answer):
        color_index = self.practice_session.current_checked_question.draft_answers[answer]
        if color_index == 1:
            color = "#CB4335"
        elif color_index == 2:
            color = "#28B463"
        else:
            color = "white"
        self.set_draft_button_color(answer, color)

    def set_draft_button_color(self, answer, color):
        self.draft_checkbuttons[answer].configure(selectcolor=color)

    def set_draft_answer_after_pressing_button(self, answer_marked_as_right_or_wrong):
        self.draft_checkbuttons[answer_marked_as_right_or_wrong].deselect()
        self.practice_session.current_checked_question.set_draft_wrong_answer(answer_marked_as_right_or_wrong)
        self.set_answer_draft_button(answer_marked_as_right_or_wrong)

    def select_draft_answers(self):
        current_checked_question = self.practice_session.current_checked_question
        if current_checked_question is None or current_checked_question.visiting_question_first_time():
            self.set_draft_white_buttons()
        else:
            self.color_draft_answers_when_setting_question()

    def initiate_answers_buttons(self):
        self.answer_chosen_gui = IntVar()
        for k in range(1, 5):
            self.initiate_answer_button(k)
            self.initiate_draft_checkbox(k)
        self.initiate_show_draft_answers_button()
        self.initiate_skip_button()
        self.initiate_answers_text_labels()
        self.grid_answer_buttons()

    def initiate_answer_button(self, k):
        self.answers_buttons[k] = Radiobutton(self.answers_buttons_final_answers_frame, text=str(k),
                                              font=self.buttons_font, bg=self.answers_buttons_color,
                                              width=4, variable=self.answer_chosen_gui, value=k)

    def initiate_draft_checkbox(self, k):
        self.draft_checkbuttons[k] = Checkbutton(self.answers_buttons_draft_answers_frame, bg=self.answers_buttons_color,
                                                 command=lambda m=k: self.set_draft_answer_after_pressing_button(m))

    def initiate_show_draft_answers_button(self):
        self.create_hide_or_show_draft_button(self.show_draft_bar_str)
        self.create_hide_or_show_draft_button(self.hide_draft_bar_str)
        self.grid_show_or_hide_draft_bar(self.show_draft_bar_str)

    def create_hide_or_show_draft_button(self, hide_or_show_str):
        self.buttons[hide_or_show_str] = Button(self.answers_frame,
                                                command=self.grid_draft_answers,
                                                bg=self.answers_frame_color)
        self.set_and_configure_button_image(hide_or_show_str, resize_length=90)

    def grid_show_or_hide_draft_bar(self, hide_or_show_str):
        self.buttons[hide_or_show_str].grid(row=0, column=0, sticky=E, padx=5)

    def grid_draft_answers(self):
        if not self.now_showing_draft_answers:
            self.buttons[self.show_draft_bar_str].grid_forget()
            self.grid_show_or_hide_draft_bar(self.hide_draft_bar_str)
            if not self.draft_answers_initiated:
                self.draft_answers_initiated = True
                self.initiate_grid_draft_answers()
            self.grid_answers_buttons_draft_answers_frame()
        else:
            self.grid_show_or_hide_draft_bar(self.hide_draft_bar_str)
            self.buttons[self.hide_draft_bar_str].grid_forget()
            self.answers_buttons_draft_answers_frame.grid_forget()
            self.grid_show_or_hide_draft_bar(self.show_draft_bar_str)
        self.now_showing_draft_answers = not self.now_showing_draft_answers

    def initiate_grid_draft_answers(self):
        self.draft_lbl.grid(row=0, column=1, padx=6, pady=2)
        m = 0
        for k in range(1, 5):
            self.draft_checkbuttons[k].grid(row=0, column=2 + m, padx=20, sticky=NS)
            m += 1

    def initiate_answers_text_labels(self):
        self.pick_answer_lbl = Label(self.answers_buttons_final_answers_frame, text="Your answer:",
                                     font=self.buttons_font,
                                     bg=self.answers_buttons_color)
        self.draft_lbl = Label(self.answers_buttons_draft_answers_frame, text="Draft answers:", font="Tahoma 10",
                               bg=self.answers_buttons_color)

    # TODO movie skip_button() the GeneralPracticeSessionGUI
    def initiate_skip_button(self):
        skip_str = "skip"
        self.buttons[skip_str] = Button(self.answers_buttons_frame, bg=self.answers_buttons_frame_color)
        self.set_and_configure_button_image(skip_str, 120, 25)

    def grid_answer_buttons(self):
        if self.run_first_time:
            self.pick_answer_lbl.grid(row=1, column=1, padx=3)
            m = 0
            for k in range(1, 5):
                self.answers_buttons[k].grid(row=1, column=2 + m, padx=2, sticky=NS)
                m += 1
            self.buttons["skip"].grid(row=1, column=6, padx=15)

    def set_status_bar(self):
        self.practice_session.set_status()
        if self.run_first_time:
            self.initiate_status_frame()
        self.status_bar.configure(text=self.practice_session.status)
        self.status_frame.configure(width=self.question_label.winfo_width())

    def initiate_status_frame(self):
        self.status_frame = LabelFrame(self.main_frame, height=32, bg=self.status_frame_color)
        self.status_frame.grid(row=0, column=0, sticky=NSEW, columnspan=2)
        self.status_frame.grid_propagate(0)
        self.initiate_status_bar()

    def initiate_status_bar(self):
        self.status_bar = Label(self.status_frame, font=self.very_small_buttons_font, bg=self.status_frame_color)
        self.status_bar.grid(row=0, column=0, sticky=NSEW)

    def end_session(self):
        self.root.destroy()

    def set_exit_button(self):
        if self.exit_str not in self.buttons:
            self.buttons[self.exit_str] = Button(self.status_frame, command=self.end_session,
                                                 bg=self.status_frame_color)
            self.set_and_configure_button_image(button_name=self.exit_str, resize_length=self.exit_button_resize_length,
                                                height=25)
            self.buttons[self.exit_str].grid(column=3, row=0, sticky=SE, padx=5)

    def set_question_gui(self):
        if self.is_graph_session:
            self.graph_gui.set_question_gui()
        else:
            self.set_gui_frames()
        if self.run_first_time:
            self.start_program()

    def set_gui_frames(self):
        self.set_question_frame()
        self.set_answers_frame()
        self.set_answers_buttons()
        self.set_status_bar()

    def start_program(self):
        self.set_exit_button()
        self.run_first_time = False
        self.root.mainloop()

    def set_questions_menu_frame(self):
        self.re_grid_frames_for_presenting_menu_frame()
        if self.run_first_time:
            self.initiate_questions_menu_frame()
            self.set_questions_buttons()
        self.color_current_question()

    def initiate_questions_menu_frame(self):
        self.questions_menu_frame = LabelFrame(self.main_frame, bg=self.questions_menu_frame_color)
        self.questions_menu_frame.grid(row=1, column=0, sticky=EW)

    def re_grid_frames_for_presenting_menu_frame(self):
        if self.is_graph_session:
            self.graph_gui.re_grid_frames_for_presenting_menu_frame()
            return
        self.question_frame.grid(column=1)
        self.re_grid_answers_and_status_frames()

    def re_grid_answers_and_status_frames(self):
        self.status_frame.grid_columnconfigure(2, weight=1)

    def set_questions_buttons(self):
        if self.practice_session.num_of_questions_in_session is None:
            self.practice_session.set_num_of_questions_in_session()
        for k in range(1, self.practice_session.num_of_questions_in_session + 1):
            self.set_question_button(k)

    def set_question_button(self, k):
        self.variables[k] = IntVar()
        self.questions_buttons[k] = Checkbutton(self.questions_menu_frame, text=k, variable=self.variables[k],
                                                command=lambda m=k: self.practice_session.switch_to_question(m),
                                                bg=self.questions_menu_frame_color)
        self.questions_buttons[k].grid(row=(k - 1) // 3, column=(k - 1) % 3)

    def color_current_question(self):
        self.questions_buttons[self.practice_session.question_number_in_session].configure(selectcolor="#283747")

    def decide_question_color(self):
        if self.practice_session.answered_question_already(self.practice_session.current_question):
            self.color_answered_questions()
        else:
            self.undo_question_color()

    def color_answered_questions(self):
        self.questions_buttons[self.practice_session.question_number_in_session].configure(
            selectcolor="#85929E")

    def undo_question_color(self):
        self.questions_buttons[self.practice_session.question_number_in_session].configure(selectcolor="white")

    def deselect_question(self, question_number=None):
        if question_number is None:
            question_number = self.practice_session.question_number_in_session
        if self.variables[question_number].get() == 1:
            self.questions_buttons[question_number].deselect()

    def get_button_address(self, filename):
        address = self.buttons_address + "\\" + filename + '.png'
        return address

    def set_button_image(self, button_name, resize_length):
        if button_name not in self.buttons_images:
            button_image_address = self.get_button_address(button_name)
            button_image = get_question_image(button_image_address, resize_length=resize_length)
            self.buttons_images[button_name] = button_image

    def set_and_configure_button_image(self, button_name, resize_length=150, height=30):
        self.set_button_image(button_name, resize_length=resize_length)
        bg_color = self.buttons[button_name].cget('background')
        self.buttons[button_name].configure(image=self.buttons_images[button_name], height=height, borderwidth=0,
                                            activebackground=bg_color)
