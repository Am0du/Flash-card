from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}


try:
    data = pandas.read_csv('data/words_to_french.csv')
except FileNotFoundError:
    original_data = pandas.read_csv('data/french_words.csv')
    data_dict = original_data.to_dict(orient='records')
else:
    data_dict = data.to_dict(orient='records')


def generate_word():
    global data_dict
    global current_card, event_id
    window.after_cancel(event_id)
    current_card = random.choice(data_dict)
    current_card_french = current_card['French']
    canvas.itemconfig(canvas_image, image=front_card)
    canvas.itemconfig(title, text='French', fill='Black')
    canvas.itemconfig(word, text=current_card_french, fill='black')
    event_id = window.after(2000, func=flip_card)


def right_button():
    global current_card
    data_dict.remove(current_card)
    learn_words = pandas.DataFrame(data_dict)
    learn_words.to_csv('data/words_to_french.csv', index=False)
    generate_word()


def flip_card():
    global current_card
    current_card_english = current_card['English']
    canvas.itemconfig(canvas_image, image=back_card)
    canvas.itemconfig(word, text=current_card_english, fill='white')
    canvas.itemconfig(title, text='English', fill='white')



window = Tk()
window.title('Flashy')
window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)

event_id = window.after(2000, func=flip_card)

front_card = PhotoImage(file='images/card_front.png')
back_card = PhotoImage(file='images/card_back.png')
right_img = PhotoImage(file='images/right.png')
wrong_img = PhotoImage(file='images/wrong.png')

canvas = Canvas(height=600, width=800, highlightthickness=0, bg=BACKGROUND_COLOR)
canvas_image = canvas.create_image(400, 300, image=front_card)
title = canvas.create_text(400, 150, text='French', font=('Helvetica', 40, 'italic'))
word = canvas.create_text(400, 300, text='Word', font=('Helvetica', 60, 'bold'))
canvas.grid(row=0, column=0, columnspan=2)

wrong_btn = Button(image=wrong_img, highlightthickness=0, command=generate_word)
wrong_btn.grid(row=1, column=0)
right_btn = Button(image=right_img, highlightthickness=0, command=right_button)
right_btn.grid(row=1, column=1)

generate_word()
window.mainloop()
