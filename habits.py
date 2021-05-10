import tkinter as tk
import json
import bs4
import requests
import random


# Define fonts and colours
blue = "#29335C"
yellow = "#F3A712"
title_font = ("Candara", 20)
main_font = ("Candara", 14)


# Define Functions
def get_daily_quote():
    """Scrape a quote website and obtain a random page and quote, along with the author.
    Returns a string to be used underneath the title. Will change upon each open."""

    random_num = random.randint(1, 9)
    url = requests.get("https://quotes.toscrape.com/page/" + str(random_num) + "/")
    quote_soup = bs4.BeautifulSoup(url.text, "lxml")

    daily_quotes = quote_soup.select(".text")
    daily_authors = quote_soup.select(".author")

    daily_quotes_list = []
    daily_authors_list = []

    for i in range(1, 10):
        daily_quotes_list.append(daily_quotes[i].text)
        daily_authors_list.append(daily_authors[i].text)

    quote_author_random_number = random.randint(1, 10)
    return daily_authors_list[quote_author_random_number] + ": " + daily_quotes_list[quote_author_random_number]


root = tk.Tk()
root.title("Habit Breaker")
root.iconbitmap("thumbs_up.ico")
root.geometry("500x500")
root.resizable(0, 0)
root.config(bg=blue)

title_frame = tk.Frame(root)
title_frame.pack(padx=5, pady=5)

title = tk.Label(title_frame, text="Habit Breaker", font=title_font, bg=yellow, width=60)
title.pack()

root.mainloop()

print(get_daily_quote())