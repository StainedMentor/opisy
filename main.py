import pandas as pd

import tkinter as tk
from PIL import Image, ImageTk


directory = 'images_109'
excel_name = 'moj.xlsx'

# if you want to instantly go to the next field after selecting an option from list
skip_on_select = True

# fixed size font (can be changed)
font_name = "courier"
font_size = 16




df = pd.read_excel(excel_name)
extensions = ['png', 'jpg', 'jpeg']


files = df['IMG_NAME'].tolist()


for index, file in enumerate(files):
    files[index] = directory+"/"+file



column_options = {
    6 : ["Eye Level Shot","Low Angle Shot","High Angle Shot","Hip Level Shot","Knee Level Shot","Ground Level Shot","Shoulder-Level Shot","Dutch Angle Shot","Birds - Eye - View Shot / Overhead Shot","Aerial Shot / Helicopter Shot","Close - up Shot"],
    7:["PHOTOGRAPHY","PAINTING","DIGITAL ART","LOGO","SKETCH","CARTOON","COMICS","POSTER","3D RENDER","ARCHITECTURAL RENDERING","DRAWING","SYMBOL","3D MODEL","SCHEMATICS","BROCHURE"],
    8:["SUNSET","SUNRISE","NIGHT","DAY","EVENING"],
    13:["YES","NO"],
    17:["DAYLIGHT","ARTIFICIAL"]
}


class ImageViewer(tk.Tk):
    def __init__(self):
        super().__init__()

        self.current_image = 0
        self.current_column = 2


        self.image_frame = tk.Frame(self)
        self.image_label = tk.Label(self.image_frame)

        self.entry_field = tk.Text(self, wrap=tk.WORD, height=5, font=(font_name, font_size))
        self.entry_field.bind('<Return>', self.enter)
        self.entry_field.bind('<Shift-Up>', self.up)
        self.entry_field.bind('<Shift-Down>', self.down)



        self.next_b = tk.Button(self, text="Next Image", command=self.next)
        self.previous = tk.Button(self, text="Previous Image", command=self.prev)

        self.listbox = tk.Listbox(self, width=100, height=10, font=(font_name, font_size))




        self.selector = tk.Listbox(self, font=(font_name, font_size))


        self.selector.bind('<<ListboxSelect>>', self.on_select)

        self.image_frame.grid(row=0, column=0,columnspan=2, padx=5, pady=5, sticky=tk.E)
        self.image_label.grid(row=0, column=0,columnspan=2, padx=5, pady=5, sticky=tk.E)
        self.entry_field.grid(row=1, column=0,columnspan=2, padx=5, pady=5, sticky=tk.E)
        self.next_b.grid(row=2, column=1, padx=5, pady=5)
        self.previous.grid(row=2, column=0, padx=5, pady=5)
        self.listbox.grid(row=0, column=2, rowspan=3, padx=10, pady=10, sticky=tk.NSEW)
        self.selector.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky=tk.NSEW)



        self.load_image()

    def on_select(self, event):
        listbox = event.widget
        index = listbox.curselection()
        value = listbox.get(index)

        if skip_on_select:
            self.fill_field(value)
            self.update_available_options()
            self.load_row(df, self.current_image)

        else:
            self.entry_field.delete("1.0", tk.END)
            self.entry_field.insert("1.0", value)
    def update_available_options(self):
        self.selector.delete(0,tk.END)
        if column_options.keys().__contains__(self.current_column):
            for item in column_options[self.current_column]:
                self.selector.insert(tk.END, item)
        required_height = min(12, self.selector.size())
        self.selector.config(height=required_height)
    def up(self, event):
        if self.current_column != 2:
            self.current_column -= 1
            self.update_available_options()
            self.load_row(df, self.current_image)


    def down(self, event):
        if self.current_column != len(df.columns)-1:
            self.current_column += 1
            self.update_available_options()
            self.load_row(df, self.current_image)

    def enter(self, event):
        global df
        text = self.entry_field.get("1.0", tk.END)

        self.fill_field(text)

        self.load_row(df, self.current_image)
        self.update_available_options()
        return "break"

    def fill_field(self, text):
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

        df.to_excel(excel_name, index=False)

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


        self.current_column = 2
        self.load_row(df, self.current_image)

    def load_row(self, dataframe, row_index):
        self.entry_field.delete("1.0", tk.END)
        if row_index < len(dataframe):
            self.listbox.delete(0, tk.END)
            current_row = dataframe.iloc[row_index]
            for idx, (column, value) in enumerate(current_row.items()):
                if idx == self.current_column:
                    self.listbox.insert(tk.END, "-->    " + "{:<30}".format(column + ":") + f"{value}")
                    self.entry_field.insert("1.0", value)
                else:
                    self.listbox.insert(tk.END, "       " + "{:<30}".format(column + ":") + f"{value}")

        else:
            self.listbox.delete(0, tk.END)
            self.listbox.insert(tk.END, "Row index out of range")

if __name__ == "__main__":
    app = ImageViewer()
    app.mainloop()




df.to_excel(excel_name, index=False)
