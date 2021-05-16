import tkinter as tk
import json
import bs4
import requests
import random
import datetime


# Define fonts and colours
blue = "#29335C"
yellow = "#F3A712"
title_font = ("Candara", 20)
main_font = ("Candara", 14)

# Define global variables
habits_list = []
time_list = []


# Define Functions
def load_json_data():
    """Get the data from the json file (if it exists) and load it into the habits list, also inserting those
    elements into the listbox."""

    global habits_list
    global time_list

    try:
        with open("habits.json", "r") as habit_file:
            data = json.loads(habit_file.read())
            habits_list = data
    except:
        habits_list = []

    try:
        with open("times.json", "r") as time_file:
            data = json.loads(time_file.read())
            time_list = data
    except:
        time_list = []

    for i in range(len(habits_list)):
        habits_listbox.insert(tk.END, "Habit: " + habits_list[i] + ", Time: " + convert_time(time_list[i])[0:6])


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
    """Adds a new habit to the habits_listbox widget, and to the appropriate lists."""
    global habits_list
    global time_list

    if habit == "":
        return None
    else:
        habits_listbox.insert(tk.END, "Habit: " + habit + ", Time: " + ">1 day")
        habits_list.append(habit)
        time_list.append(str(datetime.datetime.now().replace(microsecond=0)))


def save_habit_data():
    """Save the data to a json file when the root window has finished running."""
    global habits_list

    with open("habits.json", "w") as file:
        json.dump(habits_list, file)


def save_time_data():
    """Save the time data to a seperate json list"""
    global time_list

    with open("times.json", "w") as file:
        json.dump(time_list, file)


def convert_time(time: str):
    """Is passed a datetime string, will return the difference between then and the current date."""

    if time[0:10] == str(datetime.datetime.now())[0:10]:
        return ">1 day"

    if time[5] == "0":
        return str(datetime.datetime.now() - datetime.datetime(int(time[0:4]), int(time[6:7]), int(time[8:10])))
    else:
        return str(datetime.datetime.now() - datetime.datetime(int(time[0:4]), int(time[5:7]), int(time[8:10])))


def delete_habit(scrollbox):
    """Delete a selected habit from the scrollbox, and the respective lists."""
    global time_list
    global habits_list

    for i in scrollbox.curselection():
        # Split the selection into a list
        value_list = scrollbox.get(i).split()

    # get the index of the selected value
    index = habits_list.index(value_list[1].strip(","))

    for i in range(len(habits_list)):
        if i == index:
            del habits_list[i]
            del time_list[i]
            scrollbox.delete(i)


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

delete_habit_button = tk.Button(root, text="Delete a habit (select from the list)", font=main_font, bg=yellow, width=50, command=lambda: delete_habit(habits_listbox))
delete_habit_button.pack(pady=20)

load_json_data()
root.mainloop()

save_habit_data()
save_time_data()
