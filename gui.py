import tkinter as tk
from tkinter import ttk
import item_data as itemData
from tkinter import *

dataBase = itemData.Database()
allItems = dataBase.data()


class SavedItems:
    def __init__(self):
        self.savedItemsList = []
        self.update_saved_items()      

    def update_saved_items(self):
        file = open("saved.txt", "r")
        savedItems = file.read()
        file.close()
        self.savedItemsList = savedItems.split("\n")
        if self.savedItemsList[0] == '':
            self.savedItemsList.pop(0)
                

    def add_item(self, name):
        self.savedItemsList.append(name)
        text = ""
        for index in range(len(self.savedItemsList)):
            if index == 0:
                text += f"{self.savedItemsList[index]}"
            else:
                text += f"\n{self.savedItemsList[index]}"
        file=open("saved.txt", "w")
        file.write(text)
        file.close()
        self.update_saved_items()

    def remove_item(self, name):
        self.savedItemsList.remove(name)
        text = ""
        for index in range(len(self.savedItemsList)):
            if index == 0:
                text += f"{self.savedItemsList[index]}"
            else:
                text += f"\n{self.savedItemsList[index]}"
        file=open("saved.txt", "w")
        file.write(text)
        file.close()
        self.update_saved_items()


savedItems = SavedItems()

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
        
        self.my_label = tk.Label(self.main_frame, text="Start typing to find materials...",
                font=("Helvetica", 14), fg="grey").pack(pady=20, anchor=CENTER)

        self.my_entry = tk.Entry(self.main_frame, font=("Helvetica", 20))
        self.my_entry.pack()

        self.my_list = tk.Listbox(self.main_frame, width=40, height=20)
        self.my_list.pack(pady=10, padx=40, side=LEFT)

        self.my_new_list = tk.Listbox(self.main_frame, width=40, height=20)
        self.my_new_list.pack(pady=40, padx=40, side=RIGHT)

        self.my_list.bind("<<ListboxSelect>>", self.fillout)

        self.my_entry.bind("<KeyRelease>", self.check)
        
        
        self.refresh = tk.Button(self.main_frame, text="Refresh List", command=self.update_all_items)
        self.refresh.pack(pady=5,side = TOP)
        self.addToSaved = tk.Button(self.main_frame, text="Add to Saved", command=self.add_item_to_saved)
        self.addToSaved.pack(pady=20, padx=0)
        self.saved = tk.Button(self.main_frame, text="Saved Items", command=self.go_to_saved)
        self.saved.pack(side=BOTTOM, anchor=CENTER)

        self.update_list(allItems)

    def add_item_to_saved(self):
        savedItems.add_item(self.my_list.get(ACTIVE))

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

    def start_main_page(self):
        self.main_frame.pack()

class SavedPage:
    def __init__(self, master=None, app=None):
        self.master = master
        self.app = app
        self.frame = tk.Frame(self.master)
        self.my_label = tk.Label(self.frame, text="Start typing to find saved materials...",
                font=("Helvetica", 14), fg="grey").pack(pady=20, anchor=CENTER)

        self.my_entry = tk.Entry(self.frame, font=("Helvetica", 20))
        self.my_entry.pack()

        self.my_list = tk.Listbox(self.frame, width=40, height=20)
        self.my_list.pack(pady=10, padx=40, side=LEFT)

        self.my_new_list = tk.Listbox(self.frame, width=40, height=20)
        self.my_new_list.pack(pady=40, padx=40, side=RIGHT)

        self.my_list.bind("<<ListboxSelect>>", self.fillout)

        self.my_entry.bind("<KeyRelease>", self.check)
        
        
        self.refresh = tk.Button(self.frame, text="Refresh List", command=self.update_all_items)
        self.refresh.pack(pady=5,side = TOP)
        self.refresh = tk.Button(self.frame, text="Remove Saved Item", command=self.remove_save)
        self.refresh.pack(pady=5,side = TOP)
        self.saved = tk.Button(self.frame, text="All Items", command=self.go_to_item_explorer)
        self.saved.pack(side=BOTTOM, anchor=CENTER)

        self.update_list(savedItems.savedItemsList)

    def remove_save(self):
        savedItems.remove_item(self.my_list.get(ACTIVE))
        self.update_list(savedItems.savedItemsList)

    def update_list(self, data):
        #Clear list box
        self.my_list.delete(0, END)

        for item in data:
            self.my_list.insert(END, item)

    def update_all_items(self):
        dataBase.refresh_data()
        self.update_list(savedItems.savedItemsList)

    def fillout(self, e):
        self.my_new_list.delete(0, END)
        list_data = []

        for item in allItems:
            if self.my_list.get(ACTIVE) == item['name']:
                list_data.append(f"Name: {item['name']}")
                list_data.append(f"Data ID: {item['data_id']}")
                list_data.append(f"Rarity: {item['rarity']}")
                list_data.append(f"Level To Use:  {item['restriction_level']}")
                list_data.append(f"Last Updated: {item['price_last_changed']}")
                list_data.append(f"Buy: {item['max_offer_unit_price']}")
                list_data.append(f"Sell: {item['min_sale_unit_price']}")
                list_data.append("______________________________________")
            
        for items in list_data:
            self.my_new_list.insert(END, items)

    def check(self, e):
        typed = self.my_entry.get()

        if typed == "":
            data = savedItems.savedItemsList
        else:
            data = []
            for item in savedItems.savedItemsList:
                if typed.lower() in item['name'].lower():
                    data.append(item)
        
        self.update_list(data)

    def start_page(self):
        self.frame.pack()

    def go_to_item_explorer(self):
        self.frame.pack_forget()
        self.app.start_main_page()

if __name__ == '__main__':
    root = tk.Tk()
    root.title("GW2 - Trading information")
    root.iconphoto(False, tk.PhotoImage(file="icon.png"))
    root.geometry("1000x600")
    app = ItemExplorer(root)
    root.mainloop()
