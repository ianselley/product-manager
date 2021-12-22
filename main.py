from tkinter import StringVar, Tk, Label, LabelFrame, Entry, Toplevel, ttk, messagebox
import models
import db


db.Base.metadata.create_all(db.engine)

root = Tk()
root.title("Product Manager")
root.resizable(1, 1)
root.wm_iconbitmap("src/images/icon.ico")
# root.iconphoto(False, PhotoImage(file="src/images/icon.ico"))  # This is for mac


bigger = ttk.Style()
bigger.configure("bigger.TButton", font=("Arial", 11))

MARGIN = 12
PADDING = 9


def clean_table(table: ttk.Treeview):
    for line in table.get_children():
        table.delete(line)


def populate_table(table: ttk.Treeview):
    products = models.get_products()
    for product in products:
        # I save the id of the product in the "tags" attribute so when I want to access the product, I can get its id
        table.insert(
            "",
            0,
            text=product.name,
            values=[product.price, product.category, product.stock],
            tags=product.id,
        )


def update_table(table: ttk.Treeview):
    clean_table(table)
    populate_table(table)


def name_is_correct(name: str):
    if len(name) == 0:
        return False, "A name is required\n"
    return True, ""


def category_is_correct(category: str):
    if len(category) == 0:
        return False, "A category is required\n"
    return True, ""


def price_is_correct(price: str):
    if len(price) == 0:
        return False, "A price is required.\n"
    try:
        price = float(price)
    except ValueError:
        return False, "Price must be a number.\n"
    if price < 0:
        return False, "Price must be positive.\n"
    return True, ""


def stock_is_correct(stock: str):
    if len(stock) == 0:
        return False, "A stock quantity is required.\n"
    try:
        stock = int(stock)
    except ValueError:
        return False, "Stock must be an integer.\n"
    if stock < 0:
        return False, "Stock must be positive.\n"
    return True, ""


def validate_form(name, price, category, stock="0"):
    name_ok, name_message = name_is_correct(name)
    price_ok, price_message = price_is_correct(price)
    category_ok, category_message = category_is_correct(category)
    stock_ok, stock_message = stock_is_correct(stock)

    if not (name_ok and price_ok and category_ok and stock_ok):
        return False, name_message + price_message + category_message + stock_message
    else:
        return True, ""


def add_product():
    name = name_entry.get()
    price = price_entry.get()
    category = category_entry.get()
    stock = stock_entry.get()
    form_ok, form_message = validate_form(name, price, category, stock)
    if not form_ok:
        message["text"] = form_message
    else:
        message["text"] = ""
        models.add_product(name=name, price=price, category=category, stock=stock)
        update_table(table)
        name_entry["textvariable"] = StringVar(value="")
        price_entry["textvariable"] = StringVar(value="")
        category_entry["textvariable"] = StringVar(value="")
        stock_entry["textvariable"] = StringVar(value="")


