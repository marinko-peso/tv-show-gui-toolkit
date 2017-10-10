# -*- coding: utf-8 -*-
from Tkinter import Tk, Label, Button, END, Frame
from Tkinter import W, E, N, S
from Tkinter import Text, Scrollbar
from Tkinter import StringVar
from tkFileDialog import askopenfilename, askdirectory

from modules.file_rename import FileRename
from modules.char_replace import CharReplace


class ShowToolkitGui:

    # Initial data used.
    directory_path = None
    file_path = None
    DIRECTORY = 'directory'
    FILE = 'file'
    last_selected = None

    # Initialize module classes.
    file_rename = FileRename()
    char_replace = CharReplace()

    def __init__(self, master):
        self.master = master
        self.master.title('TV Show Files Tookit')

        # Create app layout.
        self.create_custom_layout()
        self.create_top_controls()
        self.create_status_controls()

    def create_custom_layout(self):
        """
        Parent layout, divide the app into blocks for easier handling.
        """
        # Main container for the whole app.
        self.main_container = Frame(self.master)
        self.main_container.pack(side='top', fill='both', expand=True)

        # Container for the top part of the app.
        self.top_frame = Frame(self.main_container)
        self.top_frame.pack(side='top', fill='x', expand=False)
        # Container for the bottom part of the app.
        self.bottom_frame = Frame(self.main_container)
        self.bottom_frame.pack(side='bottom', fill='both', expand=True)

        # Top container of the top container.
        self.top_top_frame = Frame(self.top_frame)
        self.top_top_frame.pack(side='top', fill='x', expand=False, padx=5, pady=5)
        # Bottom container of the top container.
        self.top_bottom_frame = Frame(self.top_frame)
        self.top_bottom_frame.pack(side='bottom', fill='x', expand=False)

        # Additional layers, divide top frame of top frame into left and right.
        self.top_top_left_frame = Frame(self.top_top_frame, relief='groove', borderwidth=2)
        self.top_top_left_frame.pack(side='left', fill='x', expand=False, padx=5, pady=5)
        self.top_top_right_frame = Frame(self.top_top_frame, relief='groove', borderwidth=2)
        self.top_top_right_frame.pack(side='right', fill='x', expand=False, padx=5, pady=5)

    def create_top_controls(self):
        """
        Top layout, controls for the app.
        """
        # Button for selecting directory.
        self.select_directory_button = Button(self.top_top_left_frame, text='Select Directory', command=self.select_directory)
        self.select_directory_button.grid(row=0, column=0, sticky=W+E, padx=7, pady=2)

        # Button for selecting file.
        self.select_file_button = Button(self.top_top_left_frame, text='Select File', command=self.select_file)
        self.select_file_button.grid(row=1, column=0, sticky=W+E, padx=7, pady=2)

        # Button to run the Rename operation.
        self.rename_button = Button(self.top_top_right_frame, text='Rename to S**E**', command=self.process_rename)
        self.rename_button.grid(row=0, column=0, sticky=W+E, padx=7, pady=2)

        # Button to run the Character Replace operation.
        self.char_button = Button(self.top_top_right_frame, text='Character Replace', command=self.process_character_replace)
        self.char_button.grid(row=1, column=0, sticky=W+E, padx=7, pady=2)

    def create_status_controls(self):
        """
        Bottom layout, text status controls for letting the user know what the current state is.
        """
        # Status text for currently selected directory or file.
        self.status_text = StringVar()
        self.status_label = Label(self.top_bottom_frame, textvariable=self.status_text)
        self.status_text.set('Use controls above to select a source to be modified')
        self.status_label.grid(row=0, column=0)

        # Progress text controls, outputs full logs from libs.
        self.progress_text = Text(self.bottom_frame, height=8, width=60)
        # Add visible scrollbar.
        self.scrollbar = Scrollbar(self.bottom_frame, command=self.progress_text.yview)
        self.progress_text.configure(yscrollcommand=self.scrollbar.set)
        # Define custom tags for text format.
        self.progress_text.tag_config('bold', background='black', foreground='green', font=('Arial', 12, 'bold'))
        self.progress_text.tag_config('big', background='black', foreground='green', font=('Arial', 20, 'bold'))
        self.progress_text.tag_config('default', foreground='red', font=('Courier', 11))
        # Set initial empty text and position.
        self.update_progress_text('')
        self.progress_text.grid(row=0, column=0, sticky='nsew')
        # Add North and South to the scrollbar so it streches in vertical direction.
        self.scrollbar.grid(column=1, row=0, sticky=N+S+W)

    def select_directory(self):
        """
        Get the selected directory path.
        """
        # Open directory selector.
        self.directory_path = askdirectory()
        # If user selected a directory, mark it.
        if self.directory_path:
            self.last_selected = self.DIRECTORY
            self.status_text.set(self.directory_path)

    def select_file(self):
        """
        Get the selected file path.
        """
        # Open file selector, only some file types are supported.
        self.file_path = askopenfilename(filetypes=(
            ('SRT Files', '*.srt'), 
            ('SUB Files', '*.sub'), 
            ('TXT Files', '*.txt'), 
            ('AVI Files', '*.avi'), 
            ('MP4 Files', '*.mp4'), 
            ('MKV Files', '*.mkv')
        ))
        # If user selected a file, mark it.
        if self.file_path:
            self.last_selected = self.FILE
            self.status_text.set(self.file_path)

    def process_rename(self):
        """
        Call the rename operation on directory or file selected.
        """
        if not self.last_selected:
            return

        if self.last_selected == self.DIRECTORY:
            progress_message = self.file_rename.process_directory(self.directory_path)
        elif self.last_selected == self.FILE:
            progress_message = self.file_rename.rename_file(self.file_path)
        self.update_progress_text(progress_message)

    def process_character_replace(self):
        """
        Call the char replace operation on directory or file selected.
        """
        if not self.last_selected:
            return

        if self.last_selected == self.DIRECTORY:
            progress_message = self.char_replace.process_directory(self.directory_path)
        elif self.last_selected == self.FILE:
            progress_message = self.char_replace.process_file(self.file_path)
        self.update_progress_text(progress_message)

    def update_progress_text(self, new_text):
        """
        Update the progress text from the rename or character replace operations.
        """
        # If list is sent convert it to string.
        if type(new_text) is list:
            new_text = '\n'.join(new_text)
        # Enable the changes on text, clear it, send new content, and then disable editing.
        self.progress_text.config(state='normal')
        self.progress_text.delete(1.0, END)
        self.progress_text.insert(END, new_text, ('default'))
        self.progress_text.config(state='disabled')


root = Tk()
# Disable resizing.
root.resizable(0, 0)
my_gui = ShowToolkitGui(root)
# Run app.
root.mainloop()
