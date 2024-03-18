import tkinter as tk
import login
import subprocess




def logout():
    # Close the entire tkinter window
    root.destroy()
    subprocess.Popen(["python", "gui.py"])


# Create a root window
root = tk.Tk()
root.title("Foodinni Cashier")
root.geometry("620x560")

# Create a frame for the groceries barcode and customer card input field and the labels
input_frame = tk.LabelFrame(root, text= "Customer and Cashier Inputs", width= 600, height= 120)
input_frame.grid(row=0, column=0, padx = 10, pady = 10)

input_frame.grid_propagate(0)

# Create a label for the groceries input field
input_label = tk.Label(input_frame, text="Groceries number/barcode")
input_label.grid(row=0, column=0, padx = 10, pady = 5, sticky = 'w')

# Create a groceries input field
input_var = tk.StringVar()
input_field = tk.Entry(input_frame, textvariable=input_var)
input_field.grid(row=1, column=0, padx = 13, pady = 5, sticky = 'w')

# Create a groceries add button
customer_button = tk.Button(input_frame, text="Add Groceries", height = 1, width = 16)
customer_button.grid(row=2, column=0, padx = 13, pady = 5, sticky = 'w')


# Create a label for the customer input field
input_label = tk.Label(input_frame, text="Customer number/card")
input_label.grid(row=0, column=1, padx = 10, pady = 5, sticky = 'w')

# Create a customer input field
input_var = tk.StringVar()
input_field = tk.Entry(input_frame, textvariable=input_var)
input_field.grid(row=1, column=1, padx = 13, pady = 5, sticky = 'w')

# Create a customer add button
customer_button = tk.Button(input_frame, text="Add Customer", height = 1, width = 16, command = addcostumer)
customer_button.grid(row=2, column=1, padx = 13, pady = 5, sticky = 'w')




# Create a label to display the cashier identifier
cashier_label = tk.Label(input_frame, text="Cashier:")
cashier_label.grid(row=0, column=3, padx = 10, pady = 5, sticky = 'w')

# Create a label to display the customer identifier
customer_label = tk.Label(input_frame, text="Customer:")
customer_label.grid(row=1, column=3, padx = 10, pady = 5, sticky = 'w')

# Create a label to display the cashier identifier
# from login import username
cashieruser_label = tk.Label(input_frame, text= f"{login.username.get()}")
cashieruser_label.grid(row=0, column=4, padx = 10, pady = 5, sticky = 'w')

# Create a label to display the customer identifier
customeruser_label = tk.Label(input_frame, text="Unknown")
customeruser_label.grid(row=1, column=4, padx = 10, pady = 5, sticky = 'w')

cashier_button = tk.Button(input_frame, text="Logout", height = 1, width = 8, command = logout)
cashier_button.grid(row=0, column=5, padx = 20)



# Create a LabelFrame for the table
table_frame = tk.LabelFrame(root, text="Added Products", width=600, height=300)
table_frame.grid(row=1, column=0, padx = 10, pady = 10)

table_frame.grid_propagate(0)


# Create a frame for the price and the label
price_frame = tk.LabelFrame(root, text = "Price and Payment", width=600, height=75)
price_frame.grid(row=3, column=0, padx = 10, pady = 10)

price_frame.grid_propagate(0)

# Create a label for the price
price_label = tk.Label(price_frame, text="Price")
price_label.grid(row = 0, column=0, padx = 10, pady = 10)

# Create a variable for the price
price_var = tk.DoubleVar()
price_var.set(0.0)

# Create a label to display the price
price_display = tk.Label(price_frame, textvariable=price_var, font=("Arial", 20))
price_display.grid(row = 0, column=1, padx = 10, pady = 10)

canvas = tk.Canvas(price_frame, width=280, height=50 )
canvas.grid(row = 0, column = 2)

# Create a button for cash payment
cash_button = tk.Button(price_frame, text="Cash", height = 2, width = 10)
cash_button.grid(row=0, column=3, padx = 5, pady= 5, sticky="n")

# Create a button for card payment
card_button = tk.Button(price_frame, text="Card", height = 2, width = 10)
card_button.grid(row=0, column=4, padx = 5, pady= 5, sticky="n")




root.mainloop()
