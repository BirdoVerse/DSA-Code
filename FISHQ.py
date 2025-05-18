from datetime import datetime, timedelta

# -------------------------
# INVENTORY SECTION
# -------------------------

# Create a seafood item as a dictionary
def create_item(id, name, qty, date_received, expiry_date):
    return {
        "id": id,
        "name": name,
        "qty": qty,
        "date_received": date_received,
        "expiry_date": expiry_date
    }

# Manually update quantity
def update_item_quantity(inventory, id, new_qty):
    for item in inventory:
        if item["id"] == id:
            item["qty"] = new_qty
            return True
    return False

# Remove all expired items from inventory
def remove_expired_items(inventory, today):
    removed = []
    i = 0
    while i < len(inventory):
        if inventory[i]["expiry_date"] < today:
            removed.append(inventory.pop(i))
        else:
            i += 1
    return removed

# Get item by ID
def find_by_id(inventory, id):
    for item in inventory:
        if item["id"] == id:
            return item
    return None

# -------------------------
# REPORTING SECTION
# -------------------------

def search_items(inventory, name, today):
    name = name.lower()
    results = []
    for item in inventory:
        if item["name"].lower() == name:
            results.append(item)
    return results

def check_alerts(inventory, today):
    alerts = []
    for item in inventory:
        if item["qty"] < 5 or item["expiry_date"] < today:
            alerts.append(item)
    return alerts

def sort_inventory(inventory, key):
    n = len(inventory)
    for i in range(n):
        for j in range(i + 1, n):
            if inventory[i][key] > inventory[j][key]:
                inventory[i], inventory[j] = inventory[j], inventory[i]
    return inventory

# -------------------------
# MAIN PROGRAM SECTION
# -------------------------

inventory = []

def ask_date(prompt):
    while True:
        try:
            return datetime.strptime(input(prompt + " (YYYY-MM-DD): "), "%Y-%m-%d")
        except ValueError:
            print("Invalid date format.")

def get_int(prompt):
    while True:
        try:
            val = int(input(prompt))
            if val >= 0:
                return val
        except:
            pass
        print("Enter a valid non-negative number.")

def print_item(item, today):
    status = "EXPIRED" if item["expiry_date"] < today else "FRESH"
    print(f"{item['id']} | {item['name']} | Qty: {item['qty']} | Received: {item['date_received'].date()} | {status}")

def main():
    today = ask_date("Enter today's date")
    while True:
        print("==================================================")
        print("||\t\t   F.I.S.H.Q. MENU\t\t|| ")
        print("||==============================================||")
        print("||\t\t0) Set Current Date\t\t||")
        print("||\t\t1) Add Seafood\t\t\t||")
        print("||\t\t2) View Inventory\t\t||")
        print("||\t\t3) Update Quantity\t\t||")
        print("||\t\t4) Remove Expired\t\t||")
        print("||\t\t5) Search Seafood\t\t||")
        print("||\t\t6) View Alerts\t\t\t||")
        print("||\t\t7) Sort Inventory\t\t||")
        print("||\t\t8) View Summary\t\t\t||")
        print("||\t\t9) Exit\t\t\t\t||")
        print("==================================================")
        choice = input("Select option (0–9): ")

        if choice == "0":
            today = ask_date("Set current date")

        elif choice == "1":
            id = input("Seafood ID: ")

            while True:
                name = input("Name (ONLY CAPITAL LETTERS): ")
                if name.isalpha() and name.isupper():
                    break
                else:
                    print("Invalid input. Use only capital letters (A–Z), no numbers or symbols.")

            qty = get_int("Quantity: ")
            received = ask_date("Date received")
            expiry = ask_date("Expiry date")

            item = create_item(id, name, qty, received, expiry)
            inventory.append(item)
            print("Item added.")

        elif choice == "2":
            if not inventory:
                print("Inventory is empty.")
            else:
                for item in inventory:
                    print_item(item, today)

        elif choice == "3":
            id = input("Enter ID to update: ")
            qty = get_int("New quantity: ")
            if update_item_quantity(inventory, id, qty):
                print("Quantity updated.")
            else:
                print("Item not found.")

        elif choice == "4":
            removed = remove_expired_items(inventory, today)
            if removed:
                for item in removed:
                    print(f"Removed expired: {item['name']} (Expired on: {item['expiry_date'].date()})")
            else:
                print("No expired items to remove.")

        elif choice == "5":
            name = input("Search name: ")
            results = search_items(inventory, name, today)
            if results:
                for item in results:
                    print_item(item, today)
            else:
                print("Not found.")

        elif choice == "6":
            alerts = check_alerts(inventory, today)
            if alerts:
                print("ALERTS:")
                for item in alerts:
                    reasons = []
                    if item["qty"] < 5:
                        reasons.append("Low Quantity")
                    if item["expiry_date"] < today:
                        reasons.append(f"Expired on {item['expiry_date'].date()}")
                    reason_str = " | ".join(reasons)
                    print(f"{item['name']} - Qty: {item['qty']} - {reason_str}")
            else:
                print("No alerts.")

        elif choice == "7":
            print("Sort by: name | qty | date_received")
            field = input("Field: ").strip()
            if field in ["name", "qty", "date_received"]:
                inventory[:] = sort_inventory(inventory, field)
                print("Inventory sorted by", field + ".")
            else:
                print("Invalid field.")

        elif choice == "8":
            id = input("Enter ID: ")
            item = find_by_id(inventory, id)
            if item:
                print_item(item, today)
            else:
                print("Not found.")

        elif choice == "9":
            print("Exiting program.")
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()
