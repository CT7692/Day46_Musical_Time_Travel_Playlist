from tkinter import *
from spotify import *
from tkinter import messagebox
from datetime import datetime
from bs4 import BeautifulSoup
import requests


FONT = "Arial"
SIZE = 12
NUM_WIDTH = 8
PADDING = 20


def process_date(m_text, d_text, y_text):
    month = m_text.get()
    day = d_text.get()
    year = y_text.get()
    if len(month) == 0 or len(day) == 0 or len(year) == 0:
        messagebox.showwarning(title="Entry Error",
                               message="All fields are required. Please try again.")
    else:
        try:
            desired_date = datetime(year=int(year), month=int(month), day=int(day)).strftime("%Y-%m-%d")
        except TypeError:
            error_msg()
        except ValueError:
            error_msg()
        else:
            songs = get_songs(desired_date)
            song_uris = get_song_uris(songs, year)
            playlist_response = spotify_client.create_playlist(desired_date, song_uris)
            window.quit()

def error_msg():
    messagebox.showwarning(title="Entry Error", message="Please enter a valid date.")
    month_input.delete(0, END)
    day_input.delete(0, END)
    year_input.delete(0, END)
    month_input.focus()

def get_songs(date):
    response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}", timeout=60)
    soup = BeautifulSoup(response.text, "html.parser")
    first_song = soup.find(name="h3", class_="c-title a-no-trucate a-font-primary-bold-s "
                                             "u-letter-spacing-0021 u-font-size-23@tablet "
                                             "lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max "
                                             "a-truncate-ellipsis u-max-width-245 u-max-width-230@tablet-only "
                                             "u-letter-spacing-0028@tablet").getText().strip("\n\t")

    song_titles = soup.find_all(name="h3", class_="c-title a-no-trucate a-font-primary-bold-s "
                                          "u-letter-spacing-0021 lrv-u-font-size-18@tablet "
                                          "lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max "
                                          "a-truncate-ellipsis u-max-width-330 u-max-width-230@tablet-only")

    songs = [song.getText().strip('\n\t') for song in song_titles]
    songs.insert(0, first_song)
    return songs

def get_song_uris(songs, year):
    song_uris = []
    for song in songs:
        try:
            response = spotify_client.spotify_search(song, year)
            uri = response["tracks"]["items"][0]["uri"]
        except ValueError as error:
            print(error)
        except TypeError as error:
            print(error)
        except IndexError:
            print("Song not available. Not added.")
        except ConnectionError as error:
            print(error)
        except requests.exceptions.HTTPError as http_error:
            print(http_error)
        else:
            song_uris.append(uri)
    return song_uris


spotify_client = SpotifyDataOperations()

# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Enter Date")
window.config(padx=PADDING, pady=PADDING)
my_canvas = Canvas(width=100, height=100, highlightthickness=0)
window.configure(background='light grey')
prompt_label = Label(text="What particular time are you nostalgic for? Enter the date.", font=(FONT, SIZE))
prompt_label.config(padx=PADDING, pady=PADDING)
prompt_label.configure(background='light grey')

month_label = Label(text="Month:", font=(FONT, SIZE))
month_label.configure(background='light grey')
day_label = Label(text="Day:", font=(FONT, SIZE))
day_label.configure(background='light grey')
month_label.configure(background='light grey')
year_label = Label(text="Year:", font=(FONT, SIZE))
year_label.configure(background='light grey')

month_input = Entry(width=NUM_WIDTH)
day_input = Entry(width=NUM_WIDTH)
year_input = Entry(width=12)

enter = Button(text="Enter", width=10, command=lambda: process_date(month_input, day_input, year_input))

prompt_label.grid(column=1, row=1, columnspan=6)
month_label.grid(column=1, row=2, pady=PADDING)
month_input.grid(column=2, row=2, pady=PADDING, sticky=W)
day_label.grid(column=3, row=2, pady=PADDING)
day_input.grid(column=4, row=2, pady=PADDING, sticky=W)
year_label.grid(column=5, row=2, pady=PADDING)
year_input.grid(column=6, row=2, pady=PADDING, sticky=W)

enter.grid(column=2, row=3, columnspan=4)

window.mainloop()
