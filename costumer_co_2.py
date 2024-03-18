import requests


def check_customer_existence(customer_name):
    api_url = "https://api.mimil-grp.eu/foodinni/customer/getCustomer.php"
    params = {"customer_name": customer_name}

    response = requests.get(api_url, params=params)

    if response.status_code == 200:
        data = response.json()
        if data.get("success"):
            return f"Der Kunde '{customer_name}' existiert."
        else:
            return f"Der Kunde '{customer_name}' existiert nicht."
    else:
        return f"Fehler beim Überprüfen der Kundenexistenz. Statuscode: {response.status_code}"


# Überprüfe, ob 'emilien' als Kunde existiert
customer_name_to_check = "peter"
result = check_customer_existence(customer_name_to_check)
result
