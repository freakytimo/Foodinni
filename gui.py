import tkinter as tk
import login
import subprocess
import requests
from tkinter import ttk
import os
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from datetime import datetime
import textwrap

# Create a folder for bills (if it doesn't exist)
output_folder = "bills"
os.makedirs(output_folder, exist_ok=True)

#Global Variable
customer_identifier = "Unknown"


def logout():
    # Close the entire tkinter window
    root.destroy()
    subprocess.Popen(["python", "gui.py"])

def add_customer():

    global customer_identifier

    #Checks if the customer is in the API and adds it to the URL
    customer_url = "https://api.mimil-grp.eu/foodinni/cashier/getCustomerByIdentifier.php"
    customer_identifier = customer_var.get()
    customer_params = {'identifier': customer_identifier}

    try:
        response = requests.get(customer_url, headers=login.get_headers(), params=customer_params)
        if response.status_code == 200:
            print(response.status_code)
            print(f"Customer '{customer_identifier}' exists in the API.")
            customeruser_label.config(text=f'{customer_identifier}')
        else:
            print(f"No customer found with identifier '{customer_identifier}'.")
    except requests.RequestException as e:
        print("Error: No Connection to API", e)

    customer_var.set("")
#def add_item():
item_url = "https://api.mimil-grp.eu/foodinni/public/getAllItems.php"

