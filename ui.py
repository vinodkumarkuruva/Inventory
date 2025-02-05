import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog,QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout, QLineEdit, QMessageBox

class InventoryApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Inventory Management")
        self.setGeometry(100, 100, 600, 400)

        self.layout = QVBoxLayout()

        # Inventory Table
        self.inventory_table = QTableWidget()
        self.inventory_table.setColumnCount(6)  # Name, Quantity, Buy, Return, Remove
        self.inventory_table.setHorizontalHeaderLabels(["Item", "Quantity", "Buy", "Return", "Remove","Update"])

        self.layout.addWidget(self.inventory_table)

        # Add Item Inputs
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter Item Name")
        self.quantity_input = QLineEdit()
        self.quantity_input.setPlaceholderText("Enter Quantity")
        self.add_button = QPushButton("Add Item")
        self.add_button.clicked.connect(self.add_item)

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.name_input)
        input_layout.addWidget(self.quantity_input)
        input_layout.addWidget(self.add_button)
        self.layout.addLayout(input_layout)

        # Refresh Button
        # self.refresh_button = QPushButton("Refresh Inventory")
        # self.refresh_button.clicked.connect(self.fetch_inventory)
        # self.layout.addWidget(self.refresh_button)

        self.setLayout(self.layout)
        self.fetch_inventory()  # Load inventory on startup

    def fetch_inventory(self):
        """Fetch inventory from the backend"""
        response = requests.get("http://127.0.0.1:5000/inventory")
        if response.status_code == 200:
            self.display_inventory(response.json())
        else:
            self.show_error_message("Error fetching inventory", response.json().get("error"))

    def display_inventory(self, data):
        """Display inventory in the UI"""
        self.inventory_table.setRowCount(len(data))

        for row, (item, quantity) in enumerate(data.items()):
            self.inventory_table.setItem(row, 0, QTableWidgetItem(item))
            self.inventory_table.setItem(row, 1, QTableWidgetItem(str(quantity)))

            # Buy Button
            buy_button = QPushButton("Buy")
            buy_button.clicked.connect(lambda _, i=item: self.buy_item(i))
            self.inventory_table.setCellWidget(row, 2, buy_button)

            # Return Button
            return_button = QPushButton("Return")
            return_button.clicked.connect(lambda _, i=item: self.return_item(i))
            self.inventory_table.setCellWidget(row, 3, return_button)

            # Remove Button
            remove_button = QPushButton("Remove")
            remove_button.clicked.connect(lambda _, i=item: self.remove_item(i))
            self.inventory_table.setCellWidget(row, 4, remove_button)

            # Update Button (New button)
            update_button = QPushButton("Update")
            update_button.clicked.connect(lambda _, i=item: self.update_item(i))
            self.inventory_table.setCellWidget(row, 5, update_button)  # Adding Update button in the last column

    def update_item(self, item_name):
        """Update the quantity of an item in the inventory"""
        new_quantity, ok = QInputDialog.getInt(self, "Update Item Quantity", f"Enter new quantity for {item_name}:")

        if ok:
            response = requests.post("http://127.0.0.1:5000/update-quantity", json={"name": item_name, "quantity": new_quantity})
            if response.status_code == 200:
                self.fetch_inventory()
            else:
                self.show_error_message("Error updating item", response.json().get("error"))


    def buy_item(self, item_name):
        """Buy an item (decrease quantity)"""
        response = requests.post("http://127.0.0.1:5000/buy-item", json={"name": item_name})
        if response.status_code == 200:
            self.fetch_inventory()
        else:
            self.show_error_message("Error buying item", response.json().get("error"))

    def return_item(self, item_name):
        """Return an item (increase quantity)"""
        response = requests.post("http://127.0.0.1:5000/return-item", json={"name": item_name})
        if response.status_code == 200:
            self.fetch_inventory()
        else:
            self.show_error_message("Error returning item", response.json().get("error"))

    def remove_item(self, item_name):
        """Remove an item from the inventory"""
        response = requests.post("http://127.0.0.1:5000/remove-item", json={"name": item_name})
        if response.status_code == 200:
            self.fetch_inventory()
        else:
            self.show_error_message("Error removing item", response.json().get("error"))

    def add_item(self):
        """Add a new item to the inventory"""
        name = self.name_input.text()
        quantity = self.quantity_input.text()

        if not name or not quantity.isdigit():
            self.show_error_message("Invalid input", "Please provide valid item name and quantity.")
            return

        response = requests.post("http://127.0.0.1:5000/add-item", json={"name": name, "quantity": int(quantity)})
        if response.status_code == 200:
            self.fetch_inventory()
            self.name_input.clear()
            self.quantity_input.clear()
        else:
            self.show_error_message("Error adding item", response.json().get("error"))



    def show_error_message(self, title, message):
        """Display error message in a pop-up"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = InventoryApp()
    window.show()
    sys.exit(app.exec_())
