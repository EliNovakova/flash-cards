from tkinter import *
import pandas
from random import randint, choice
BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
words_to_learn_dict = {}

# ---------------------------- Code and functions ------------------------------- #
try:    # tries to oped csv with words we have yet to learn (exists only if we played before)
    words_to_learn_dataframe = pandas.read_csv("data/words_to_learn.csv")

except FileNotFoundError:   # if file doesn't exist, opens csv with all the words
    all_words_dataframe = pandas.read_csv("data/french_words.csv")  # opens csv, reads it and creates dataframe
    words_to_learn_dict = all_words_dataframe.to_dict(orient="records")  # dataframe to list of dicts, orient helps us to display it nicely as in one card

else:   # creates list of dicts from dataframe if file with words yet to learn exists
    words_to_learn_dict = words_to_learn_dataframe.to_dict(orient="records")


def next_card():
    """Randomly generates next card with French word."""
    global current_card, flip_timer
    window.after_cancel(flip_timer) # every time we get a next card, the timer stops and then resets (we create it again at the end of the function)
    current_card = choice(words_to_learn_dict)  # random choice of a card
    french_word = current_card["French"]    # gets hold of the French word on the card
    canvas.itemconfig(card_title, text="French", fill="black")    # changes text on canvas (on the actual card)
    canvas.itemconfig(card_word, text=french_word, fill="black")  # changes text on canvas (on the actual card) to chosen French word
    canvas.itemconfig(canvas_image, image=card_front_img)   # changes canvas image to a front of a card
    flip_timer = window.after(3000, func=flip_card)     # we create a timer


def flip_card():
    """Flips card to display the word in English."""
    canvas.itemconfig(canvas_image, image=card_back_img)    # changes canvas image to a back of a card
    canvas.itemconfig(card_title, text="English", fill="white")     # changes text on canvas ("English")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")    # changes text on canvas to a chosen English translation


def is_known():
    """Removes a card with a word the user knows from the list."""
    words_to_learn_dict.remove(current_card)    # removes current card
    next_card()     # gives us another card
    data = pandas.DataFrame(words_to_learn_dict)    # creates dataframe from list of dicts
    data.to_csv("data/words_to_learn.csv", index=False)     # saves it as csv, index False doesn't add index to it


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Flash cards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card) # establishes the timer for the first time

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
canvas_image = canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(400, 150, text="", font=("Arial", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Arial", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)


right_img = PhotoImage(file="images/right.png")
right_button = Button(image=right_img, highlightthickness=0, command=is_known)
right_button.grid(row=1, column=1)

wrong_img = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_img, highlightthickness=0, command=next_card)
wrong_button.grid(row=1, column=0)

next_card()   # we have to call it here so the moment we run the code card is already randomly chosen and displayed


window.mainloop()