from tkinter import *
from tkinter import filedialog
from tkinter import messagebox


def intro_screen(parent_frame):
    intro_frame = Frame(frame, bg="yellow", width=700, height=400)
    intro_frame.pack_propagate(False)
    intro_frame.place(x=0, y=0)

    text = Label(intro_frame, text="TEXT EDITOR!""\n""DEVELOPED BY SUMIT SONAR", font=(
        "TKDefaultFont", 12, "bold"), fg="black", bg="yellow")
    text.pack(anchor=CENTER, pady=135)

    parent_frame.after(3000, intro_frame.destroy)


def open_new_empty_file():
    main_screen()


file_path = None


def open_exist_file():
    global file_path
    file_path = filedialog.askopenfilename(
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        with open(file_path, "r") as file:
            content = file.read()
            entry.delete("1.0", END)
            entry.insert("1.0", content)


def save_as_file():
    global file_path
    current_file = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[
                                                ("Text files", "*.txt"), ("All files", "*.*")])
    if current_file:
        with open(current_file, "w") as file:
            content = entry.get("1.0", END)
            file.write(content)


def save_current_file():
    global file_path
    # current_file = filedialog.ask(defaultextension=".txt",filetypes=[("Text files","*.txt"),("All files","*.*")])
    if file_path:
        with open(file_path, "w") as file:
            content = entry.get("1.0", END)
            file.write(content)
    else:
        save_as_file()


def without_saving_file_exit():
    global file_path

    # Check if the Text widget has any content or if it has been modified
    def without_saving_file_exit():
        global file_path

    if not entry.get("1.0", "end-1c").strip():  # Check if the Text widget is empty
        frame.destroy()
    else:
        if entry.edit_modified():  # Check if the Text widget has been modified (text has been written)
            response = messagebox.askyesnocancel(
                "Unsaved changes", "Do you want to save the changes before exiting?")
            if response is None:
                return
            elif response:
                save_as_file()
        frame.destroy()


def cut_text():
    if entry.tag_ranges("sel"):
        content = entry.get("sel.first", "sel.last")
        entry.delete("sel.first", "sel.last")
        # it copies the selected text to the clipboard using frame.clipboard_clear()
        frame.clipboard_clear()
        # making it available for pasting in other applications.
        frame.clipboard_append(content)


def copy_text():
    if entry.tag_ranges("sel"):
        content = entry.get("sel.first", "sel.last")
        frame.clipboard_clear()
        frame.clipboard_append(content)


def paste_text():
    # clipboard is a temporary storage area used for copying and pasting data.
    content = frame.clipboard_get()
    if content:  # checks if there is any content retrieved from the clipboard.
        entry.insert("insert", content)


def select_all_text():
    entry.tag_add("sel", "0.1", "end")


def make_text_bold():
    start_index = entry.index("sel.first")
    end_index = entry.index("sel.last")
    # Remove the "italic" tag if present
    entry.tag_remove("italic", start_index, end_index)
    entry.tag_add("bold", start_index, end_index)
    entry.tag_config("bold", font=("TkDefaultFont", 12, "bold"))


def make_text_italic():
    start_index = entry.index("sel.first")
    last_index = entry.index("sel.last")
    # Remove the "bold" tag if present
    entry.tag_remove("bold", start_index, last_index)
    entry.tag_add("italic", start_index, last_index)
    entry.tag_config("italic", font=("TkDefaultFont", 12, "italic"))


def make_text_standard():
    first_index = entry.index("sel.first")
    last_index = entry.index("sel.last")
    entry.tag_remove("bold", first_index, last_index)
    entry.tag_remove("italic", first_index, last_index)


def main_screen():

    global frame, entry

    frame = Tk()
    frame.geometry("700x400")
    frame.title("Text Editor")

    main_frame = Frame(frame)
    main_frame.pack(fill=BOTH, expand=TRUE)
    menubar = Menu(frame)

    file_menu = Menu(menubar, tearoff=0)
    file_menu.add_command(label="New file", command=open_new_empty_file)
    file_menu.add_command(label="Open file", command=open_exist_file)
    file_menu.add_command(label="Save as", command=save_as_file)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=without_saving_file_exit)

    menubar.add_cascade(label="File", menu=file_menu)

    edit_menu = Menu(menubar, tearoff=0)
    edit_menu.add_command(label="cut", command=cut_text)
    edit_menu.add_command(label="copy", command=copy_text)
    edit_menu.add_command(label="paste", command=paste_text)
    edit_menu.add_command(label="select all", command=select_all_text)

    menubar.add_cascade(label="Edit", menu=edit_menu)

    frame.config(menu=menubar)

    left_frame = Frame(main_frame, width=150, height=400, bg="grey")
    left_frame.pack(side=LEFT, fill=BOTH)

    bold_botton = Button(left_frame, text="BOLD", command=make_text_bold,
                         width=10, height=1, font=("TkDefaultFont", 9, "bold")).place(x=35, y=10)
    italic_botton = Button(left_frame, text="Italic", command=make_text_italic,
                           width=10, height=1, font=("TkDefaultFont", 9, "italic")).place(x=35, y=50)
    standard_botton = Button(left_frame, text="Standard",
                             command=make_text_standard, width=10, height=1).place(x=35, y=90)
    save_botton = Button(left_frame, text="Save",
                         command=save_current_file, width=10, height=1).place(x=35, y=130)

    right_frame = Frame(main_frame)
    right_frame.pack(side=TOP, fill=BOTH, expand=True)
    right_frame.grid_rowconfigure(0, weight=1)
    right_frame.grid_columnconfigure(0, weight=1)

    # The Text widget supports advanced text manipulation and
    entry = Text(right_frame, font=("TkDefaultFont", 12))
# formatting options, including the ability to apply tags to selected text.INSTEAD
#  ENRTY WIDGET
    entry.grid(row=0, column=1, sticky="nsew")
    entry.pack(side=TOP, fill=BOTH, expand=True)
    entry.tag_configure("font", font=("TkDefaultFont", 12))
    entry.focus()

    def close():
        if entry.get("1.0", "end-1c").strip():
            # Intercept the window closing event to run close
            frame.protocol("WM_DELETE_WINDOW", close)

    intro_screen(frame)
    frame.mainloop()


main_screen()