def edit_product():
    global new_name_entry, new_price_entry, new_category_entry, edit_root, edit_message
    selection = table.selection()

    if not selection:
        message["text"] = "You must select one product"
        return

    if len(selection) > 1:
        message["text"] = "You must select only one product"
        return

    product_id = table.item(selection)["tags"][0]
    product = models.get_product(product_id)

    edit_root = Toplevel()
    edit_root.title("Edit Product details")
    edit_root.resizable(1, 1)
    edit_root.wm_iconbitmap("src/images/icon.ico")
    # root.iconphoto(False, PhotoImage(file="src/images/icon.ico"))  # This is for mac

    edit_frame = LabelFrame(
        edit_root, width=150, padx=10, pady=10, text="Edit Product", font=("Arial", 11)
    )
    edit_frame.grid(
        row=0,
        column=0,
        columnspan=2,
        padx=MARGIN,
        pady=PADDING,
        sticky="we",
    )

    # Label previous name
    new_name_label = Label(edit_frame, text="Previous name: ", font=("Arial", 11))
    new_name_label.grid(row=0, column=0)

    # Disbled entry previous name
    previous_name_entry = Entry(
        edit_frame,
        width=50,
        textvariable=StringVar(edit_root, value=product.name),
        state="readonly",
        font=("Arial", 11),
    )
    previous_name_entry.grid(row=0, column=1)

    # Label new name
    new_name_label = Label(edit_frame, text="New name: ", font=("Arial", 11))
    new_name_label.grid(row=1, column=0, pady=PADDING, sticky="we")

    # Entry new name
    new_name_entry = Entry(
        edit_frame, textvariable=StringVar(value=product.name), font=("Arial", 11)
    )
    new_name_entry.grid(row=1, column=1, sticky="we")

    # Label previous price
    previous_price_label = Label(
        edit_frame, text="Previous price: ", font=("Arial", 11)
    )
    previous_price_label.grid(row=2, column=0)

    # Disbled entry previous price
    previous_price_entry = Entry(
        edit_frame,
        width=50,
        textvariable=StringVar(edit_root, value=product.price),
        state="readonly",
        font=("Arial", 11),
    )
    previous_price_entry.grid(row=2, column=1)

    # Label new price
    new_price_label = Label(edit_frame, text="New price: ", font=("Arial", 11))
    new_price_label.grid(row=3, column=0, pady=PADDING, sticky="we")

    # Entry new price
    new_price_entry = Entry(
        edit_frame, textvariable=StringVar(value=product.price), font=("Arial", 11)
    )
    new_price_entry.grid(row=3, column=1, sticky="we")

    # Label previous category
    previous_category_label = Label(
        edit_frame, text="Previous category: ", font=("Arial", 11)
    )
    previous_category_label.grid(row=4, column=0)

    # Disbled entry previous category
    previous_category_entry = Entry(
        edit_frame,
        width=50,
        textvariable=StringVar(edit_root, value=product.category),
        state="readonly",
        font=("Arial", 11),
    )
    previous_category_entry.grid(row=4, column=1)

    # Label new category
    new_category_label = Label(edit_frame, text="New category: ", font=("Arial", 11))
    new_category_label.grid(row=5, column=0, pady=PADDING, sticky="we")

    # Entry new category
    new_category_entry = Entry(
        edit_frame, textvariable=StringVar(value=product.category), font=("Arial", 11)
    )
    new_category_entry.grid(row=5, column=1, sticky="we")

    # Error message in edit root
    edit_message = Label(edit_root, text="", fg="red", font=("Arial", 11))
    edit_message.grid(row=1, column=0, columnspan=2, sticky="we")

    # Save button
    save_button = ttk.Button(
        edit_root,
        text="SAVE",
        command=lambda: save_edit(product_id),
        style="bigger.TButton",
    )
    save_button.grid(row=2, column=0, sticky="we")

    # Cancel button
    cancel_button = ttk.Button(
        edit_root, text="CANCEL", command=edit_root.destroy, style="bigger.TButton"
    )
    cancel_button.grid(row=2, column=1, sticky="we")


def save_edit(product_id):
    new_name = new_name_entry.get()
    new_price = new_price_entry.get()
    new_category = new_category_entry.get()
    form_ok, form_message = validate_form(new_name, new_price, new_category)
    if not form_ok:
        edit_message["text"] = form_message
    else:
        models.edit_product(product_id, new_name, new_price, new_category)
        edit_root.destroy()
        update_table(table)


def delete_product():
    selection = table.selection()
    if not selection:
        message["text"] = "You must select at least one product"
        return
    for product in selection:
        product_id = table.item(product)["tags"][0]
        table.delete(product)
        models.delete_product(product_id)


def save_sell(product_id):
    stock_sold = sell_entry.get()
    product = models.get_product(product_id)
    stock_ok, stock_message = stock_is_correct(stock_sold)
    if not stock_ok:
        sell_message["text"] = stock_message
    elif (new_stock := product.stock - int(stock_sold)) < 0:
        sell_message["text"] = "You don't have enough stock"
    else:
        models.edit_product(product_id, new_stock=new_stock)
        order = False
        if new_stock == 0:
            order = messagebox.askyesno(
                message=f"There are 0 items in stock of: {product.name}. Do you want to order some more?",
                icon="question",
                title=f"Order {product.name}",
            )
        if order:
            order_product()
        sell_window.destroy()
        update_table(table)


