# Version 4.2 | Code: Lypheo | Idee: Nino
# Gui Version 1.0 | Django.Durano

from tkinter import *
import ass
import re
import sys
import os
import tkinter.filedialog as fd


replace = [("'", "’"), ("...", "…"), ("--", "–"), ("!?", "?!")]
quotes = ("„", "“")
# Change Prefix here. Will be added at the end of filename.
prefix: str = '_fixed'


class RepGUI:
    # Create Main Window
    def __init__(self, master):
        self.master = master
        master.title("Fuehre mich GUI")
        master.geometry("800x400")

        # Create Frame for Label's and Button's
        self.frame = Frame(master)
        self.frame.pack()

        # Create Label's
        self.label1 = Label(self.frame, text="Source Location:")
        self.label1.grid(row=0, column=0, pady=20)

        self.label2 = Label(self.frame, text="Save Destination:")
        self.label2.grid(row=1, column=0)

        # Create Entry's
        self.text1 = Entry(self.frame, width=100)
        self.text1.grid(row=0, column=1, columnspan=4, padx=10)

        self.text2 = Entry(self.frame, width=100)
        self.text2.grid(row=1, column=1, columnspan=4, padx=10)

        # Create Button's for Opening (put folder-open.png in the same folder)
        if os.path.isfile('folder-open.png'):
            self.image = PhotoImage(file='folder-open.png')
            self.image = self.image.subsample(18, 18)
            self.button1 = Button(self.frame, image=self.image, command=lambda: self.open("text1"), borderwidth=0)
            self.button1.grid(row=0, column=6, pady=10, sticky='NWSE')

            self.button2 = Button(self.frame, image=self.image, command=lambda: self.save("text2"), borderwidth=0)
            self.button2.grid(row=1, column=6, pady=10, sticky='NWSE')
        else:
            self.button1 = Button(self.frame, text="Browse", command=lambda: self.open("text1"), borderwidth=1)
            self.button1.grid(row=0, column=6, pady=10)

            self.button2 = Button(self.frame, text="Browse", command=lambda: self.save("text2"), borderwidth=1)
            self.button2.grid(row=1, column=6, pady=10)

        # Create Clear and Process Button
        self.clear_button = Button(master, text='Clear', command=self.clear)
        self.clear_button.place(x=350, y=115, width=70, height=28, anchor="center")

        self.process_button = Button(master, text='Process', command=lambda: process(self.text1.get(), self.text2.get()))
        self.process_button.place(x=450, y=115, width=70, height=28, anchor="center")

    # Function search Source path
    def open(self, arg):
        try:
            path = globals()['path'][0]
        except KeyError:
            path = "/"

        file = fd.askopenfilename(parent=self.master, initialdir=path, title='Choose a file',
                                  filetypes=(("Ass files", "*.ass"), ("All files", "*.*")))
        if len(file) > 0:
            globals()['path'], filename = os.path.split(file), os.path.splitext(file)
            self.__dict__[arg].delete(0, 'end')
            self.__dict__[arg].insert(INSERT, os.path.normpath(file))
            self.text2.delete(0, 'end')
            self.text2.insert(INSERT, f'{os.path.normpath(filename[0])}{prefix}{filename[1]}')

    # Function save Output Path
    def save(self, arg):
        try:
            path = globals()['path'][0]
        except KeyError:
            path = "/"

        file = fd.asksaveasfilename(parent=self.master, initialdir=path, title='Choose a file',
                                    filetypes=(("Ass files", "*.ass"), ("All files", "*.*")))
        if len(file) > 0:
            self.__dict__[arg].delete(0, 'end')
            self.__dict__[arg].insert(INSERT, f'{os.path.normpath(file)}.ass')

    def clear(self):
        for text in self.__dict__:
            if 'text' in text:
                self.__dict__[text].delete(0, 'end')


# Put Code from fuehre-mich.py here, change sys.argv[1] in source and sys.argv[2] in out
def process(source, out):

    with open(source, "r", encoding="utf-8-sig") as f:
        doc = ass.parse(f)

    even = True
    for i in range(len(doc.events)):
        line = doc.events[i].text

        for x in replace:
            line = line.replace(x[0], x[1])

        line = re.sub(r'(^|\s|\\N|\})-', r"\1–", line)
        line = re.sub(r"–(\S)", r"– \1", line)

        while '"' in line:
            line = line.replace('"', quotes[0], 1) if even else line.replace('"', quotes[1], 1)
            even = not even

        doc.events[i].text = line

    with open(out, "w", encoding="utf-8-sig") as f:
        doc.dump_file(f)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        process(sys.argv[1], sys.argv[2])
    else:
        root = Tk()
        my_gui = RepGUI(root)
        root.mainloop()
