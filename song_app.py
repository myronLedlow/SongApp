import os
import threading
from tkinter import ttk, messagebox
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
import pygame
import sqlite3
from sqlite3 import Error
import turtle


class SongCreatorApp:

    def __init__(self, root):
        ''' Initialize vars'''
        self.retrieveDB()
        self.original_dir = os.getcwd()
        self.root = root
        self.root.title("Song Manager")
        self.original_chords = []
        self.transposed_chords = []
        self.song_list = []
        self.arr = []
        self.chords_arr = []
        self.chords_arr_new = []
        self.load_icons()  # Load icons
        pygame.init()
        self.create_ui()
        self.metronome_sound = pygame.mixer.Sound("metronome.wav")
        self.metronome_thread = None
        self.is_metronome_playing = False
        self.metronome_bpm = 120

     # load image icons
    def load_icons(self):

        add_icon_img = (Image.open("images/add_icon_2.png"))
        resized_image = add_icon_img.resize((30, 30))
        self.add_icon = ImageTk.PhotoImage(resized_image)
        edit_icon_img = (Image.open("images/edit_icon_2.png"))
        resized_image = edit_icon_img.resize((30, 30))
        self.edit_icon = ImageTk.PhotoImage(resized_image)
        delete_icon_img = (Image.open("images/delete_icon_2.png"))
        resized_image = delete_icon_img.resize((30, 30))
        self.delete_icon = ImageTk.PhotoImage(resized_image)
        save_icon_img = (Image.open("images/save_icon_2.png"))
        resized_image = save_icon_img.resize((30, 30))
        self.save_icon = ImageTk.PhotoImage(resized_image)
        submit_icon_img = (Image.open("images/submit_icon.png"))
        resized_image = submit_icon_img.resize((30, 30))
        self.submit_icon = ImageTk.PhotoImage(resized_image)
        exit_icon_img = (Image.open("images/exit_icon_2.png"))
        resized_image = exit_icon_img.resize((30, 30))
        self.exit_icon = ImageTk.PhotoImage(resized_image)
        play_icon_img = (Image.open("images/play_icon.png"))
        resized_image = play_icon_img.resize((30, 30))
        self.play_icon = ImageTk.PhotoImage(resized_image)
        pause_icon_img = (Image.open("images/pause_icon.png"))
        resized_image = pause_icon_img.resize((30, 30))
        self.pause_icon = ImageTk.PhotoImage(resized_image)
        stop_icon_img = (Image.open("images/stop_icon.png"))
        resized_image = stop_icon_img.resize((30, 30))
        self.stop_icon = ImageTk.PhotoImage(resized_image)
        metronome_icon_img = (Image.open("images/metronome_icon.png"))
        resized_image = metronome_icon_img.resize((30, 30))
        self.metronome_icon = ImageTk.PhotoImage(resized_image)

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

        # connection = create_connection("sm_app.sqlite")
        db_path = os.path.abspath(os.path.join(
            os.path.dirname(__file__), "sm_app.sqlite"))
        connection = create_connection(db_path)

        # create table in DB
        create_song_table = """CREATE TABLE IF NOT EXISTS songs (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, arrangement TEXT, bpm TEXT, capo TEXT, chords TEXT, transposed_chords TEXT, lyrics TEXT, notes TEXT);"""
        execute_query(connection, create_song_table)
        conn = sqlite3.connect(db_path)
        conn.commit()
        conn.close()

        '''
        drop_table = """Drop Table songs"""
        execute_query(connection, drop_table)
        conn = sqlite3.connect("sm_app.sqlite")
        conn.commit()
        conn.close()
        '''

    def center_window(self, window):
        window_width = 1500
        window_height = 1500
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x_cordinate = int((screen_width / 2) - (window_width / 2))
        y_cordinate = int((screen_height / 2) - (window_height / 2))
        window.geometry("{}x{}+{}+{}".format(window_width,
                        window_height, x_cordinate, y_cordinate))

    def create_ui(self):

        def animate_bg():
            screen_bg.clear()

            for i in range(4):

                screen_bg.pensize(5)
                screen_bg.penup()
                screen_bg.speed(3)
                screen_bg.goto(0, 0)
                screen_bg.color("#0078D4")
                screen_bg.shape('images/notes.gif')
                screen_bg.begin_fill()
                screen_bg.end_fill()
                screen_bg.rt(4)
                screen_bg.fd(8)
                screen_bg.rt(4)

            screen.update()
            screen.ontimer(animate_bg, 100)

        self.style = ttk.Style()
        self.style.configure("TLabel", font=("Arial", 16))
        self.style.configure("TButton", font=(
            "Arial", 14, "bold"), padding=10)
        self.style.configure("TEntry", font=(
            "Arial", 14), padding=10)
        self.style.configure("TCombobox", font=(
            "Arial", 14), bd=0)
        self.style.configure("TText", font=("Arial", 14))
        self.root.configure(bg="#333333")
        self.root.geometry("1500x1000")
        self.root.title("Song Manager")
        self.root.config(bg="white")
        canvas = tk.Canvas(root, width=1500, height=60, bg="#333333")
        canvas.pack()

        # create graphics screen
        screen = turtle.TurtleScreen(canvas)
        screen.register_shape('images/notes.gif')
        # screen.bgcolor("#333333")
        screen.bgcolor("white")
        screen.tracer(0)  # Turn off automatic screen updates
        screen_bg = turtle.RawTurtle(screen)
        # schedule animation
        screen.ontimer(animate_bg, 100)

        # make 1st header
        header_frame = tk.Frame(self.root, bg="white", height=100)
        header_frame.pack(fill="x")
        header_label = tk.Label(header_frame, text="Song Manager", font=(
            "Arial", 34, "bold"), bg="white", fg="#333333", width=100)
        header_label.pack(pady=3)

        # Create Song Button
        create_button = ttk.Button(
            self.root, text=" Add Song", command=self.create_song, style="TButton", image=self.add_icon, compound=LEFT)
        create_button.pack(pady=10)

        # Song List Frame
        self.song_frame = tk.Frame(self.root)
        self.song_frame.pack(fill="both", expand=True)
        self.song_frame.configure(bg="white")

        header_frame_2 = tk.Frame(self.root, bg="#333333", height=150)
        header_frame_2.pack(fill="x")
        header_label_2 = tk.Label(header_frame_2, bg="#333333", fg="white")
        header_label_2.pack(pady=5)

        # Delete All Songs From DB
        delete_all_button = ttk.Button(
            header_frame_2, text=" Delete\n  All", command=self.delete_all, style="TButton", image=self.delete_icon, compound=LEFT)
        delete_all_button.pack(padx=200, pady=3, side=LEFT)

        # Exit
        exit_button = ttk.Button(
            header_frame_2, text=" Exit", command=self.confirm_exit, style="TButton", image=self.exit_icon, compound=LEFT)
        exit_button.pack(padx=200, pady=3, side=RIGHT)

        self.update_song_list()

    def delete_all(self):
        # Prompt the user for confirmation
        confirm_delete = messagebox.askyesno(
            "Delete Song", f"Are you sure you want to delete all songs'?")
        if confirm_delete:
            # Delete the song from the database
            conn = sqlite3.connect("sm_app.sqlite")
            conn.execute("DELETE FROM songs")
            conn.commit()
            conn.close()

            # Remove song from list
            for song in self.song_list:
                self.song_list.remove(song)

            # update  list
            self.update_song_list()
            messagebox.showinfo("information", "All Songs Deleted")

    def confirm_exit(self):
        result = messagebox.askquestion(
            "Exit", "Are you sure you want to exit?")
        if result == "yes":
            self.root.destroy()

    def confirm_exit_add(self):
        result = messagebox.askquestion(
            "Exit", "Are you sure you want to exit?")
        if result == "yes":
            self.song_window.destroy()

    def create_song(self):

        self.song_window = tk.Toplevel(self.root)
        self.song_window.title("Add Song")
        self.song_window.resizable(True, True)
        self.song_window.configure(bg="#333333")
        self.center_window(self.song_window)

        tk.Label(self.song_window, text="Song Name: ",
                 font=("Arial", 18, "bold"), bg="#333333", fg="white").pack(pady=5)
        self.song_name_entry = tk.Entry(
            self.song_window, font=("Arial", 14))
        self.song_name_entry.pack(pady=5)
        tk.Label(self.song_window, text="Song Arrangement: ",
                 font=("Arial", 18, "bold"), bg="#333333", fg="white").pack(pady=5)
        self.song_arrangement_entry = tk.Entry(
            self.song_window, font=("Arial", 14))
        self.song_arrangement_entry.pack(pady=5)

        tk.Label(self.song_window, text="Song BPM: ", font=(
            "Arial", 18, "bold"), bg="#333333", fg="white").pack(pady=5)
        self.bpm_combobox = ttk.Combobox(
            self.song_window, values=[i for i in range(40, 201)], state="readonly")
        self.bpm_combobox.pack(pady=5)

        self.metronome_button = ttk.Button(
            self.song_window, text="Use Metronome", command=self.show_metronome_window, style="TButton", image=self.metronome_icon, compound=tk.LEFT)
        self.metronome_button.pack(pady=10)

        tk.Label(self.song_window, text="Capo: ", font=(
            "Arial", 18, "bold"), bg="#333333", fg="white").pack(pady=5)
        self.capo_combobox = ttk.Combobox(
            self.song_window, values=["None"] + [str(i + 1) for i in range(8)], state="readonly")
        self.capo_combobox.pack()

        tk.Label(self.song_window, text="Number of Chords: ",
                 font=("Arial", 18, "bold"), bg="#333333", fg="white").pack(pady=5)
        self.song_chord_num_entry = ttk.Combobox(
            self.song_window, values=[i for i in range(1, 21)], state="readonly")
        self.song_chord_num_entry.pack(pady=5)
        tk.Label(self.song_window,
                 text="(After selecting the number of chords and clicking submit, you will be asked for input)", font=("Arial", 13), bg="#333333", fg="white").pack()

        submit_button = ttk.Button(
            self.song_window, text=" Submit", command=self.submit_chord_num, style="Green.TButton", image=self.submit_icon, compound=tk.LEFT)
        submit_button.pack(pady=10)

        exit_button = ttk.Button(
            self.song_window, text=" Exit", command=self.confirm_exit_add, style="TButton", image=self.exit_icon, compound=tk.LEFT)
        exit_button.pack(pady=10, side="bottom")

        save_button = ttk.Button(
            self.song_window, text=" Save", command=self.save_song, style="Green.TButton", image=self.save_icon, compound=tk.LEFT)
        save_button.pack(pady=10, side="bottom")

        self.song_lyrics_entry = tk.Text(
            self.song_window, wrap=tk.WORD, height=300, width=75)
        self.song_lyrics_entry.pack(pady=10, side="right", expand=True)

        self.song_notes_entry = tk.Text(
            self.song_window, wrap=tk.WORD, height=300, width=75)
        self.song_notes_entry.pack(pady=10, side="left", expand=True)

        tk.Label(self.song_window, text="Song Lyrics ——>",
                 font=("Arial", 18, "bold"), bg="#333333", fg="white").pack(side="right", padx=20, pady=5)
        tk.Label(self.song_window, text="<—— Notes",
                 font=("Arial", 18, "bold"), bg="#333333", fg="white").pack(side="left", padx=20, pady=5)

    # Allow user to play, pause, stop metronome

    def show_metronome_window(self):

        self.metronome_window = tk.Toplevel(self.root)
        self.metronome_window.title("Metronome")
        self.metronome_window.resizable(False, False)
        self.metronome_window.protocol(
            "WM_DELETE_WINDOW", self.close_metronome_window)
        self.metronome_window.configure(bg="#333333")
        window_height = 500
        window_width = 300
        screen_width = self.metronome_window.winfo_screenwidth()
        screen_height = self.metronome_window.winfo_screenheight()
        x_coordinate = int((screen_width/2) - (window_width/2))
        y_coordinate = int((screen_height/2) - (window_height/2))
        self.metronome_window.geometry(
            "{}x{}+{}+{}".format(window_width, window_height, x_coordinate, y_coordinate))

        self.play_button = ttk.Button(
            self.metronome_window, text="Play", command=self.start_metronome, style="TButton", image=self.play_icon, compound=tk.LEFT)
        self.play_button.pack(pady=50)
        self.pause_button = ttk.Button(
            self.metronome_window, text="Pause", command=self.pause_metronome, style="TButton", image=self.pause_icon, compound=tk.LEFT)
        self.pause_button.pack(pady=50)
        self.pause_button["state"] = "disabled"
        self.stop_button = ttk.Button(
            self.metronome_window, text="Stop", command=self.stop_metronome, style="TButton", image=self.stop_icon, compound=tk.LEFT)
        self.stop_button.pack(pady=50)
        self.stop_button["state"] = "disabled"

    def close_metronome_window(self):
        self.is_metronome_playing = False
        self.metronome_window.destroy()

    # Starts a different thread
    def start_metronome(self):
        if self.bpm_combobox.get():
            bpm = int(self.bpm_combobox.get())

            self.metronome_bpm = bpm
            self.play_button["state"] = "disabled"
            self.pause_button["state"] = "normal"
            self.stop_button["state"] = "normal"
            self.is_metronome_playing = True
            self.metronome_thread = threading.Thread(
                target=self.play_metronome)
            self.metronome_thread.start()
        else:
            messagebox.showinfo("Information", "Please select the BPM first")
            return

    def pause_metronome(self):
        self.play_button["state"] = "normal"
        self.pause_button["state"] = "disabled"
        self.stop_button["state"] = "normal"
        self.is_metronome_playing = False

    def stop_metronome(self):
        self.play_button["state"] = "normal"
        self.pause_button["state"] = "disabled"
        self.stop_button["state"] = "disabled"
        self.is_metronome_playing = False
        pygame.mixer.stop()
        self.metronome_window.destroy()

    def play_metronome(self):

        while self.is_metronome_playing:
            try:
                self.metronome_sound.play()
                beat_delay = 60000 / self.metronome_bpm  # Calculate delay in milliseconds
                pygame.time.delay(int(beat_delay))
            except pygame.error:
                print(
                    "Error: Metronome sound file not found or could not be loaded.")
                self.is_metronome_playing = False

        '''
        canvas.bind('<Configure>', lambda e: canvas.configure(
            scrollregion=canvas.bbox('all')))
        '''
    # Get chord input from user

    def submit_chord_num(self):

        num_chords_orig = self.song_chord_num_entry.get()

        if not num_chords_orig:
            messagebox.showinfo(
                "Information", "Please select the number of chords first")
            return

        self.chords_window = tk.Toplevel(self.root)
        self.chords_window.configure(bg="#333333")
        self.chords_window.title("Chords")
        self.chords_window.resizable(True, True)

        window_height = 500
        window_width = 300
        screen_width = self.chords_window.winfo_screenwidth()
        screen_height = self.chords_window.winfo_screenheight()
        x_coordinate = int((screen_width/2) - (window_width/2))
        y_coordinate = int((screen_height/2) - (window_height/2))
        self.chords_window.geometry(
            "{}x{}+{}+{}".format(window_width, window_height, x_coordinate, y_coordinate))

        # self.center_window(self.chords_window)

        canvas = tk.Canvas(self.chords_window, bg="#333333")
        canvas.pack(side='left', fill='both', expand=True)

        vscrollbar = tk.Scrollbar(
            self.chords_window, orient='vertical', command=canvas.yview)
        vscrollbar.pack(side='right', fill='y')
        hscrollbar = tk.Scrollbar(
            self.chords_window, orient='horizontal', command=canvas.xview)
        hscrollbar.pack(side='bottom', fill='x')
        canvas.configure(yscrollcommand=vscrollbar.set)
        canvas.configure(xscrollcommand=hscrollbar.set)

        chords_frame = tk.Frame(canvas, bg="#333333")
        canvas.create_window((0, 0), window=chords_frame,
                             anchor='n', tags='chords_frame')

        canvas.bind('<Configure>', lambda e: canvas.configure(
            scrollregion=canvas.bbox('all')))

        try:
            chord_num = int(num_chords_orig)
            if chord_num <= 0:
                messagebox.showinfo(
                    "Information", "Number of chords must be greater than 0.")
                return
        except ValueError:
            messagebox.showinfo(
                "Information", "Please enter a valid number of chords.")
            return

        self.chords_arr = []

        for i in range(chord_num):
            tk.Label(chords_frame, text="Enter Chord " + str(i+1) +
                     ": ", font=("Arial", 12, "bold"), bg="#333333", fg="white").pack(padx=60, pady=2.5)
            self.song_chord_entry = ttk.Combobox(
                chords_frame, values=[
                    "C", "C#", "D", "Eb", "E", "F", "F#",
                    "G", "Ab", "A", "Bb", "B", "Cm", "C#m",
                    "Dm", "Ebm", "Em", "Fm", "F#m", "Gm",
                    "Abm", "Am", "Bbm", "Bm",
                    "C7", "C#7", "D7", "Eb7", "E7", "F7", "F#7",
                    "G7", "Ab7", "A7", "Bb7", "B7", "Cm7", "C#m7",
                    "Dm7", "Ebm7", "Em7", "Fm7", "F#m7", "Gm7",
                    "Abm7", "Am7", "Bbm7", "Bm7"
                ], state="readonly")
            self.song_chord_entry.pack(padx=60, pady=5)
            self.chords_arr.append(self.song_chord_entry)

        submit_button = ttk.Button(
            chords_frame, text=" Submit", command=self.submit_callback, style="Blue.TButton", image=self.submit_icon, compound=LEFT)
        submit_button.pack(padx=60, pady=5)

    # save reult of chord input
    def submit_callback(self):

        if any(not entry.get() for entry in self.chords_arr):
            messagebox.showinfo("Information", "Please Enter All Chords.")
            return
        self.chords_arr_new = [entry.get()
                               for entry in self.chords_arr]  # Retrieve chords
        self.chords_window.destroy()
        messagebox.showinfo("information", "Chords Submitted")

    # save song in a dictionary
    def save_song(self):

        self.original_chords = self.chords_arr_new
        self.transposed_chords = []
        new_song = {
            "Name":   self.song_name_entry.get(),
            "Arrangement": self.song_arrangement_entry.get(),
            "BPM": self.bpm_combobox.get(),
            "Capo": self.capo_combobox.get(),
            "Chords": self.original_chords,
            "Transposed Chords": self.transposed_chords,
            "Lyrics": self.song_lyrics_entry.get(1.0, tk.END),
            "Notes": self.song_notes_entry.get(1.0, tk.END)

        }

        capo = self.capo_combobox.get()

        if capo != '' and capo != 'None':
            transposed_chords = [self.transpose_chord(
                chord, int(capo)) for chord in self.chords_arr_new]
            new_song["Chords"] = transposed_chords
            self.transposed_chords = transposed_chords  # Update the instance variable

        if (not self.song_name_entry.get()):
            messagebox.showinfo(
                "Information", "Please enter the name of the song.")
            return
        if (self.song_name_entry.get().isnumeric()):
            messagebox.showinfo(
                "Information", "Please enter a valid name.")
            return

        messagebox.showinfo("information", "Song Saved")

        # insert data in database

        def saveDB():

            conn = sqlite3.connect("sm_app.sqlite")
            entry_name = self.song_name_entry.get()
            entry_arrangement = self.song_arrangement_entry.get()
            entry_bpm = self.bpm_combobox.get()
            entry_capo = self.capo_combobox.get()
            # Store original chords as a space-separated string
            entry_chords = ' '.join(self.original_chords)
            # Store transposed chords as a space-separated string
            entry_transposed_chords = ' '.join(self.transposed_chords)
            entry_lyrics = self.song_lyrics_entry.get(1.0, tk.END)
            entry_notes = self.song_notes_entry.get(1.0, tk.END)

            if (len(entry_name) > 0):
                conn.execute('INSERT INTO songs (name, arrangement, bpm, capo, chords, transposed_chords, lyrics, notes) VALUES(?,?,?,?,?,?,?,?)', (
                    str(entry_name), str(entry_arrangement), str(entry_bpm), str(entry_capo), str(entry_chords), str(entry_transposed_chords), str(entry_lyrics), str(entry_notes)))
                conn.commit()

        saveDB()
        self.song_list.append(new_song)
        self.update_song_list()
        self.song_window.destroy()

    # map chords to their transposed selves (based on chord and capo fret number)

    def transpose_chord(self, chord, capo):

        chord_mappings = {
            # Major and Minor chords / Capo to and including the 8th fret
            "C": ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab"],
            "C#": ["C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A"],
            "D": ["D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb"],
            "Eb": ["Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"],
            "E": ["E", "F", "F#", "G", "Ab", "A", "Bb", "B", "C"],
            "F": ["F", "F#", "G", "Ab", "A", "Bb", "B", "C", "C#"],
            "F#": ["F#", "G", "Ab", "A", "Bb", "B", "C", "C#", "D"],
            "G": ["G", "Ab", "A", "Bb", "B", "C", "C#", "D", "Eb"],
            "Ab": ["Ab", "A", "Bb", "B", "C", "C#", "D", "Eb"],
            "A": ["A", "Bb", "B", "C", "C#", "D", "Eb", "E", "F"],
            "Bb": ["Bb", "B", "C", "C#", "D", "Eb", "E", "F", "F#"],
            "B": ["B", "C", "C#", "D", "Eb", "E", "F", "F#", "G"],
            "Cm": ["Cm", "C#m", "Dm", "Ebm", "Em", "Fm", "F#m", "Gm", "Abm"],
            "C#m": ["C#m", "Dm", "Ebm", "Em", "Fm", "F#m", "Gm", "Abm", "Am"],
            "Dm": ["Dm", "Ebm", "Em", "Fm", "F#m", "Gm", "Abm", "Am", "Bbm"],
            "Ebm": ["Ebm", "Em", "Fm", "F#m", "Gm", "Abm", "Am", "Bbm", "Bm"],
            "Em": ["Em", "Fm", "F#m", "Gm", "Abm", "Am", "Bbm", "Bm", "Cm"],
            "Fm": ["Fm", "F#m", "Gm", "Abm", "Am", "Bbm", "Bm", "Cm", "C#m"],
            "Gm": ["Gm", "Abm", "Am", "Bbm", "Bm", "Cm", "C#m", "Dm", "Ebm"],
            "Bbm": ["Bbm", "Bm", "Cm", "C#m", "Dm", "Ebm", "Em", "Fm", "F#m"],
            "F#m": ["F#m", "Gm", "Abm", "Am", "Bbm", "Bm", "Cm", "C#m", "Dm"],
            "Am": ["Am", "Bbm", "Bm", "Cm", "C#m", "Dm", "Ebm", "Em", "Fm"],
            "Abm": ["Abm", "Am", "Bbm", "Bm", "Cm", "C#m", "Dm", "Ebm"],
            "Bm": ["Bm", "Cm", "C#m", "Dm", "Ebm", "Em", "Fm", "F#m", "Gm"],
            # 7ths and minor 7ths to and including the 8th fret
            "C7": ["C7", "C#7", "D7", "Eb7", "E7", "F7", "F#7", "G7", "Ab7"],
            "C#7": ["C#7", "D7", "Eb7", "E7", "F7", "F#7", "G7", "Ab7", "A7"],
            "D7": ["D7", "Eb7", "E7", "F7", "F#7", "G7", "Ab7", "A7", "Bb7"],
            "Eb7": ["Eb7", "E7", "F7", "F#7", "G7", "Ab7", "A7", "Bb7", "B7"],
            "E7": ["E7", "F7", "F#7", "G7", "Ab7", "A7", "Bb7", "B7", "C7"],
            "F7": ["F7", "F#7", "G7", "A7", "Ab7", "Bb7", "B7", "C7", "C#7"],
            "F#7": ["F#7", "G7", "Ab7", "A7", "Bb7", "B7", "C7", "C#7", "D7"],
            "G7": ["G7", "Ab7", "A7", "Bb7", "B7", "C7", "C#7", "D7", "Eb7"],
            "Ab7": ["Ab7", "A7", "Bb7", "B7", "C7", "C#7", "D7", "Eb7"],
            "A7": ["A7", "Bb7", "B7", "C7", "C#7", "D7", "Eb7", "E7", "F7"],
            "Bb7": ["Bb7", "B7", "C7", "C#7", "D7", "Eb7", "E7", "F7", "F#7"],
            "B7": ["B7", "C7", "C#7", "D7", "Eb7", "E7", "F7", "F#7", "G7"],
            "Cm7": ["Cm7", "C#m7", "Dm7", "Ebm7", "Em7", "Fm7", "F#m7", "Gm7", "Abm7"],
            "C#m7": ["C#m7", "Dm7", "Ebm7", "Em7", "Fm7", "F#m7", "Gm7", "Abm7", "Am7"],
            "Dm7": ["Dm7", "Ebm7", "Em7", "Fm7", "F#m7", "Gm7", "Abm7", "Am7", "Bbm7"],
            "Ebm7": ["Ebm7", "Em7", "Fm7", "F#m7", "Gm7", "Abm7", "Am7", "Bbm7", "Bm7"],
            "Em7": ["Em7", "Fm7", "F#m7", "Gm7", "Abm7", "Am7", "Bbm", "Bm7", "Cm7"],
            "Fm7": ["Fm7", "F#m7", "Gm7", "Abm7", "Am7", "Bbm7", "Bm7", "Cm7", "C#m7"],
            "Gm7": ["Gm7", "Abm7", "Am7", "Bbm7", "Bm7", "Cm7", "C#m7", "Dm7", "Ebm7"],
            "Bbm7": ["Bbm7", "Bm7", "Cm7", "C#m7", "Dm7", "Ebm7", "Em7", "Fm7", "F#m7"],
            "F#m7": ["F#m7", "Gm7", "Abm7", "Am7", "Bbm", "Bm7", "Cm7", "C#m7", "Dm7"],
            "Am7": ["Am7", "Bbm7", "Bm7", "Cm7", "C#m7", "Dm7", "Ebm7", "Em7", "Fm7"],
            "Abm7": ["Abm7", "Am7", "Bbm7", "Bm7", "Cm7", "C#m7", "Dm7", "Ebm7"],
            "Bm7": ["Bm7", "Cm7", "C#m7", "Dm7", "Ebm7", "Em7", "Fm7", "F#m7", "Gm7"],
        }
        # handle case where chord input is not in the list or no capo is used
        if chord not in chord_mappings or capo == "None":
            return chord

        # get the index of the input chord
        chord_index = chord_mappings[chord].index(chord)
        capo = int(capo)
       # get the index of the transposed chord
        transposed_index = (chord_index + capo) % len(chord_mappings[chord])

        # return transposed chord
        return chord_mappings[chord][transposed_index]

    def update_song_list(self):

        for widget in self.song_frame.winfo_children():
            widget.destroy()

        canvas = tk.Canvas(self.song_frame, width=1000, height=550)
        canvas.pack(side="left", fill='both', expand=True)
        vscrollbar = tk.Scrollbar(
            self.song_frame, orient='vertical', command=canvas.yview)
        vscrollbar.pack(side='right', fill='y')
        hscrollbar = tk.Scrollbar(
            self.song_frame, orient='horizontal', command=canvas.xview)
        hscrollbar.pack(side='bottom', fill='x')
        canvas.configure(yscrollcommand=vscrollbar.set)
        canvas.configure(xscrollcommand=hscrollbar.set)
        ui_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=ui_frame,
                             anchor='nw', tags='ui_frame')
        canvas.bind('<Configure>', lambda e: canvas.configure(
            scrollregion=canvas.bbox('all')))

        conn = sqlite3.connect("sm_app.sqlite")
        curr = conn.execute("SELECT * FROM songs ORDER BY name")

        for c in curr:
            song_label = tk.Label(ui_frame, text=str(
                c[1]), width=15)
            song_label.config(
                font=("Sans Serif", 50, "bold"))
            song_label.pack(pady=2, anchor="center")
            song_label.bind("<Button-1>", lambda event, song=str(c[1]), arrangement=str(c[2]), bpm=str(c[3]), capo=str(c[4]), chords=str(
                c[5]), transposed_chords=str(c[6]), lyrics=str(c[7]), notes=str(c[8]): self.show_song_details(song, arrangement, bpm, capo, chords, transposed_chords, lyrics, notes), song_label.config(relief="raised", anchor="center"))
            edit_button = ttk.Button(ui_frame, text=" Edit", image=self.edit_icon, compound=LEFT, style="Yellow.TButton", command=lambda song=c[1], arrangement=c[2], bpm=c[3], capo=c[4], chords=c[5], transposed_chords=c[6], lyrics=c[7], notes=c[8]: self.edit_song(
                song, arrangement, bpm, capo, chords, transposed_chords, lyrics, notes))  # Pass original chords
            edit_button.pack(pady=5)
            delete_button = ttk.Button(
                ui_frame, text=" Delete", style="Red.TButton", image=self.delete_icon, compound=LEFT, command=lambda name=c[1]: self.delete_song(name))
            delete_button.pack(pady=5)

    def delete_song(self, song_name):

        # confirm that user wants to delete song
        confirm_delete = messagebox.askyesno(
            "Delete Song", f"Do you want to delete the song '{song_name}'?")
        if confirm_delete:
            # Delete song from db
            conn = sqlite3.connect("sm_app.sqlite")
            conn.execute("DELETE FROM songs WHERE name=?", (song_name,))
            conn.commit()
            conn.close()

            # remove song from list
            for song in self.song_list:
                if song["Name"] == song_name:
                    self.song_list.remove(song)
                    break

            # update list
            self.update_song_list()
            messagebox.showinfo("information", "Song Deleted")

    def confirm_exit_edit(self):
        result = messagebox.askquestion(
            "Exit", "Are you sure you want to exit?")
        if result == "yes":
            self.edit_window.destroy()

    # edit song details
    def edit_song(self, song, arrangement, bpm, capo, chords, transposed_chords, lyrics, notes):

        # Allow user to play, pause, stop metronome
        def show_metronome_window_2():

            self.metronome_window = tk.Toplevel(self.root)
            self.metronome_window.title("Metronome")
            self.metronome_window.resizable(False, False)
            self.metronome_window.configure(bg="#333333")
            window_height = 500
            window_width = 300
            screen_width = self.metronome_window.winfo_screenwidth()
            screen_height = self.metronome_window.winfo_screenheight()
            x_coordinate = int((screen_width/2) - (window_width/2))
            y_coordinate = int((screen_height/2) - (window_height/2))
            self.metronome_window.geometry(
                "{}x{}+{}+{}".format(window_width, window_height, x_coordinate, y_coordinate))
            # self.center_window(self.metronome_window)

            self.play_button = ttk.Button(
                self.metronome_window, text="Play", command=self.start_metronome, style="TButton", image=self.play_icon, compound=tk.LEFT)
            self.play_button.pack(pady=50)
            self.pause_button = ttk.Button(
                self.metronome_window, text="Pause", command=self.pause_metronome, style="TButton", image=self.pause_icon, compound=tk.LEFT)
            self.pause_button.pack(pady=50)
            self.pause_button["state"] = "disabled"
            self.stop_button = ttk.Button(
                self.metronome_window, text="Stop", command=self.stop_metronome, style="TButton", image=self.stop_icon, compound=tk.LEFT)
            self.stop_button.pack(pady=50)
            self.stop_button["state"] = "disabled"

        # Starts a different thread
        def start_metronome():
            if self.bpm_combobox.get():
                bpm = int(self.bpm_combobox.get())
                self.metronome_bpm = bpm
                self.play_button["state"] = "disabled"
                self.pause_button["state"] = "normal"
                self.stop_button["state"] = "normal"
                self.is_metronome_playing = True
                self.metronome_thread = threading.Thread(
                    target=self.play_metronome)
                self.metronome_thread.start()
            else:
                messagebox.showinfo(
                    "Information", "Please select the BPM first")
                return

        def pause_metronome():
            self.play_button["state"] = "normal"
            self.pause_button["state"] = "disabled"
            self.stop_button["state"] = "normal"
            self.is_metronome_playing = False

        def stop_metronome():
            self.play_button["state"] = "normal"
            self.pause_button["state"] = "disabled"
            self.stop_button["state"] = "disabled"
            self.is_metronome_playing = False
            pygame.mixer.stop()
            self.metronome_window.destroy()

        def play_metronome():

            while self.is_metronome_playing:
                try:
                    self.metronome_sound.play()
                    beat_delay = 60000 / self.metronome_bpm  # Calculate delay in milliseconds
                    pygame.time.delay(int(beat_delay))
                except pygame.error:
                    print(
                        "Error: Metronome sound file not found or could not be loaded.")
                    self.is_metronome_playing = False

        self.edit_window = tk.Toplevel(self.root)
        self.edit_window.title("Edit Song")
        self.edit_window.resizable(True, True)
        self.edit_window.configure(bg="#333333")
        #  window geometry

        self.center_window(self.edit_window)

        # Create and populate fields for editing song details
        tk.Label(self.edit_window, text="Song Name: ",
                 font=("Arial", 14, "bold"), bg="#333333", fg="white").pack()
        song_name_entry = ttk.Entry(self.edit_window)
        song_name_entry.insert(0, song)
        song_name_entry.pack(pady=5)
        tk.Label(self.edit_window, text="Song Arrangement: ",
                 font=("Arial", 14, "bold"), bg="#333333", fg="white").pack()
        song_arrangement_entry = ttk.Entry(self.edit_window)
        song_arrangement_entry.insert(0, arrangement)
        song_arrangement_entry.pack(pady=5)
        tk.Label(self.edit_window, text="Song BPM: ",
                 font=("Arial", 14, "bold"), bg="#333333", fg="white").pack()
        self.bpm_combobox = ttk.Combobox(
            self.edit_window, values=[str(i) for i in range(40, 201)], state="readonly")
        self.bpm_combobox.set(bpm)
        self.bpm_combobox.pack(pady=5)

        metronome_button_2 = ttk.Button(
            self.edit_window, text="Use Metronome", command=show_metronome_window_2, style="TButton", image=self.metronome_icon, compound=tk.LEFT)
        metronome_button_2.pack(pady=5)

        capo_label = tk.Label(
            self.edit_window, text="Select Capo:", font=("Arial", 14, "bold"), bg="#333333", fg="white")
        capo_label.pack()
        capo_combobox = ttk.Combobox(self.edit_window, values=[
            "None"] + [str(i) for i in range(1, 9)], state="readonly")

        if capo:
            capo_combobox.set(capo)
        else:
            capo_combobox.set("None")
        capo_combobox.pack(pady=5)

        def update_song_details():
            new_name = song_name_entry.get()
            new_arrangement = song_arrangement_entry.get()
            new_bpm = self.bpm_combobox.get()
            new_capo = capo_combobox.get()

            if (not new_name):
                messagebox.showinfo(
                    "Information", "Please enter the name of the song.")
                return
            if (new_name.isnumeric()):
                messagebox.showinfo(
                    "Information", "Please enter a valid name.")
                return

            # Convert chords to lists
            new_chords = self.song_chords_entry.get().split()
            new_transposed_chords = [
                self.transpose_chord(i, new_capo) for i in new_chords]
            new_lyrics = self.song_lyrics_entry.get("1.0", tk.END)
            new_notes = self.song_notes_entry.get("1.0", tk.END)
            new_chords = [chord.strip() for chord in new_chords]
            new_transposed_chords = [chord.strip()
                                     for chord in new_transposed_chords]

            chord_error = False

            for c in new_transposed_chords:
                if not (c in ["C", "C#", "D", "Eb", "E", "F", "F#",
                              "G", "Ab", "A", "Bb", "B", "Cm", "C#m",
                              "Dm", "Ebm", "Em", "Fm", "F#m", "Gm",
                              "Abm", "Am", "Bbm", "Bm",
                              "C7", "C#7", "D7", "Eb7", "E7", "F7", "F#7",
                              "G7", "Ab7", "A7", "Bb7", "B7", "Cm7", "C#m7",
                              "Dm7", "Ebm7", "Em7", "Fm7", "F#m7", "Gm7",
                              "Abm7", "Am7", "Bbm7", "Bm7"]):
                    chord_error = True

            if chord_error:
                messagebox.showinfo(
                    "Information", "Please enter valid chords")
                return

            # update the song details in the database with both original and transposed chords
            # conn = sqlite3.connect("sm_app.sqlite")
            db_path = os.path.abspath(os.path.join(
                os.path.dirname(__file__), "sm_app.sqlite"))
            conn = sqlite3.connect(db_path)
            conn.execute(
                'UPDATE songs SET name=?, arrangement=?, bpm=?, capo=?, chords=?, transposed_chords=?, lyrics=?, notes=? WHERE name=?',
                (new_name, new_arrangement, new_bpm, new_capo, ' '.join(
                    new_chords), ' '.join(new_transposed_chords), new_lyrics, new_notes, song)
            )
            conn.commit()
            conn.close()

            # close edit window
            self.edit_window.destroy()
            # update the list
            self.update_song_list()
            messagebox.showinfo("Information", "Changes Saved")

        # get chords from input
        tk.Label(self.edit_window, text="Original Chords (space-separated):",
                 font=("Arial", 14, "bold"), bg="#333333", fg="white").pack(pady=5)
        chord_s = "C, C#, D, Eb, E, F, F#,\nG, Ab, A, Bb, B, Cm, \nC#m,Dm, Ebm, Em, Fm, F#m, \nGm, Abm, Am, Bbm, Bm, C7, \nC#7, D7, Eb7, E7, F7, F#7, \nG7, Ab7, A7, Bb7, B7, Cm7, \nC#m7,Dm7, Ebm7, Em7, Fm7, F#m7, Gm7,\nAbm7, Am7, Bbm7, Bm7"

        tk.Label(self.edit_window, text=f"Chord options are: \n————————\n {chord_s}\n————————", font=(
            "times", 12, "italic"), bg="#333333", fg="light yellow").pack(pady=5)
        self.song_chords_entry = ttk.Entry(self.edit_window)
        self.song_chords_entry.insert(0, ''.join(chords))
        self.song_chords_entry.pack(pady=10)

        # save Changes
        save_changes_button = ttk.Button(
            self.edit_window, text=" Save Changes", style="Green.TButton", command=update_song_details, image=self.save_icon, compound=LEFT)
        save_changes_button.pack(pady=10)

        exit_button = ttk.Button(
            self.edit_window, text=" Exit", command=self.confirm_exit_edit, style="TButton", image=self.exit_icon, compound=tk.LEFT)
        exit_button.pack(pady=10)

        self.song_lyrics_entry = tk.Text(
            self.edit_window, height=25, width=50, wrap=WORD, font=("Arial", 12, "italic"))
        self.song_lyrics_entry.insert("1.0", lyrics)
        self.song_lyrics_entry.pack(pady=5, side="right", expand=True)
        self.song_notes_entry = tk.Text(
            self.edit_window, height=25, width=50, wrap=WORD, font=("Arial", 12, "italic"))
        self.song_notes_entry.insert(
            "1.0", notes)
        self.song_notes_entry.pack(pady=5, side="left", expand=True)
        tk.Label(self.edit_window, text="Song Lyrics ——>",
                 font=("Arial", 16, "bold"), bg="#333333", fg="white").pack(side="right", pady=5, padx=10)
        tk.Label(self.edit_window, text="<—— Notes",
                 font=("Arial", 16, "bold"), bg="#333333", fg="white").pack(side="left", pady=5, padx=10)

        self.edit_window.mainloop()

    def exit_details(self):
        self.details_window.destroy()

    def show_song_details(self, song, arrangement, bpm, capo, chords, transposed_chords, lyrics, notes):

        self.retrieveDB()
        self.details_window = tk.Toplevel(self.root)
        self.details_window.title("Song Details")
        self.details_window.resizable(False, False)
        self.details_window.configure(bg="#333333")

        self.center_window(self.details_window)
        # alt bg -> bg="#0078D4"
        header_frame = tk.Frame(
            self.details_window, bg="#333333", height=100)
        header_frame.pack(fill="x")

        tk.Label(self.details_window, text=f"Name: {song}", font=(
            "arial", 32, "bold"), bg="#333333", fg="white").pack(pady=20)
        tk.Label(self.details_window, text=f"Arrangement: [{arrangement}]", font=(
            "Times", 28, "bold"), bg="#333333", fg="white").pack(pady=20, padx=10)
        tk.Label(self.details_window, text=f"BPM: {bpm}", font=(
            "Times", 28, "bold"), bg="#333333", fg="white").pack(pady=20)
        tk.Label(self.details_window, text=f"Capo: {capo}", font=(
            "Times", 28, "bold"), bg="#333333", fg="white").pack(pady=20)

        if capo and capo != "None":

            chords = ' '.join(chord.strip() for chord in chords.split())
            transposed_chords = ' '.join(
                chord.strip() for chord in transposed_chords.split())
            tk.Label(self.details_window, text=f"Original Chords: {chords}", font=(
                "Times", 32, "bold"), bg="#333333", fg="white").pack(pady=20)
            tk.Label(self.details_window, text=f"New Chords: {transposed_chords}", font=(
                "Times", 32, "bold"), bg="#333333", fg="white").pack(pady=20)

        else:
            tk.Label(self.details_window, text=f"Chords: {chords}", font=(
                "Times", 32, "bold"), bg="#333333", fg="white").pack(pady=20)

        show_lyrics_button = ttk.Button(self.details_window, text="Show Lyrics", style="Blue.TButton", command=lambda: [
            self.show_lyrics(lyrics)])  # Pass the lyrics to the show_lyrics method
        show_lyrics_button.pack(pady=10)
        show_notes_button = ttk.Button(self.details_window, text="Show Notes", style="Blue.TButton", command=lambda: [
            self.show_notes(notes)])
        show_notes_button.pack(pady=10)

        exit_button = ttk.Button(
            self.details_window, text=" Exit", command=self.exit_details, style="TButton", image=self.exit_icon, compound=tk.LEFT)
        exit_button.pack(pady=20)

    def show_lyrics(self, lyrics):

        self.lyrics_window = tk.Toplevel(self.root)
        self.lyrics_window.title("Lyrics")
        self.lyrics_window.resizable(False, False)

        self.center_window(self.lyrics_window)

        ''' in case I want to use a canvas and frame here later
        canvas = tk.Canvas(self.lyrics_window)
        canvas.pack(side='left', fill='both', expand=True)
        vscrollbar = tk.Scrollbar(
            self.lyrics_window, orient='vertical', command=canvas.yview)
        vscrollbar.pack(side='right', fill='y')
        canvas.configure(yscrollcommand=vscrollbar.set)
        lyrics_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=lyrics_frame,
                             anchor='nw', tags='lyrics_frame')
        '''

        lyrics_text = tk.Text(self.lyrics_window, wrap=tk.WORD)
        lyrics_text.pack(pady=10, fill='both', expand=True)
        lyrics_text.insert(tk.END, lyrics)
        lyrics_text.config(state=tk.DISABLED)
        self.lyrics_window.mainloop()

        '''
        canvas.bind('<Configure>', lambda e: canvas.configure(
            scrollregion=canvas.bbox('all')))
        '''

    def show_notes(self, notes):

        self.notes_window = tk.Toplevel(self.root)
        self.notes_window.title("Notes")
        self.notes_window.resizable(False, False)

        self.center_window(self.self.notes_window)

        ''' in case I want to use a canvas and frame here later
        canvas = tk.Canvas(self.notes_window)
        canvas.pack(side='left', fill='both', expand=True)
        vscrollbar = tk.Scrollbar(
            self.notes_window, orient='vertical', command=canvas.yview)
        vscrollbar.pack(side='right', fill='y')
        canvas.configure(yscrollcommand=vscrollbar.set)
        notes_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=notes_frame,
                             anchor='nw', tags='notes_frame')
        '''

        notes_text = tk.Text(self.notes_window, wrap=tk.WORD)
        notes_text.pack(pady=10, fill='both', expand=True)
        notes_text.insert(tk.END, notes)
        notes_text.config(state=tk.DISABLED)  # Disable editing

        '''
        canvas.bind('<Configure>', lambda e: canvas.configure(
            scrollregion=canvas.bbox('all')))
        self.notes_window.mainloop()
        '''


if __name__ == "__main__":

    root = tk.Tk()

    # button styles
    ttk.Style().configure("Blue.TButton", foreground="#0078D4",
                          background="#0078D4", font=("Arial", 12, "bold"), borderwidth=0,  padding=10)
    ttk.Style().configure("Green.TButton", foreground="#4CAF50",
                          background="#4CAF50", font=("Arial", 12, "bold"), borderwidth=0,  padding=10)
    ttk.Style().configure("Yellow.TButton", foreground="#FFC107",
                          background="#FFC107", font=("Arial", 12, "bold"), borderwidth=0,  padding=10)
    ttk.Style().configure("Red.TButton", foreground="#FF5722",
                          background="#FF5722", font=("Arial", 12, "bold"), borderwidth=0,  padding=10)
    ttk.Style().configure("Regular.TButton", foreground="black",
                          background="white", font=("Arial", 12, "bold"), borderwidth=0,  padding=10)

    app_icon = tk.PhotoImage(file="images/SongManager_Logo_2.png")
    root.iconphoto(True, app_icon)
    app = SongCreatorApp(root)
    root.mainloop()
