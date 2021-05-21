import tkinter as tk
from tkinter import ttk
import item_data as itemData
from tkinter import *

dataBase = itemData.Database()
allItems = dataBase.data()

try:
    file = open("saved.txt", "r")
    file.close()
except:
    file = open("saved.txt", "w")
    file.close()

def update_saved_items():
    file = open("saved.txt", "r")
    savedItems = file.read()
    savedItems = savedItems.split("\n")

update_saved_items()

class ItemExplorer:
    def update_list(self, data):
        #Clear list box
        self.my_list.delete(0, END)

        for item in data:
            self.my_list.insert(END, item['name'])

    def __init__(self, root=None):
        self.root = root
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill="both", expand=1)
        self.saved_page = SavedPage(master=self.root, app=self)

        self.my_canvas = tk.Canvas(self.main_frame)
        self.my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

        self.my_scrollbar = ttk.Scrollbar(self.main_frame, orient=VERTICAL, command=self.my_canvas.yview)
        self.my_scrollbar.pack(side=RIGHT, fill=Y)

        self.my_canvas.configure(yscrollcommand=self.my_scrollbar.set)
        self.my_canvas.bind('<Configure>', lambda e: self.my_canvas.configure(scrollregion=self.my_canvas.bbox("all")))

        self.second_frame = tk.Frame(self.my_canvas)

        self.my_canvas.create_window((0,0), window=self.second_frame, anchor="nw")

        self.my_label = tk.Label(self.second_frame, text="Start typing to find materials...",
                font=("Helvetica", 14), fg="grey").pack(pady=20, anchor=CENTER)

        self.my_entry = tk.Entry(self.second_frame, font=("Helvetica", 20))
        self.my_entry.pack()

        self.my_list = tk.Listbox(self.second_frame, width=50, height=20)
        self.my_list.pack(pady=40, padx=40, side=LEFT)

        self.my_new_list = tk.Listbox(self.second_frame, width=50, height=20)
        self.my_new_list.pack(pady=40, padx=40, side=RIGHT)

        self.my_list.bind("<<ListboxSelect>>", self.fillout)

        self.my_entry.bind("<KeyRelease>", self.check)

        self.refresh = tk.Button(self.main_frame, text="Refresh List", command=self.update_all_items)
        self.refresh.pack()
        self.saved = tk.Button(self.main_frame, text="Saved Items", command=self.go_to_saved)
        self.saved.pack(side=BOTTOM, anchor=CENTER)

        self.update_list(allItems)

    def update_all_items(self):
        dataBase.refresh_data()
        self.update_list(allItems)

    def fillout(self, e):
        self.my_new_list.delete(0, END)
        list_data = []

        for item in allItems:
            if self.my_list.get(ACTIVE) == item['name']:
                list_data.append(f"Name: {item['name']}")
                list_data.append(f"Data ID: {item['data_id']}")
                list_data.append(f"Rarity: {item['rarity']}")
                list_data.append(f"Restriction Level {item['restriction_level']}")
                list_data.append(f"Last Updated: {item['price_last_changed']}")
                list_data.append(f"Buy: {item['max_offer_unit_price']}")
                list_data.append(f"Sell: {item['min_sale_unit_price']}")
                list_data.append("______________________________________")
            
        for items in list_data:
            self.my_new_list.insert(END, items)

    def check(self, e):
        typed = self.my_entry.get()

        if typed == "":
            data = allItems
        else:
            data = []
            for item in allItems:
                if typed.lower() in item['name'].lower():
                    data.append(item)
        
        self.update_list(data)

    def go_to_saved(self):
        self.main_frame.pack_forget()
        self.saved_page.start_page()

class SavedPage:
    def __init__(self, master=None, app=None):
        self.master = master
        self.app = app
        self.frame = tk.Frame(self.master)
        tk.Label(self.frame, text='Page 1').pack()
        #tk.Button(self.frame, text='Go back', command=self.go_back).pack()

    def start_page(self):
        self.frame.pack()

if __name__ == '__main__':
    root = tk.Tk()
    root.title("GW2 - Trading information")
    root.iconphoto(False, tk.PhotoImage(file="icon.png"))
    root.geometry("1000x600")
    app = ItemExplorer()
    root.mainloop()