def save_order(product_id):
    stock_ordered = order_entry.get()
    product = models.get_product(product_id)
    stock_ok, stock_message = stock_is_correct(stock_ordered)
    if not stock_ok:
        order_message["text"] = stock_message
    else:
        new_stock = product.stock + int(stock_ordered)
        models.edit_product(product_id, new_stock=new_stock)
        order_window.destroy()
        update_table(table)


def sell_product():
    global sell_entry, sell_window, sell_message
    selection = table.selection()

    if not selection:
        message["text"] = "You must select one product"
        return

    if len(selection) > 1:
        message["text"] = "You must select only one product"
        return

    product_id = table.item(selection)["tags"][0]
    product = models.get_product(product_id)

    sell_window = Toplevel()
    sell_window.title("Sell Product")
    sell_window.resizable(1, 1)
    sell_window.wm_iconbitmap("src/images/icon.ico")
    # root.iconphoto(False, PhotoImage(file="src/images/icon.ico"))  # This is for mac

    info = Label(
        sell_window,
        text=f"There are {product.stock} items left in stock of the product: {product.name}",
        font=("Arial", 11),
    )
    info.grid(row=0, column=0, columnspan=2, padx=PADDING, pady=PADDING, sticky="we")

    frame = LabelFrame(sell_window, padx=PADDING, pady=PADDING, font=("Arial", 11))
    frame.grid(row=1, column=0, columnspan=2, padx=PADDING, pady=PADDING)

    sell_label = Label(
        frame,
        text="How many items do you want to sell?",
        font=("Arial", 11),
    )
    sell_label.grid(row=1, column=0, padx=PADDING)

    sell_entry = Entry(frame, font=("Arial", 11))
    sell_entry.grid(row=1, column=1, padx=PADDING)

    # Error message in sell window
    sell_message = Label(sell_window, text="", fg="red", font=("Arial", 11))
    sell_message.grid(row=2, column=0, columnspan=2, sticky="we")

    # Save button
    save_button = ttk.Button(
        sell_window,
        text="SAVE",
        command=lambda: save_sell(product_id),
        style="bigger.TButton",
    )
    save_button.grid(row=3, column=0, sticky="we")

    # Cancel button
    cancel_button = ttk.Button(
        sell_window, text="CANCEL", command=sell_window.destroy, style="bigger.TButton"
    )
    cancel_button.grid(row=3, column=1, sticky="we")


def order_product():
    global order_entry, order_window, order_message
    selection = table.selection()

    if not selection:
        message["text"] = "You must select one product"
        return

    if len(selection) > 1:
        message["text"] = "You must select only one product"
        return

    product_id = table.item(selection)["tags"][0]
    product = models.get_product(product_id)

    order_window = Toplevel()
    order_window.title("Order Product")
    order_window.resizable(1, 1)
    order_window.wm_iconbitmap("src/images/icon.ico")
    # root.iconphoto(False, PhotoImage(file="src/images/icon.ico"))  # This is for mac

    info = Label(
        order_window,
        text=f"There are {product.stock} items left in stock of the product: {product.name}",
        font=("Arial", 11),
    )
    info.grid(row=0, column=0, columnspan=2, padx=PADDING, pady=PADDING, sticky="we")

    frame = LabelFrame(order_window, padx=PADDING, pady=PADDING, font=("Arial", 11))
    frame.grid(row=1, column=0, columnspan=2, padx=PADDING, pady=PADDING)

    order_label = Label(
        frame,
        text="How many items do you want to order?",
        font=("Arial", 11),
    )
    order_label.grid(row=1, column=0, padx=PADDING)

    order_entry = Entry(frame, font=("Arial", 11))
    order_entry.grid(row=1, column=1, padx=PADDING)

    # Error message in order window
    order_message = Label(order_window, text="", fg="red", font=("Arial", 11))
    order_message.grid(row=2, column=0, columnspan=2, sticky="we")

    # Save button
    save_button = ttk.Button(
        order_window,
        text="SAVE",
        command=lambda: save_order(product_id),
        style="bigger.TButton",
    )
    save_button.grid(row=3, column=0, sticky="we")

    # Cancel button
    cancel_button = ttk.Button(
        order_window,
        text="CANCEL",
        command=order_window.destroy,
        style="bigger.TButton",
    )
    cancel_button.grid(row=3, column=1, sticky="we")


