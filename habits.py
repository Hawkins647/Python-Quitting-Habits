import tkinter as tk
import json
import bs4
import requests
import random

# TODO: Add habit info to json file, create a timer that will run in the background and display on the listbox, add ability to delete elements from listbox

# Define fonts and colours
blue = "#29335C"
yellow = "#F3A712"
title_font = ("Candara", 20)
main_font = ("Candara", 14)

# Define global variables
habits_list = []


# Define Functions
def load_json_data():
    global habits_list

    """Get the data from the json file (if it exists) and load it into the habits list, also inserting those 
    elements into the listbox."""
    try:
        with open("habits.json", "r") as file:
            data = json.loads(file.read())
            habits_list = data
    except FileNotFoundError:
        habits_list = []

    for val in habits_list:
        habits_listbox.insert(tk.END, "Habit: " + val)


def get_daily_quote():
    """Scrape a quote website and obtain a random page and quote, along with the author.
    Returns a string to be used underneath the title. Will change upon each open."""

    random_num = random.randint(1, 10)
    url = requests.get("https://quotes.toscrape.com/page/" + str(random_num) + "/")
    quote_soup = bs4.BeautifulSoup(url.text, "lxml")

    daily_quotes = quote_soup.select(".text")
    daily_authors = quote_soup.select(".author")

    daily_quotes_list = []
    daily_authors_list = []

    for i in range(1, 9):
        daily_quotes_list.append(daily_quotes[i].text)
        daily_authors_list.append(daily_authors[i].text)

    quote_author_random_number = random.randint(1, 7)
    return daily_authors_list[quote_author_random_number] + ": " + daily_quotes_list[quote_author_random_number]


def add_new_habit(habit):
    """Adds a new habit to the habits_listbox widget."""
    global habits_list

    if habit == "":
        return None
    else:
        habits_listbox.insert(tk.END, "Habit: " + habit)
        habits_list.append(habit)


def save_data():
    global habits_list

    """Save the data to a json file when the root window has finished running."""
    with open("habits.json", "w") as file:
        json.dump(habits_list, file)


root = tk.Tk()
root.title("Habit Breaker")
root.iconbitmap("thumbs_up.ico")
root.geometry("600x600")
root.resizable(0, 0)
root.config(bg=blue)

title_frame = tk.Frame(root, bg=yellow)
title_frame.pack()

main_frame = tk.Frame(root, bg=blue)
main_frame.pack(padx=10, pady=10)

scroll_frame = tk.Frame(main_frame, bg=blue)
scroll_frame.grid(row=0, column=0, padx=10, pady=10)

add_new_frame = tk.Frame(main_frame, bg=blue)
add_new_frame.grid(row=0, column=1, padx=10, pady=10)

title = tk.Label(title_frame, text="Habit Breaker", font=title_font, bg=yellow, width=60)
title.pack()

title_quote = tk.Label(title_frame, text=get_daily_quote(), font=("Candara", 10), bg=yellow, width=98)
title_quote.pack()
title_quote.bind('<Configure>', lambda wrap_text: title_quote.config(wraplength=root.winfo_width()))

habits_listbox = tk.Listbox(scroll_frame, width=50)
habits_listbox.grid(row=0, column=1, sticky='nsew', rowspan=2)
habits_listbox.config(border=2, relief='sunken')

listbox_scroll = tk.Scrollbar(scroll_frame, orient=tk.VERTICAL, command=habits_listbox.yview)
listbox_scroll.grid(row=0, column=0, sticky='nsw', rowspan=2)

add_new_habit_label = tk.Label(add_new_frame, text="Habit Name: ", font=main_font, bg=yellow)
add_new_habit_label.grid(row=0, column=0)

add_new_habit_entry = tk.Entry(add_new_frame, font=main_font, bg=yellow)
add_new_habit_entry.grid(row=1, column=0, pady=35)

add_new_habit_button = tk.Button(add_new_frame, text="Add a new habit", font=main_font, bg=yellow,
                                 command=lambda: add_new_habit(add_new_habit_entry.get()))
add_new_habit_button.grid(row=2, column=0)

load_json_data()
root.mainloop()

save_data()
