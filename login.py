import tkinter as tk
from functools import partial
import requests
import base64
import hashlib

def validate_login(username, password):
    #URL
    api_url = "https://api.mimil-grp.eu/foodinni/cashier/getCashier.php"

    # MD5 hash the password
    hashed_password = hashlib.md5(password.get().encode()).hexdigest()

    # Encode the credentials (username:hashed_password) in Base64
    encoded_credentials = base64.b64encode(f"{username.get()}:{hashed_password}".encode()).decode()

    headers = {"Authorization": f"Basic {encoded_credentials}"}
    #payload = {"basic": username.get(), "identifier": password.get()}

    try:
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            print("Erfolgreich eingeloggt!")
            main_window.destroy()  # Schließe das Fenster bei erfolgreichem Login
        else:
            print("Fehler: Ungültige Anmeldedaten")
            print(response.status_code, username.get(), password.get(), headers)
            # Zeige eine Fehlermeldung unter dem Login-Button an (z. B. mit einem Label)
            # Lösche das vorhandene Label, falls es bereits existiert
            for widget in main_window.winfo_children():
                if isinstance(widget, tk.Label) and (widget.cget("text") == "Error: No API Connection" or widget.cget(
                        "text") == "Error: Wrong Login Data"):
                    widget.destroy()
            Error_Data = tk.Label(main_window, text="Error: Wrong Login Data", font=("Calibri", 14), fg="red").pack()

            # Clear the input fields
            username_entry.delete(0, tk.END)
            password_entry.delete(0, tk.END)

    except requests.RequestException:
        print("Fehler: Verbindung zur API nicht möglich")
        # Zeige eine Fehlermeldung unter dem Login-Button an (z. B. mit einem Label)
        # Lösche das vorhandene Label, falls es bereits existiert
        for widget in main_window.winfo_children():
            if isinstance(widget, tk.Label) and (widget.cget("text") == "Error: No API Connection" or widget.cget("text") == "Error: Wrong Login Data") :
                widget.destroy()
        Error_Api = tk.Label(main_window, text="Error: No API Connection", font=("Calibri", 14), fg="red").pack()



# Erstelle das Hauptfenster
main_window = tk.Tk()
main_window.geometry("300x200")
main_window.title("Login")

# Erstelle ein Label und ein Entry-Feld für den Benutzernamen
tk.Label(main_window, text="Username", font=("Calibri", 14)).pack()
username = tk.StringVar()
username_entry = tk.Entry(main_window, textvariable=username, font=("Calibri", 14))
username_entry.pack()

# Erstelle ein Label und ein Entry-Feld für das Passwort
tk.Label(main_window, text="Password", font=("Calibri", 14)).pack()
password = tk.StringVar()
password_entry = tk.Entry(main_window, textvariable=password, show="*", font=("Calibri", 14))
password_entry.pack()

# Erstelle einen Button zum Einloggen
validate_login = partial(validate_login, username, password)
tk.Button(main_window, text="Login", command=validate_login, font=("Calibri", 14)).pack(pady = 10)



# Starte die Hauptloop
main_window.mainloop()
