import tkinter as tk
from tkinter import ttk, PhotoImage
from tkinter import *

# from PIL import ImageTk, Image
import sqlite3
from sqlite3 import Error
import time


class SongCreatorApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Song App")
        self.retrieveDB()
        self.song_list = []
        self.arr = []
        self.chords_arr = []
        self.chords_arr_new = []
        self.create_ui()

    def retrieveDB(self):

        def execute_query(connection, query):
            cursor = connection.cursor()
            try:

                cursor.execute(query)
                connection.commit()
                print("Query executed successfully")
            except Error as e:
                print(f"The error '{e}' occurred in executing regular query")

        def create_connection(path):
            connection = None
            try:
                connection = sqlite3.connect(path)
                print("Connection to SQLite DB successful")
            except Error as e:
                print(f"The error '{e}' occurred in creating connection")

            return connection

        connection = create_connection("sm_app.sqlite")

        # save to Database
        create_song_table = """CREATE TABLE IF NOT EXISTS songs (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, arrangement TEXT, bpm TEXT, chords TEXT, lyrics TEXT);"""

        execute_query(connection, create_song_table)

        conn = sqlite3.connect("sm_app.sqlite")
        
        curr = conn.execute("SELECT * FROM songs")
        
    def create_ui(self):

        my_style = ttk.Style()
        my_style.configure("TLabel")
        label = tk.Label(self.root, text="Song App", font=(
            "Arial", 38, "bold"), bg="white", fg="black").pack(pady=10)

        ttk.Style().configure("TButton", padding=6, relief="raised", background="#000")
        create_button = ttk.Button(
            self.root, text="Add Song", command=self.create_song).pack(pady=15)

        '''
        img = ImageTk.Image.open("SkyrimMap.png")
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        img_resized=img.resize((screen_width,screen_height)) # new width & height
        my_img=ImageTk.PhotoImage(img_resized)
        '''

        self.song_frame = tk.Frame(self.root)
        self.song_frame.pack(pady=10)
        exit_button = ttk.Button(
            self.root, text="Exit", command=exit).pack(pady=10)
        self.update_song_list()

    def create_song(self):
        song_window = tk.Toplevel(self.root)
        song_window.title("Add Song")

        song_window.resizable(False, False)

        window_height = 800
        window_width = 1000

        screen_width = song_window.winfo_screenwidth()
        screen_height = song_window.winfo_screenheight()

        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2))

        song_window.geometry(
            "{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

        canvas = tk.Canvas(song_window)
        canvas.pack(side='left', fill='both', expand=True)

        vscrollbar = tk.Scrollbar(
            song_window, orient='vertical', command=canvas.yview)
        vscrollbar.pack(side='right', fill='y')

        canvas.configure(yscrollcommand=vscrollbar.set)

        song_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=song_frame,
                             anchor='center', tags='song_frame')
        tk.Label(song_frame, text="Song Name: ",
                 font=("Arial", 14, "bold")).pack(pady=5)
        self.song_name_entry = ttk.Entry(song_frame)
        self.song_name_entry.pack(pady=10)
        tk.Label(song_frame, text="Song Arrangement: ",
                 font=("Arial", 14, "bold")).pack(pady=5)
        self.song_arrangement_entry = ttk.Entry(song_frame)
        self.song_arrangement_entry.pack(pady=10)

        tk.Label(song_frame, text="Song BPM: ", font=(
            "Arial", 14, "bold")).pack(pady=5)
        self.bpm_combobox = ttk.Combobox(
            song_frame, values=[i for i in range(40, 201)])
        self.bpm_combobox.pack(pady=5)
        # self.song_bpm_entry = ttk.Entry(song_frame)
        # self.song_bpm_entry.pack(pady=10)

        tk.Label(song_frame, text="Number of Chords: ",
                 font=("Arial", 14, "bold")).pack(pady=5)
        self.song_chord_num_entry = ttk.Combobox(
            song_frame, values=[i for i in range(1, 21)])
        self.song_chord_num_entry.pack(pady=5)
        # self.song_chord_num_entry = ttk.Entry(song_frame)
        # self.song_chord_num_entry.pack(pady=10)

        submit_button = ttk.Button(
            song_frame, text="Submit", command=self.submit_chord_num)
        submit_button.pack(pady=10)

        tk.Label(song_frame, text="Song Lyrics: ",
                 font=("Arial", 14, "bold")).pack(pady=5)
        self.song_lyrics_entry = tk.Text(
            song_frame, yscrollcommand=vscrollbar.set)
        self.song_lyrics_entry.pack(pady=10, fill='both', expand=True)

        save_button = ttk.Button(
            song_frame, text="Save", command=self.save_song)
        save_button.pack(pady=10)

        canvas.bind('<Configure>', lambda e: canvas.configure(
            scrollregion=canvas.bbox('all')))

    def submit_chord_num(self):

        chords_window = tk.Toplevel(self.root)
        chords_window.title("Chords")
        chords_window.resizable(False, False)
        window_height = 800
        window_width = 1000

        screen_width = chords_window.winfo_screenwidth()
        screen_height = chords_window.winfo_screenheight()

        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2))

        chords_window.geometry(
            "{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

        canvas = tk.Canvas(chords_window)
        canvas.pack(side='left', fill='both', expand=True)

        vscrollbar = tk.Scrollbar(
            chords_window, orient='vertical', command=canvas.yview)
        vscrollbar.pack(side='right', fill='y')
        hscrollbar = tk.Scrollbar(
            chords_window, orient='horizontal', command=canvas.xview)
        hscrollbar.pack(side='bottom', fill='x')

        # canvas.configure(yscrollcommand=vscrollbar.set)
        canvas.configure(yscrollcommand=vscrollbar.set)

        # canvas.configure(xscrollcommand=hscrollbar.set)
        canvas.configure(xscrollcommand=hscrollbar.set)

        chords_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=chords_frame, anchor='center', tags='chords_frame')

        # tk.Label(chords_frame, text="Song Details", font=("Impact", 40, "bold"), bg="black").pack(pady=20)

        canvas.bind('<Configure>', lambda e: canvas.configure(
            scrollregion=canvas.bbox('all')))

        num_chords = (str(self.song_chord_num_entry.get()))

        for i in range(int(num_chords)):

            tk.Label(chords_frame, text="Enter Chord " + str(i+1) +
                     ": ", font=("Arial", 14, "bold")).pack(pady=10)
            self.song_chord_entry = ttk.Combobox(chords_frame, values= ["C", "D", "E", "F", "G", "A", "B"])
            self.song_chord_entry.pack(pady=10)
            self.chords_arr.append(self.song_chord_entry)

        submit_button = ttk.Button(
            chords_frame, text="Submit", command=self.submit_callback)
        submit_button.pack(pady=10)

    def submit_callback(self):
        self.chords_arr_new = [entry.get() for entry in self.chords_arr]  # Retrieve chords

    def save_song(self):

        # entry_text = tk.StringVar()
        new_song = {
            "Name":   self.song_name_entry.get(),
            "Arrangement": self.song_arrangement_entry.get(),
            "BPM": self.bpm_combobox.get(),
            "Chords": self.chords_arr_new,
            "Lyrics": self.song_lyrics_entry.get(1.0, tk.END)
        }

        # "Quest": self.quest_combobox.get().replace("{ } ",  ",")
        # "Name": self.character_name_entry.get()

        def saveDB():

            conn = sqlite3.connect("sm_app.sqlite")
            entry_name = self.song_name_entry.get()
            entry_arrangement = self.song_arrangement_entry.get()
            entry_bpm = self.bpm_combobox.get()
            entry_chords = self.chords_arr_new
            entry_lyrics = self.song_lyrics_entry.get(1.0, tk.END)

            # conn.execute('CREATE TABLE IF NOT EXISTS quests (id INTEGER PRIMARY KEY AUTOINCREMENT, quest TEXT NOT NULL)')

            # conn.execute('INSERT INTO songs (name, arrangement, lyrics) VALUES(?)', (str(entry_name, entry_arrangement, entry_lyrics)))
            if (len(entry_name) > 0):
                conn.execute('INSERT INTO songs (name, arrangement, bpm, chords, lyrics) VALUES(?,?,?,?,?)', (str(
                entry_name), str(entry_arrangement), str(entry_bpm), str(entry_chords), str(entry_lyrics)))
                conn.commit()        

        def execute_read_query(connection, query):
            cursor = connection.cursor()
            result = None
            try:
                cursor.execute(query)
                result = cursor.fetchall()
                return result
            except Error as e:
                print(f"The error '{e}' occurred in read query")

        saveDB()

        self.song_list.append(new_song)
        self.update_song_list()

    def update_song_list(self):

        for widget in self.song_frame.winfo_children():
            widget.destroy()

        canvas = tk.Canvas(self.song_frame, width=1000, height=550)
        canvas.pack(side='left', fill='both', expand=True)

        vscrollbar = tk.Scrollbar(
            self.song_frame, orient='vertical', command=canvas.yview)
        vscrollbar.pack(side='right', fill='y')

        hscrollbar = tk.Scrollbar(
            self.song_frame, orient='horizontal', command=canvas.xview)
        hscrollbar.pack(side='bottom', fill='x')

        canvas.configure(yscrollcommand=vscrollbar.set)
        canvas.configure(xscrollcommand=hscrollbar.set)

        ui_frame = tk.Frame(canvas)
        # ui_frame.pack()
        # ui_frame.place(anchor='center', relx=0.5, rely=0.5)

        canvas.create_window((0, 0), window=ui_frame,
                             anchor='nw', tags='ui_frame')
        canvas.bind('<Configure>', lambda e: canvas.configure(
            scrollregion=canvas.bbox('all')))

        conn = sqlite3.connect("sm_app.sqlite")


        curr = conn.execute("SELECT * FROM songs")

        for c in curr:

           

            
            song_label = tk.Label(ui_frame, text=str(c[1]))
            song_label.config(font=("Arial", 28, "bold"))
            song_label.pack(pady=10)
            song_label.bind("<Button-1>", lambda event, song=str(c[1]), arrangement=str(c[2]), bpm=str(c[3]), chords=str(
                c[4]), lyrics=str(c[5]): self.show_song_details(song, arrangement, bpm, chords, lyrics), song_label.config(relief="raised"))
           

    def show_song_details(self, song, arrangement, bpm, chords, lyrics):

        self.retrieveDB()

        details_window = tk.Toplevel(self.root)
        details_window.title("Song Details")
        details_window.resizable(False, False)
        window_height = 500
        window_width = 900

        screen_width = details_window.winfo_screenwidth()
        screen_height = details_window.winfo_screenheight()

        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2))

        details_window.geometry(
            "{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

        canvas = tk.Canvas(details_window)
        canvas.pack(side='left', fill='both', expand=True)

        vscrollbar = tk.Scrollbar(
            details_window, orient='vertical', command=canvas.yview)
        vscrollbar.pack(side='right', fill='y')
        hscrollbar = tk.Scrollbar(
            details_window, orient='horizontal', command=canvas.xview)
        hscrollbar.pack(side='bottom', fill='x')

        canvas.configure(yscrollcommand=vscrollbar.set)

        canvas.configure(xscrollcommand=hscrollbar.set)

        details_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=details_frame,
                             anchor='center', tags='details_frame')

        tk.Label(details_frame, text="Song Details",
                 font=("Impact", 40, "bold")).pack(pady=20)
        tk.Label(details_frame, text=f"Name: {song}", font=(
            "Arial", 32, "bold")).pack(pady=20)
        tk.Label(details_frame, text=f"Arrangement: {arrangement}", font=(
            "Arial", 32, "bold")).pack(pady=20)
        tk.Label(details_frame, text=f"BPM: {bpm}", font=(
            "Arial", 32, "bold")).pack(pady=20)
        tk.Label(details_frame, text=f"Chords: {chords}", font=(
            "Arial", 32, "bold")).pack(pady=20)
        show_lyrics_button = ttk.Button(details_frame, text="Show Lyrics", command=lambda: [
                                        root.after(500, details_window.destroy()), self.show_lyrics(lyrics)])
        show_lyrics_button.pack(pady=10)

        canvas.bind('<Configure>', lambda e: canvas.configure(
            scrollregion=canvas.bbox('all')))

    def show_lyrics(self, lyrics):

        lyrics_window = tk.Toplevel(self.root)
        lyrics_window.title("Lyrics")
        lyrics_window.resizable(False, False)
        window_height = 800
        window_width = 1400

        screen_width = lyrics_window.winfo_screenwidth()
        screen_height = lyrics_window.winfo_screenheight()
        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2))

        lyrics_window.geometry(
            "{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
        canvas = tk.Canvas(lyrics_window)
        canvas.pack(side='left', fill='both', expand=True)
        
        vscrollbar = tk.Scrollbar(
            lyrics_window, orient='vertical', command=canvas.yview)
        vscrollbar.pack(side='right', fill='y')

        canvas.configure(yscrollcommand=vscrollbar.set)

        lyrics_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=lyrics_frame,
                             anchor='nw', tags='lyrics_frame')

        tk.Label(lyrics_frame, text=f"Lyrics: \n\n{lyrics}", font=(
            "Arial", 28)).pack(pady=10)

        canvas.bind('<Configure>', lambda e: canvas.configure(
            scrollregion=canvas.bbox('all')))


if __name__ == "__main__":

    root = tk.Tk()
    root.config(bg="white")
    #root.attributes('-fullscreen', True)
    #root.resizable(False, False)
    '''
    window_height = 900
    window_width = 900

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x_cordinate = int((screen_width/2) - (window_width/2))
    y_cordinate = int((screen_height/2) - (window_height/2))

    root.geometry(
        "{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
    '''

    app = SongCreatorApp(root)
    root.mainloop()
