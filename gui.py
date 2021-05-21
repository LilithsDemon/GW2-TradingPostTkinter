from tkinter import *
from tkinter import ttk
import item_data as itemData
import os


dataBase = itemData.Database()
dataBase.refresh_data()
allItems = dataBase.data()

root = Tk()
root.title("GW2 - Trading information")
root.iconphoto(False, PhotoImage(file="icon.png"))
root.geometry("1000x600")

main_frame = Frame(root)
main_frame.pack(fill=BOTH, expand=1)

my_canvas = Canvas(main_frame)
my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
my_scrollbar.pack(side=RIGHT, fill=Y)

my_canvas.configure(yscrollcommand=my_scrollbar.set)
my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

second_frame = Frame(my_canvas)

my_canvas.create_window((0,0), window=second_frame, anchor="nw")

def item(positiony, index):
    Button(second_frame, text=f"{allItems[index]['name']}").pack(pady=5, padx = 5, anchor=W)


my_label = Label(second_frame, text="Start typing to find materials...",
           font=("Helvetica", 14), fg="grey").pack(pady=20, anchor=CENTER)

my_entry = Entry(second_frame, font=("Helvetica", 20))
my_entry.pack()

my_list = Listbox(second_frame, width=50, height=20)
my_list.pack(pady=40, padx=40, side=LEFT)

my_new_list = Listbox(second_frame, width=50, height=20)
my_new_list.pack(pady=40, padx=40, side=RIGHT)

def fillout(e):
    my_new_list.delete(0, END)
    list_data = []

    for item in allItems:
        if my_list.get(ACTIVE) == item['name']:
            list_data.append(f"Name: {item['name']}")
            list_data.append(f"Data ID: {item['data_id']}")
            list_data.append(f"Rarity: {item['rarity']}")
            list_data.append(f"Restriction Level {item['restriction_level']}")
            list_data.append(f"Last Updated: {item['price_last_changed']}")
            list_data.append(f"Buy: {item['max_offer_unit_price']}")
            list_data.append(f"Sell: {item['min_sale_unit_price']}")
            list_data.append("______________________________________")
    
    for items in list_data:
        my_new_list.insert(END, items)


def check(e):
    typed = my_entry.get()

    if typed == "":
        data = allItems
    else:
        data = []
        for item in allItems:
            if typed.lower() in item['name'].lower():
                data.append(item)

    update_list(data)
        

def update_list(data):
    #Clear list box
    my_list.delete(0, END)

    for item in data:
        my_list.insert(END, item['name'])

update_list(allItems)


my_list.bind("<<ListboxSelect>>", fillout)

my_entry.bind("<KeyRelease>", check)


root.mainloop()