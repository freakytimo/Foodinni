import tkinter as tk

# Create a function to add a customer
def add_customer():
    customer_name = input_var.get()
    customeruser_label.config(text=customer_name)

# Create a function to logout
def logout():
    cashieruser_label.config(text="Unknown")
    customeruser_label.config(text="Unknown")

# Create the main Tkinter window
root = tk.Tk()
root.title("Cashier System")

# Create a frame for input widgets
input_frame = tk.Frame(root)
input_frame.pack(padx=20, pady=20)

# Create a label for the customer input field
input_label = tk.Label(input_frame, text="Customer number/card")
input_label.grid(row=0, column=1, padx=10, pady=5, sticky='w')

# Create a customer input field
input_var = tk.StringVar()
input_field = tk.Entry(input_frame, textvariable=input_var)
input_field.grid(row=1, column=1, padx=13, pady=5, sticky='w')

# Create a customer add button
customer_button = tk.Button(input_frame, text="Add Customer", height=1, width=16, command=add_customer)
customer_button.grid(row=2, column=1, padx=13, pady=5, sticky='w')

# Create a label to display the cashier identifier
cashier_label = tk.Label(input_frame, text="Cashier:")
cashier_label.grid(row=0, column=3, padx=10, pady=5, sticky='w')

# Create a label to display the customer identifier
customer_label = tk.Label(input_frame, text="Customer:")
customer_label.grid(row=1, column=3, padx=10, pady=5, sticky='w')

# Create a label to display the cashier identifier
# from login import username
cashieruser_label = tk.Label(input_frame, text=f"{"Cashier"}")
cashieruser_label.grid(row=0, column=4, padx=10, pady=5, sticky='w')

# Create a label to display the customer identifier
customeruser_label = tk.Label(input_frame, text="Unknown")
customeruser_label.grid(row=1, column=4, padx=10, pady=5, sticky='w')

# Create a logout button
cashier_button = tk.Button(input_frame, text="Logout", height=1, width=8, command=logout)
cashier_button.grid(row=0, column=5, padx=20)

# Run the Tkinter event loop
root.mainloop()