# Create main frame
frame = LabelFrame(root, text="Register a new product", font=("Arial", 11))
frame.grid(
    row=0,
    column=0,
    columnspan=4,
    padx=MARGIN * 9,
    pady=PADDING,
    sticky="we",
)

# Label name
name_label = Label(frame, padx=PADDING, text="Name: ", font=("Arial", 11))
name_label.grid(row=0, column=0, padx=PADDING, pady=PADDING, sticky="we")

# Entry name
name_entry = Entry(frame, width=80, font=("Arial", 11))
name_entry.focus()
name_entry.grid(row=0, column=1, columnspan=3, padx=PADDING, sticky="we")

# Label price
price_label = Label(frame, text="Price: ", font=("Arial", 11))
price_label.grid(row=1, column=0, padx=PADDING, sticky="we")

# Entry price
price_entry = Entry(frame, font=("Arial", 11))
price_entry.grid(row=1, column=1, columnspan=3, padx=PADDING, sticky="we")

# Label category
category_label = Label(frame, text="Category: ", font=("Arial", 11))
category_label.grid(row=2, column=0, padx=PADDING, pady=PADDING, sticky="we")

# Entry category
category_entry = Entry(frame, font=("Arial", 11))
category_entry.grid(row=2, column=1, columnspan=3, padx=PADDING, sticky="we")

# Label stock
stock_label = Label(frame, text="Stock: ", font=("Arial", 11))
stock_label.grid(row=3, column=0, padx=PADDING, sticky="we")

# Entry stock
stock_entry = Entry(frame, font=("Arial", 11))
stock_entry.grid(row=3, column=1, columnspan=3, padx=PADDING, sticky="we")

# Button save
save_button = ttk.Button(
    frame, text="Save Product", command=add_product, style="bigger.TButton"
)
save_button.grid(row=4, columnspan=4, padx=PADDING, pady=PADDING, sticky="we")

# Error message
message = Label(root, text="", fg="red", font=("Arial", 11))
message.grid(row=1, column=0, columnspan=4, padx=PADDING, sticky="we")

# Styling Treeview
basic = ttk.Style()
basic.configure("basic.Treeview", font=("Arial", 11), highlightthickness=0, bd=0)
basic.configure("basic.Treeview.Heading", font=("Calibri", 13, "bold"))
basic.layout("basic.Treeview", [("basic.Treeview.treearea", {"sticky": "nswe"})])

# Table structure
table = ttk.Treeview(
    root, height=20, columns=("#1", "#2", "#3"), style="basic.Treeview"
)
table.grid(row=2, column=0, columnspan=4)
table.heading("#0", text="Name", anchor="center")
table.heading("#1", text="Price", anchor="center")
table.heading("#2", text="Category", anchor="center")
table.heading("#3", text="Stock", anchor="center")

populate_table(table)

# Scrollbar
scrollbar = ttk.Scrollbar(root, command=table.yview)
scrollbar.grid(row=2, rowspan=20, column=4, sticky="ns")

table.configure(yscrollcommand=scrollbar.set)

# Spacing
Label(root).grid(row=3, column=0)

# Edit button
edit_button = ttk.Button(
    root, text="EDIT", command=edit_product, style="bigger.TButton"
)
edit_button.grid(row=5, column=0, sticky="we")

# Delete button
delete_button = ttk.Button(
    root, text="DELETE", command=delete_product, style="bigger.TButton"
)
delete_button.grid(row=5, column=1, sticky="we")

# Sell button
sell_button = ttk.Button(
    root, text="SELL", command=sell_product, style="bigger.TButton"
)
sell_button.grid(row=5, column=2, sticky="we")

# Reorder button
sell_button = ttk.Button(
    root, text="ORDER", command=order_product, style="bigger.TButton"
)
sell_button.grid(row=5, column=3, sticky="we")


root.mainloop()
