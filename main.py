import random

import pandas as pd
from tkinter import *

BACKGROUND_COLOR = "#B1DDC6"
WORDS_TO_LEARN_PATH = "./data/words_to_learn.csv"
ENGLISH_WORDS_PATH = "./data/english_words.csv"

english_df = pd.read_csv(ENGLISH_WORDS_PATH)
dict_of_words = english_df.to_dict(orient="records")
current_card = {}


def delete_row_from_csv(path_to_csv, card):
    english_df = pd.read_csv(path_to_csv)
    dict_of_words = english_df.to_dict(orient="records")
    dict_of_words.remove(card)
    pd.DataFrame(dict_of_words).to_csv(path_to_csv, index=False)


def add_to_learn(card):
    df_to_learn = pd.DataFrame()
    try:
        df_to_learn = pd.read_csv(WORDS_TO_LEARN_PATH)
    except (FileNotFoundError, pd.errors.EmptyDataError):
        df_to_learn.to_csv(WORDS_TO_LEARN_PATH, mode="a", index=False)
    finally:
        df_to_learn.append(card, ignore_index=True)
        # df_to_learn.to_csv(WORDS_TO_LEARN_PATH, mode="a", index=False)


def right_button_clicked():
    global current_card
    next_card()
    delete_row_from_csv(ENGLISH_WORDS_PATH, current_card)


def wrong_button_clicked():
    global current_card
    next_card()
    delete_row_from_csv(ENGLISH_WORDS_PATH, current_card)
    add_to_learn(current_card)


def next_card():
    global flip_timer
    global current_card
    window.after_cancel(flip_timer)
    current_card = random.choice(dict_of_words)
    rank = dict_of_words.index(current_card) + 1
    english_word = current_card["english"]

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
rank_text = canvas.create_text(400, 400, font=("Arial", 10))

right_img = PhotoImage(file="./images/right.png")
right_button = Button(image=right_img, highlightthickness=0, relief="flat", border=0, command=right_button_clicked)
wrong_img = PhotoImage(file="./images/wrong.png")
wrong_button = Button(image=wrong_img, highlightthickness=0, relief="flat", border=0, command=wrong_button_clicked)

canvas.grid(columnspan=2)
right_button.grid(row=1, column=1)
wrong_button.grid(row=1, column=0)

next_card()
window.mainloop()
