import random

import pandas as pd
from tkinter import *

BACKGROUND_COLOR = "#B1DDC6"
WORDS_TO_LEARN_PATH = "./data/words_to_learn.csv"
ENGLISH_WORDS_PATH = "./data/english_words.csv"

current_card = {}
dict_of_words = {}

try:
    data = pd.read_csv(WORDS_TO_LEARN_PATH)
except FileNotFoundError:
    original_data = pd.read_csv(ENGLISH_WORDS_PATH)
    dict_of_words = original_data.to_dict(orient="records")
else:
    dict_of_words = data.to_dict(orient="records")


def right_button_clicked():
    global current_card
    dict_of_words.remove(current_card)
    pd.DataFrame(dict_of_words).to_csv(WORDS_TO_LEARN_PATH, index=False)
    next_card()


def wrong_button_clicked():
    global current_card
    next_card()


def next_card():
    global flip_timer
    global current_card
    window.after_cancel(flip_timer)
    current_card = random.choice(dict_of_words)
    english_word = current_card["english"]
    rank = current_card["rank"]

    canvas.itemconfig(canvas_background, image=card_front_image)
    canvas.itemconfig(language_text, text="English", fill="black")
    canvas.itemconfig(word_text, text=english_word, fill="black")
    canvas.itemconfig(rank_text, text=f"место {rank} по частоте использования", fill="black")

    flip_timer = window.after(3000, show_translation)


def show_translation():
    russian_word = current_card["russian"]

    canvas.itemconfig(canvas_background, image=card_back_image)
    canvas.itemconfig(language_text, text="Russian", fill="white")
    canvas.itemconfig(word_text, text=russian_word, fill="white")
    canvas.itemconfig(rank_text, fill="white")


window = Tk()
window.title("Flashy")
window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)
flip_timer = window.after(3000, show_translation)

canvas = Canvas()
card_front_image = PhotoImage(file="./images/card_front.png")
card_back_image = PhotoImage(file="./images/card_back.png")
canvas.config(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
canvas_background = canvas.create_image(400, 263, image=card_front_image)

language_text = canvas.create_text(400, 150, font=("Arial", 40, "italic"))
word_text = canvas.create_text(400, 263, font=("Arial", 60, "bold"))
rank_text = canvas.create_text(400, 380, font=("Arial", 14))

right_img = PhotoImage(file="./images/right.png")
right_button = Button(image=right_img, highlightthickness=0, relief="flat", border=0, command=right_button_clicked)
wrong_img = PhotoImage(file="./images/wrong.png")
wrong_button = Button(image=wrong_img, highlightthickness=0, relief="flat", border=0, command=wrong_button_clicked)

canvas.grid(columnspan=2)
right_button.grid(row=1, column=1)
wrong_button.grid(row=1, column=0)

next_card()
window.mainloop()