# Send a GET request to the API
response = requests.get(item_url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the response JSON
    items = response.json()

    # Create a dictionary to store the items (using EAN13 as keys)
    item_dict = {}

    # Function to add an item by EAN13
def add_item():
    ean13_to_add = input_var.get()
    # Get the kg from the kg entry, default to 1 if not specified or invalid
    kg_to_add = float(kg_var.get()) if kg_var.get() and kg_var.get().replace('.', '', 1).isdigit() else 1.0
    # Get the count from the count entry, default to 1 if not specified or invalid
    count_to_add = int(nr_var.get()) if nr_var.get() and nr_var.get().isdigit() else 1
    for item in items:
        if item["ean13"] == ean13_to_add:
            if "price_kg" in item and item["price_kg"]:  # Check if the item has a per kg price
                if ean13_to_add in item_dict:
                    # Item already exists, update the kg and count
                    item_dict[ean13_to_add]["kg"] += kg_to_add
                    item_dict[ean13_to_add]["count"] += count_to_add
                else:
                    # New item with kg price, add it to the dictionary with specified count
                    item_dict[ean13_to_add] = {
                        "count": count_to_add,
                        "name": item["name"],
                        "price": item["price"],
                        "price_kg": item["price_kg"],
                        "kg": kg_to_add  # Set kg as specified
                    }
            else:
                # Item without kg price, add normally with specified count
                if ean13_to_add in item_dict:
                    # Item already exists, increment the count by the specified amount
                    item_dict[ean13_to_add]["count"] += count_to_add
                else:
                    # New item, add it to the dictionary with specified count and 'kg' key set to 0
                    item_dict[ean13_to_add] = {
                        "count": count_to_add,
                        "name": item["name"],
                        "price": item["price"],
                        "price_kg": None,  # Set 'price_kg' to None for items without a per kg price
                        "kg": 0  # Set 'kg' to 0 for items without a per kg price
                    }
            print(f"Item with EAN13 {ean13_to_add} added to the list.")
            update_treeview()
            break

    # Function to update the treeview
def update_treeview():
    tree.delete(*tree.get_children())
    total_price = 00.00
    for ean13, item_info in item_dict.items():
        if item_info["price_kg"] is not None:
            price = item_info["price_kg"] * item_info["kg"]
        else:
            price = item_info["price"] * item_info["count"]
        total_price += price

        # Format the price and kg to two decimal places
        formatted_total_price = f"{total_price:.2f}"
        formatted_price = f"{price:.2f}"
        formatted_kg = f"{item_info['kg']:.2f}"

        tree.insert("", "end", values=(
            item_info["count"], item_info["name"], item_info["price"], item_info["price_kg"], formatted_kg,
            formatted_price))

        price_var.set(formatted_total_price)
        kg_var.set("1")
        nr_var.set("1")
        input_var.set("")

# Function to remove kg from a selected item by its ID
def remove_item():
    selected_item = tree.selection()
    if not selected_item:
        print("No item selected to remove.")
        return
    # Get the values from the entry fields, default to 1 if not specified
    kg_to_remove = float(kg_var.get()) if kg_var.get() else 1.0
    count_to_remove = int(nr_var.get()) if nr_var.get() else 1
    for item_id in selected_item:
        # Retrieve the item's values
        item_values = tree.item(item_id, 'values')
        # Find the EAN13 in the item_dict using the name (assuming name is unique)
        ean13_to_remove = None
        for ean13, item_info in item_dict.items():
            if item_info["name"] == item_values[1]:  # Assuming name is in the second column
                ean13_to_remove = ean13
                break
        if ean13_to_remove:
            # Check if the item has a 'price_kg' to decide on removal method
            if item_dict[ean13_to_remove].get("price_kg"):
                # It's a kg item, remove by kg
                if item_dict[ean13_to_remove]["kg"] > kg_to_remove:
                    item_dict[ean13_to_remove]["kg"] -= kg_to_remove
                else:
                    del item_dict[ean13_to_remove]
                print(f"{kg_to_remove} kg removed from item with EAN13 {ean13_to_remove}.")
            else:
                # It's a count item, remove by count
                if item_dict[ean13_to_remove]["count"] > count_to_remove:
                    item_dict[ean13_to_remove]["count"] -= count_to_remove
                else:
                    del item_dict[ean13_to_remove]
                print(f"{count_to_remove} count removed from item with EAN13 {ean13_to_remove}.")
            tree.delete(item_id)
            # Re-insert the item with updated values if there's still some left
            if ean13_to_remove in item_dict:
                tree.insert("", "end", values=(
                    item_dict[ean13_to_remove]["count"],
                    item_dict[ean13_to_remove]["name"],
                    item_dict[ean13_to_remove]["price"],
                    item_dict[ean13_to_remove]["price_kg"],
                    item_dict[ean13_to_remove]["kg"],
                    item_dict[ean13_to_remove]["price_kg"] * item_dict[ean13_to_remove]["kg"] if
                    item_dict[ean13_to_remove]["price_kg"] else item_dict[ean13_to_remove]["price"]
                ))
        else:
            print("Item not found in the list.")
    update_treeview()
    kg_var.set("1")
    nr_var.set("1")


def generate_pdf():
    global customer_identifier
    max_name_length = 35  # Maximum length for product name

    try:
        # Generate a unique filename using the current timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        pdf_filename = os.path.join(output_folder, f"bill_{timestamp}.pdf")

        # Create a PDF canvas with the specified dimensions
        width, height = 70 * mm, 200  # Initialize height

        textwrap_count = 0  # Counter Variable for Textwrap
        # Textwrap_count for PDF height
        for ean13, item_info in item_dict.items():
            if item_info["price_kg"] is not None:
                item_text = f"{item_info['count']}x - {item_info['name']} ({item_info['kg']:.2f} kg)"
            else:
                item_text = f"{item_info['count']}x - {item_info['name']}"

            textwrap_count += 1 if len(item_text) > max_name_length else 0

        # Calculate total height based on the number of items
        total_height = height + (len(item_dict) * 10 * mm) + (textwrap_count * 3 * mm)

        # Add custom content to the bill
        c = canvas.Canvas(pdf_filename, pagesize=(width, total_height))
        c.setFont("Helvetica-Bold", 20)  # Set font to bold and larger size
        c.drawCentredString(width / 2, total_height - 10 * mm, "Foodinni")  # Centered "Foodinni" text
        c.setFont("Helvetica", 10)  # Reset font to regular size

        # Add URL and date, centered
        url = "https://foodinni.mimil-grp.eu/"
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M")
        total_height -= 16 * mm  # Adjust height
        c.drawCentredString(width / 2, total_height, url)
        total_height -= 7 * mm  # Adjust height
        c.drawCentredString(width / 2, total_height, f"{current_datetime}")

        # Increase space before the first list item
        total_height -= 10 * mm

        # Iterate through the item_dict and print each item
        line_height = 15  # Adjust line height
        total_price = 00.00
        for ean13, item_info in item_dict.items():
            if item_info["price_kg"] is not None:
                price = item_info["price_kg"] * item_info["kg"]
                item_text = f"{item_info['count']}x - {item_info['name']} ({item_info['kg']:.2f} kg)"
            else:
                price = item_info["price"] * item_info["count"]
                item_text = f"{item_info['count']}x - {item_info['name']}"

            total_price += price

            # Split long item names into multiple lines if needed
            if len(item_text) > max_name_length:
                item_lines = textwrap.wrap(item_text, width=max_name_length)
                for line in item_lines:
                    total_height -= line_height  # Adjust height
                    c.setFont("Helvetica", 10)
                    c.drawString(10 * mm, total_height, line)
            else:
                total_height -= line_height  # Adjust height
                c.setFont("Helvetica", 10)
                c.drawString(10 * mm, total_height, item_text)

            # Increase space between items
            total_height -= 3 * mm

            # Print prices on the right
            c.setFont("Helvetica-Bold", 10)
            c.drawRightString(width - 5 * mm, total_height - 1 * mm, f"{price:.2f} €")

        # Print the total price
        c.setFont("Helvetica-Bold", 20)
        total_height -= 20 * mm  # Adjust height
        c.drawString(10 * mm, total_height, f"Total:")
        c.drawRightString(width - 5 * mm, total_height, f"{total_price:.2f} €")

        # Add customer and cashier names
        c.setFont("Helvetica", 10)
        total_height -= 7 * mm  # Adjust height
        c.drawString(10 * mm, total_height, f"Cashier: {login.username.get()}")
        total_height -= 7 * mm  # Adjust height
        c.drawString(10 * mm, total_height, f"Customer: {customer_identifier}")

        # Save the PDF
        c.save()

        # Clear customer name, price and item list after generating PDF
        customeruser_label.config(text="Unknown")
        item_dict.clear()
        tree.delete(*tree.get_children())
        price_var.set("00.00")
        customer_identifier = "Unknown"

        print(f"PDF saved as: {pdf_filename}")
    except Exception as e:
        print(f"Error saving PDF: {e}")

# Create a root window
root = tk.Tk()
root.title("Foodinni Cashier")
root.geometry("670x500")

# Create a frame for the groceries barcode and customer card input field and the labels
input_frame = tk.LabelFrame(root, text= "Customer and Cashier Inputs", width= 650, height= 120)
input_frame.grid(row=0, column=0, padx = 10, pady = 10)

input_frame.grid_propagate(0)

# Create a label for the groceries input field
input_label = tk.Label(input_frame, text="Barcode")
input_label.grid(row=0, column=0, padx = 10, pady = 5, sticky = 'w')

# Create a groceries input field
input_var = tk.StringVar()
input_groceries = tk.Entry(input_frame, width = 17, textvariable=input_var)
input_groceries.grid(row=1, column=0, padx = 13, pady = 5, sticky = 'w')

# Create a groceries add button
customer_button = tk.Button(input_frame, text="Add Groceries", height = 1, width = 29, command= add_item)
customer_button.grid(row=2, column=0, columnspan = 3,  padx = 13, pady = 5, sticky = 'w')

# Create a label for the groceries Nr input field
nr_label = tk.Label(input_frame, text="Nr")
nr_label.grid(row=0, column=1, pady = 5, sticky = 'w')

# Create a groceries Nr input field
nr_var = tk.StringVar()
nr_field = tk.Entry(input_frame, width = 5, textvariable=nr_var)
nr_field.grid(row=1, column=1, pady = 5, sticky = 'w')
nr_field.insert(0, "1")

# Create a label for the groceries Kg input field
kg_label = tk.Label(input_frame, text="Kg")
kg_label.grid(row=0, column=2, pady = 5, sticky = 'w')


# Create a groceries Kg input field
kg_var = tk.StringVar()
kg_field = tk.Entry(input_frame, width = 5, textvariable=kg_var)
kg_field.grid(row=1, column=2, pady = 5, sticky = 'w')
kg_field.insert(0, "1")


# Create a label for the customer input field
input_label = tk.Label(input_frame, text="Customer Name")
input_label.grid(row=0, column=3, padx = 10, pady = 5, sticky = 'w')

# Create a customer input field
customer_var = tk.StringVar()
input_field = tk.Entry(input_frame, textvariable=customer_var)
input_field.grid(row=1, column=3, padx = 13, pady = 5, sticky = 'w')

# Create a customer add button
customer_button = tk.Button(input_frame, text="Add Customer", height = 1, width = 16, command = add_customer)
customer_button.grid(row=2, column=3, padx = 13, pady = 5, sticky = 'w')






# Create a label to display the cashier identifier
cashier_label = tk.Label(input_frame, text="Cashier:")
cashier_label.grid(row=0, column=4, padx = 10, pady = 5, sticky = 'w')

# Create a label to display the customer identifier
customer_label = tk.Label(input_frame, text="Customer:")
customer_label.grid(row=1, column=4, padx = 10, pady = 5, sticky = 'w')

# Create a label to display the cashier identifier
# from login import username
canvas_frame = tk.Canvas(input_frame, width=80, height= 10 )
canvas_frame.grid(row = 0, column = 5)

cashieruser_label = tk.Label(input_frame, text= f"{login.username.get()}")
cashieruser_label.grid(row=0, column=5, padx = 10, pady = 5, sticky = 'w')

# Create a label to display the customer identifier
customeruser_label = tk.Label(input_frame, text="Unknown")
customeruser_label.grid(row=1, column=5, padx = 10, pady = 5, sticky = 'w')

cashier_button = tk.Button(input_frame, text="Logout", height = 1, width = 8, command = logout)
cashier_button.grid(row=0, column=6, padx = 20)

cashier_button = tk.Button(input_frame, text="Remove", height = 1, width = 8, command = remove_item)
cashier_button.grid(row=2, column=6, padx = 20)



# Create a LabelFrame for the table
table_frame = tk.LabelFrame(root, text="Added Products", width=650, height=300)
table_frame.grid(row=1, column=0, padx = 10, pady = 10)

#table_frame.grid_propagate(0)

tree = ttk.Treeview(table_frame, columns=("Count", "Name", "Price", "per kg", "Kg", "Total"))
tree.heading("#1", text="Count")
tree.heading("#2", text="Name")
tree.heading("#3", text="Price")
tree.heading("#4", text="per Kg")
tree.heading("#5", text="Kg")
tree.heading("#6", text="Total")

# Set column widths (adjust the values as needed)
tree.column("#0", width=0)
tree.column("#1", width=70)   # Count column
tree.column("#2", width=275)  # Name column
tree.column("#3", width=70)   # Price column
tree.column("#4", width=70)   # per kg column
tree.column("#5", width=60)   # kg column
tree.column("#6", width=100)   # Total column
tree.pack()



# Create a frame for the price and the label
price_frame = tk.LabelFrame(root, text = "Price and Payment", width=650, height=75)
price_frame.grid(row=3, column=0, padx = 10, pady = 10)

price_frame.grid_propagate(0)

# Create a label for the price
price_label = tk.Label(price_frame, text="Price")
price_label.grid(row = 0, column=0, padx = 10, pady = 10)

# Create a variable for the price
price_var = tk.DoubleVar()
price_var.set(00.00)

# Create a label to display the price
canvas_frame = tk.Canvas(price_frame, width=100, height=50 )
canvas_frame.grid(row = 0, column = 1)
price_display = tk.Label(price_frame, textvariable=price_var, font=("Arial", 20))
price_display.grid(row = 0, column=1, padx = 10, pady = 10)

canvas_frame = tk.Canvas(price_frame, width=280, height=50 )
canvas_frame.grid(row = 0, column = 2)

# Create a button for cash payment
#cash_button = tk.Button(price_frame, text="Cash", height = 2, width = 10)
#cash_button.grid(row=0, column=3, padx = 5, pady= 5, sticky="n")

# Create a button for card payment
#card_button = tk.Button(price_frame, text="Card", height = 2, width = 10)
#card_button.grid(row=0, column=4, padx = 5, pady= 5, sticky="n")

#Create a button for Payment
pay_button = tk.Button(price_frame, text="Pay", height = 1, width = 15, font=("Arial", 15), command=generate_pdf)
pay_button.grid(row=0, column=3, padx = 5, pady= 5, sticky="n")


root.mainloop()
