import os
import glob
import pandas as pd

import tkinter as tk
from PIL import Image, ImageTk


directory = 'images_109'
excel_name = 'data_numer_paczki.xlsx'

df = pd.read_excel(excel_name)
extensions = ['png', 'jpg', 'jpeg']



def list_files(directory):
    files = []
    for ext in extensions:
        files.extend(glob.glob(os.path.join(directory, f'*.{ext}')))
    return files

files = list_files(directory)





class ImageViewer(tk.Tk):
    def __init__(self):
        super().__init__()

        self.current_image = 0
        self.current_column = 2


        self.image_frame = tk.Frame(self)
        self.image_label = tk.Label(self.image_frame)

        self.entry_field = tk.Text(self, wrap=tk.WORD, height=5)
        # self.entry_field = tk.Entry(self, width=50)
        self.entry_field.bind('<Return>', self.enter)
        self.entry_field.bind('<Shift-Up>', self.up)
        self.entry_field.bind('<Shift-Down>', self.down)



        self.next_b = tk.Button(self, text="Next Image", command=self.next)
        self.previous = tk.Button(self, text="Previous Image", command=self.prev)

        self.listbox = tk.Listbox(self, width=100, height=10)



        self.image_frame.grid(row=0, column=0,columnspan=2, padx=5, pady=5, sticky=tk.E)
        self.image_label.grid(row=0, column=0,columnspan=2, padx=5, pady=5, sticky=tk.E)
        self.entry_field.grid(row=1, column=0,columnspan=2, padx=5, pady=5, sticky=tk.E)
        self.next_b.grid(row=2, column=1, padx=5, pady=5)
        self.previous.grid(row=2, column=0, padx=5, pady=5)
        self.listbox.grid(row=0, column=2, rowspan=3, padx=10, pady=10, sticky=tk.NSEW)


        # df.loc[len(df)] = {}

        self.load_image()

    def up(self, event):
        if self.current_column != 2:
            self.current_column -= 1
            self.load_row(df, self.current_image)


    def down(self, event):
        if self.current_column != len(df.columns)-1:
            self.current_column += 1
            self.load_row(df, self.current_image)

    def enter(self, event):
        global df
        text = self.entry_field.get("1.0", tk.END)
        if text != "":
            if self.current_image < len(df):
                if self.current_column < len(df.columns):
                    print(self.current_image, self.current_column)
                    df.iloc[self.current_image, self.current_column] = text
        if self.current_column == len(df.columns)-1:
            self.next()

            self.current_column = 2
        else:
            self.current_column += 1
            self.load_row(df, self.current_image)

        df.to_excel(excel_name, index=False)
        self.entry_field.delete("1.0", tk.END)
        return "break"

    def next(self):
        if self.current_image < len(files):
            self.current_image = self.current_image+1
            self.load_image()

    def prev(self):
        if self.current_image != 0:
            self.current_image = self.current_image-1
            self.load_image()

    def load_image(self):
        global df
        image = Image.open(files[self.current_image])
        image = image.resize((400, 400))
        self.image_tk = ImageTk.PhotoImage(image)
        self.image_label.config(image=self.image_tk)

        if len(df) == self.current_image+1:
            df.loc[len(df)] = {}
        df.iloc[self.current_image, 1] = files[self.current_image]
        self.current_column = 2
        self.load_row(df, self.current_image)

    def load_row(self, dataframe, row_index):
        if row_index < len(dataframe):
            self.listbox.delete(0, tk.END)
            current_row = dataframe.iloc[row_index]
            for idx, (column, value) in enumerate(current_row.items()):
                if idx == self.current_column:
                    self.listbox.insert(tk.END, f"{column}: {value}" + " <---")
                else:
                    self.listbox.insert(tk.END, f"{column}: {value}")
        else:
            self.listbox.delete(0, tk.END)
            self.listbox.insert(tk.END, "Row index out of range")

if __name__ == "__main__":
    app = ImageViewer()
    app.mainloop()




df.to_excel(excel_name, index=False)
