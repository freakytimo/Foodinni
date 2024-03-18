import tkinter as tk
import requests
import base64

# Funktion zum Hinzufügen eines Kunden
def add_customer():
    #customer_name = input_var.get()

    # API aufrufen, um zu überprüfen, ob der Kunde existiert
    api_url = "https://api.mimil-grp.eu/foodinni/customer/getCustomer.php"
    encoded_customer = base64.b64encode(f"{input_var.get()}".encode())
    headers = {"Authorization": f"Basic {encoded_customer}"}
    #headers = {"customer_name": encoded_customer}
    response = requests.get(api_url, headers = headers)


    if response.status_code == 200:
        # Kunde existiert, Label aktualisieren
        customeruser_label.config(text=input_var.get())
        print(response.status_code, headers)
    else:
        # Kunde existiert nicht, Label als "Unknown" belassen und das Eingabefeld leeren
        input_var.set("")
        input_field.delete(0, tk.END)
        print(response.status_code, headers)


# Funktion zum Ausloggen
def logout():
    cashieruser_label.config(text="Unknown")
    customeruser_label.config(text="Unknown")


# Hauptfenster von Tkinter erstellen
root = tk.Tk()
root.title("Kassensystem")

# Rahmen für Eingabewidgets erstellen
input_frame = tk.Frame(root)
input_frame.pack(padx=20, pady=20)

# Label für das Kunden-Eingabefeld erstellen
input_label = tk.Label(input_frame, text="Kundennummer/Karte")
input_label.grid(row=0, column=1, padx=10, pady=5, sticky='w')

# Kunden-Eingabefeld erstellen
input_var = tk.StringVar()
input_field = tk.Entry(input_frame, textvariable=input_var)
input_field.grid(row=1, column=1, padx=13, pady=5, sticky='w')

# Kunden-Button erstellen
customer_button = tk.Button(input_frame, text="Kunde hinzufügen", height=1, width=16, command=add_customer)
customer_button.grid(row=2, column=1, padx=13, pady=5, sticky='w')

# Label für die Kassierer-Kennung erstellen
cashier_label = tk.Label(input_frame, text="Kassierer:")
cashier_label.grid(row=0, column=3, padx=10, pady=5, sticky='w')

# Label für die Kunden-Kennung erstellen
customer_label = tk.Label(input_frame, text="Kunde:")
customer_label.grid(row=1, column=3, padx=10, pady=5, sticky='w')

# Label für die Kassierer-Kennung erstellen
# aus login import username
cashieruser_label = tk.Label(input_frame, text="timo")
cashieruser_label.grid(row=0, column=4, padx=10, pady=5, sticky='w')

# Label für die Kunden-Kennung erstellen
customeruser_label = tk.Label(input_frame, text="Unknown")
customeruser_label.grid(row=1, column=4, padx=10, pady=5, sticky='w')

# Logout-Button erstellen
cashier_button = tk.Button(input_frame, text="Ausloggen", height=1, width=8, command=logout)
cashier_button.grid(row=0, column=5, padx=20)

# Tkinter-Ereignisschleife ausführen
root.mainloop()
