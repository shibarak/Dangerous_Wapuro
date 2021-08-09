from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter.messagebox import askyesno
from tkinter.filedialog import asksaveasfilename
from random import choice
from prompts import PROMPTS

DARK_GREY = "#D1CEBD"
LIGHT_GREY = "#F6EEDF"
ORANGE = "#F57B51"
RED = "#D63447"
FONT_NAME = "Courier"
FONT_FADE = [LIGHT_GREY, "#c4bdb1", "#918c83", "#5e5b55", "#403d39", "#1c1b19"]

class Dangerous:
    def __init__(self):
        self.time = 999999999999

        # ------- Set up UI ----------- #
        self.window = Tk()
        self.window.title("Dangerous WaPuRo")
        self.window.config(padx=40, pady=10)
        self.canvas = Canvas()
        self.canvas.config(
            width=900,
            height=650,
        )
        image = PhotoImage(file="bg.png")
        self.canvas.create_image(450, 325, image=image)
        self.canvas.grid(row=0, column=0)
        self.text_box = ScrolledText(wrap="word")
        self.text_box.config(bg=LIGHT_GREY,
                             fg="black",
                             insertbackground="black",
                             width=70,
                             height=30,
                             font=(FONT_NAME, 18, "normal"),
                             borderwidth=0,
                             highlightthickness=0,
                             padx=20,
                             pady=20)
        self.text_box.frame.grid(row=0, column=0)
        self.text_box.tag_configure("prompt", justify="center")
        self.text_box.insert("1.0", "Start typing or choose a writing prompt from the dropdown menu.\n"
                                    "Remember, everything you've written will disappear if you stop typing "
                                    "for more than 10 seconds!\n\n")
        self.text_box.tag_add("prompt", "1.0", "3.0")
        self.text_box.tag_configure("text", justify="left")
        self.text_box.tag_add("text", "prompt.last", END)
        self.text_box.tag_raise("text", "prompt")
        self.text_box.see(END)
        self.text_box.bind("<Key>", self.reset_timer)
        self.genre_var = StringVar(self.window)
        self.genres = {'None', 'Mystery / Thriller', 'Romance', 'Science Fiction', 'Fantasy / Paranormal',
                       'General Fiction', 'Religion / Spirituality', 'Travel / Adventure', 'Horror', 'Children’s',
                       'Young Adult', 'Random'}
        self.genre_var.set('None')
        self.genre_label = Label(text="Choose a writing prompt genre:", fg=LIGHT_GREY, font=("Arial", 14, "normal"), )
        self.genre_label.grid(row=1, column=0, pady=2, padx=2)
        self.genre_drop = OptionMenu(self.window, self.genre_var, *self.genres, command=self.choose_genre)
        self.genre_drop.config(width=15,
                               height=2,
                               )
        self.genre_drop.grid(row=2, column=0, pady=2, padx=2)
        self.timer()
        self.window.mainloop()

    # Timer method counts down to zero and slowly fades the text to the background color if the timer gets
    # below 7 seconds.
    def timer(self):
        self.time -= 1
        if self.time > 0:
            if self.time <= 6:
                self.text_box.config(fg=FONT_FADE[self.time-1])
            self.window.after(1000, self.timer)
        else:
            if askyesno("Time's up!", "Time's up!\nWould you like to save?"):
                self.save_text()
            self.text_box.delete("1.0", "end")
            self.text_box.config(fg="black")
            self.time = 99999999
            self.timer()

    # Method for saving the output as a .txt file
    def save_text(self):
        data = self.text_box.get("1.0", END)
        if "more than 10 seconds!" in data:  # remove instructions from output text if no prompt is used
            data = data.split("more than 10 seconds!")[1]

        file_path = asksaveasfilename(filetypes=(
                    ("Text files", "*.txt"),
                    ("All files", "*.*"),
                )
            )
        try:
            with open(file_path, "w") as file:
                file.write(data)
            return
        except FileNotFoundError:
            return

    # Method to reset the timer to 10 seconds every time a key is pressed
    def reset_timer(self, x):
        self.time = 10
        self.text_box.config(fg="black")

    # Method for choosing a writing prompt from the drop down menu,
    # displaying it, and getting the screen ready for writing #
    def choose_genre(self, var):
        self.time = 9999999999  #set time to a high number so timer doesn't run out
        self.text_box.delete("1.0", "end")
        self.text_box.config(fg="black")
        if var == "Random":
            rand_genre = choice(list(PROMPTS))
            prompt = choice(PROMPTS[rand_genre])
        elif var == "None":
            return
        else:
            prompt = choice(PROMPTS[var])
            print(prompt)
        self.text_box.insert("1.0", f"{prompt}\n\n")
        self.text_box.tag_add("prompt", "1.0", "3.0")
        self.text_box.tag_add("text", "prompt.last", END)
        self.text_box.tag_raise("text", "prompt")
        self.text_box.see("end")
        self.text_box.bind("<Key>", self.reset_timer)




