from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox
from data_manager import Method

BACKGROUND_COLOR = "#B1DDC6"
IMG_PATH = "./images"

class UI:
    def __init__(self):

        self.timer = None
        self.backend = Method()
        self.data_manager = self.backend.data_manager

        self.current_frame = None

        self.window = Tk()

        # Reading all of the images
        self.yes_img = PhotoImage(file=f'{IMG_PATH}/right.png')
        self.no_img = PhotoImage(file=f'{IMG_PATH}/wrong.png')
        self.card_front_img = PhotoImage(file=f'{IMG_PATH}/card_front.png')
        self.card_back_img = PhotoImage(file=f'{IMG_PATH}/card_back.png')

        # ---------------------------- FRAME 1 ------------------------------------ #
        self.select_lang_frame = Frame(self.window, bg='white')

        self.background_img = Label(self.select_lang_frame, image=self.card_back_img)

        # Both Translate from and to have same Values
        self.translate_to_button = Combobox(self.select_lang_frame, width=23, state='readonly', height=8)
        self.translate_from_button = Combobox(self.select_lang_frame, width=23, state='readonly', height=11)
        self.translate_from_button['values'] = self.translate_to_button['values'] = self.data_manager.languages

        self.title = Label(self.select_lang_frame, text='Flash Card', font=('Arial', 40, 'italic'),
                           background='#91C2AF',
                           foreground='white')

        self.translate_from_label = Label(self.select_lang_frame, text='Language to Learn ', font=('Arial', 20),
                                          background='#91C2AF', foreground='white')

        self.translate_to_label = Label(self.select_lang_frame, text='Your Language', font=('Arial', 20),
                                        background='#91C2AF',
                                        foreground='white')

        self.button1 = Button(self.select_lang_frame, width=20, text='Continue',
                              command=self.update_data)

        # ----- SETTING THE UI ---- #
        self.background_img.grid(row=0, column=0, rowspan=10)
        self.title.grid(row=1, column=0, pady=30)
        self.translate_from_label.grid(row=2, column=0)
        self.translate_from_button.grid(row=3, column=0)
        self.translate_to_label.grid(row=4, column=0)
        self.translate_to_button.grid(row=5, column=0, pady=(10, 10))
        self.button1.grid(row=6, column=0, pady=(40, 10))

        # ------------------------------- MAIN FRAME ------------------------------ #

        # Creating the canvas
        self.main_frame = Frame(self.window, bg=BACKGROUND_COLOR)
        self.canvas = Canvas(self.main_frame, width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
        self.canvas_img = self.canvas.create_image(400, 263, image=self.card_front_img)

        # Placing The Text
        self.language_title = self.canvas.create_text(400, 150, text='Title', font=('Arial', 40, 'italic'),
                                                      fill='black')
        self.language_translation = self.canvas.create_text(400, 263, text='word', font=('Arial', 60, 'bold'),
                                                            fill='black')

        self.no_button = Button(self.main_frame, image=self.no_img, bd=0, highlightthickness=0, bg=BACKGROUND_COLOR,
                                activebackground=BACKGROUND_COLOR, command=self.update_data)

        self.yes_button = Button(self.main_frame, image=self.yes_img, bd=0, highlightthickness=0, bg=BACKGROUND_COLOR,
                                 activebackground=BACKGROUND_COLOR,

                                 command=lambda: (self.data_manager.words_known(
                                     self.backend.current_word[self.data_manager.translate_from]
                                 ), self.update_data()))
        # Adds the current word for lang user is translating from to The file in)))

        self.canvas.grid(row=0, column=0, columnspan=2, padx=50, pady=50)
        self.no_button.grid(row=1, column=0)
        self.yes_button.grid(row=1, column=1)

        self.window.eval('tk::PlaceWindow . center')
        self.window.resizable(0, 0)

    # ------------------------------------ FUNCTIONALITY ------------------------------------- #

    def switch_frames(self, frame_name):

        """
        Switches Between 2 Of the frames takes a frame_name and checks if given frame exists
        If it exist we remove it from the screen and pack the other frame
        """

        if frame_name != 'select_lang' and frame_name != 'main':
            raise ValueError("Frame Parameter can only Be loading, select_lang or main")

        try:
            self.current_frame.pack_forget()

        except (TclError, AttributeError):
            pass

        if frame_name == 'select_lang':
            self.current_frame = self.select_lang_frame
            self.window.config(padx=20, pady=20, bg='white')

        elif frame_name == 'main':
            self.current_frame = self.main_frame
            self.window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)

        self.current_frame.pack()
        self.window.eval('tk::PlaceWindow . center')

    def change_canvas(self, canvas_img_to: str, language_title_text: str, text: str, label_color='black'):
        """ This Function Changes The Canvas With respect to the arguments given

        It takes 3 Required Parameters
        1) canvas Image This needs To be one of ('back', 'front') Represents the Images in the card
        2) Language Title This represents The Label in which Language is Displayed
        3) Text is just the text that we want to change the canvas main text to

        Optional Parameters:
        Label & Text Color By Default It is Black
        """

        canvas_img_to = canvas_img_to.lower()

        if canvas_img_to != 'front' and canvas_img_to != 'back':
            raise AttributeError('Canvas Img Parameter Should Only Be front or back')

        if label_color != 'white' and label_color != 'black':
            raise ValueError("Parameter Label Color Must Be white or black")

        if canvas_img_to == 'front':
            canvas_img_to = self.card_front_img
        else:
            canvas_img_to = self.card_back_img

        self.canvas.itemconfig(self.canvas_img, image=canvas_img_to)
        self.canvas.itemconfig(self.language_title, fill=label_color, text=language_title_text)
        self.canvas.itemconfig(self.language_translation, fill=label_color, text=text)


    def enable_disable_buttons(self, mode_: str):
        """ Does Literally what the name says It enables and disabled buttons when called """

        if mode_ == 'enable':
            self.yes_button['state'] = self.no_button['state'] = 'normal'
        elif mode_ == 'disable':
            self.yes_button['state'] = self.no_button['state'] = 'disabled'


    def update_data(self):
        try:
            translate_from_data = self.translate_from_button.get()
            translate_to_data = self.translate_to_button.get()

        except TclError:
            pass

        else:
            # -------------------------- GENERATING ERROR MESSAGE ---------------------------------------- #

            if translate_from_data == translate_to_data or translate_from_data == '' or translate_to_data == '':
                if translate_from_data == '' or translate_to_data == '':
                    msgbox_msg = 'Translate From and Translate to Cannot Be Empty.'
                else:
                    trans = translate_from_data  # Temporary Variable
                    msgbox_msg = f'Cannot translate from {trans} to {trans}'

                messagebox.showerror(title='Error', message=msgbox_msg)
                return

            else:
                # self.backend.update_current_word()
                self.data_manager.translate_from = translate_from_data
                self.data_manager.translate_to = translate_to_data

        if self.backend.still_has_translations():

            self.backend.get_translations()

            self.change_canvas(
                canvas_img_to='front',
                language_title_text=self.data_manager.translate_from,
                text=self.backend.current_word[self.data_manager.translate_from]
            )

            self.enable_disable_buttons(mode_='disable')

            self.timer = self.window.after(3000,
                                           func=lambda: (self.change_canvas(
                                               canvas_img_to='back',
                                               language_title_text=self.data_manager.translate_to,
                                               text=self.backend.current_word[self.data_manager.translate_to],
                                               label_color='white'), self.enable_disable_buttons('enable'))
                                           )


        else:  # If the translate_from is Out Of translations Currently we have 98 Translations for 90 Languages
            self.change_canvas('back', self.data_manager.translate_from, 'Top 100 Completed', label_color='white')

        if self.select_lang_frame.winfo_ismapped():
            # If the current frame Is the selection_frame We load the main frame
            self.switch_frames('main')
