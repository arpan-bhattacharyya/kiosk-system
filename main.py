import csv
import matplotlib.pyplot as plt
import os

class Menu:
    def __init__(self):
        self.items = {
            'Starters': {
                'pizza': 250,
                'pasta': 200,
                'burger': 150,
                'sandwiches': 70,
                'french fries': 100,
                'salad': 100,
                'taco': 110,
                'spring rolls': 130,
                'noodles': 150
            },
            'Drinks': {
                'hot coffee': 90, 
                'cold coffee': 100,
                'iced tea': 80,
                'milkshake': 100,
                'mocktails': 120,
                'beverages': 40
            },
            'Desserts': {
                'brownie': 90,
                'cheesecake': 160,
                'pastry': 75
            }
        }

    def display_menu(self):
        print("Welcome to Cafe Haven")
        for category, items in self.items.items():
            print(f"\n--- {category} ---")
            for item, price in items.items():
                print(f"{item.title()}: {price}")

    def get_price(self, item):
        item = item.lower()
        for category in self.items.values():
            if item in category:
                return category[item]
        return None


class CustomerOrder(Menu):
    def __init__(self, customer_name):
        super().__init__()
        self.customer_name = customer_name
        self.order_list = []
        self.subtotal = 0
        self.discount = 0
        self.total = 0

    def add_item(self, item, qty):
        price = self.get_price(item)
        if price:
            item_total = price * qty
            self.subtotal += item_total
            self.order_list.append((item.title(), qty, item_total))
            print(f"{qty} x {item.title()} has been ordered, total: {item_total}")
        else:
            print(f"{item.title()} is not available")

    def calculate_discount(self):
        if self.subtotal > 500:
            self.discount = 0.1 * self.subtotal
        elif self.subtotal > 300:
            self.discount = 0.05 * self.subtotal
        self.total = self.subtotal - self.discount

    def display_order_summary(self):
        print(f"\n--- Total Bill for {self.customer_name} ---")
        for item, qty, item_total in self.order_list:
            print(f"- {qty} x {item}: {item_total}")
        print(f"\nSubtotal: {self.subtotal}")
        print(f"Discount: {self.discount}")
        print(f"Total after discount: {self.total}")
        print("Thank You for ordering with us, visit again !!")
        return self.total


class CafeSystem:
    def __init__(self):
        self.menu = Menu()
        self.customer_orders = {}

    def take_order(self, customer_name):
        customer_order = CustomerOrder(customer_name)
        print(f"\nTaking order for {customer_name}:")

        while True:
            entry = input("\nEnter the name of the dish and quantity separated by a comma (or type 'done' to finish): ")
            if entry.lower() == 'done':
                break
            item, qty = entry.split(",")
            qty = int(qty.strip())
            customer_order.add_item(item.strip(), qty)

        customer_order.calculate_discount()
        self.customer_orders[customer_name] = customer_order
        total = customer_order.display_order_summary()

        # Save order to CSV
        self.save_order_to_csv(customer_name, customer_order)

        # Conduct a survey
        self.conduct_survey(customer_name)

    def save_order_to_csv(self, customer_name, customer_order):
        filename = "orders.csv"
        # Check if the file exists and is empty to add headers
        file_exists = os.path.isfile(filename)
        with open(filename, mode="a", newline="") as file:
            writer = csv.writer(file)
            if not file_exists or os.path.getsize(filename) == 0:
                writer.writerow(["Customer Name", "Item", "Quantity", "Item Total", "Subtotal", "Discount", "Total"])
            for item, qty, item_total in customer_order.order_list:
                writer.writerow([customer_name, item, qty, item_total, customer_order.subtotal, customer_order.discount, customer_order.total])

    def conduct_survey(self, customer_name):
        filename = "survey.csv"
        file_exists = os.path.isfile(filename)
        feedback = input("How would you rate your experience (1-5)? ")
        recommend = input("Would you recommend us to others? (yes/no): ")

        with open(filename, mode="a", newline="") as file:
            writer = csv.writer(file)
            if not file_exists or os.path.getsize(filename) == 0:
                writer.writerow(["Customer Name", "Feedback", "Recommend"])
            writer.writerow([customer_name, feedback, recommend])
        print("Thank you for your feedback!")

    def display_all_orders(self):
        for customer_name, order in self.customer_orders.items():
            order.display_order_summary()

    def average_spent_per_customer(self):
        # Read the data from the CSV file
        customer_totals = {}

        with open("orders.csv", mode="r") as file:
            reader = csv.reader(file)
            next(reader)  # Skip header if present
            for row in reader:
                customer_name = row[0]
                total_spent = float(row[6])  # Assuming 'total' is in the 7th column (index 6)
                
                # Add to the customer's total spent (accumulating if customer ordered multiple times)
                if customer_name in customer_totals:
                    customer_totals[customer_name] += total_spent
                else:
                    customer_totals[customer_name] = total_spent

        # Check if there are any orders
        if not customer_totals:
            print("No orders to calculate average.")
            return

        # Calculate the average spent per customer
        average_spent = sum(customer_totals.values()) / len(customer_totals)
        print(f"\nAverage amount spent per customer: {average_spent:.2f}")

        # Plot the data
        names = list(customer_totals.keys())
        spends = list(customer_totals.values())

        plt.figure(figsize=(10, 5))
        plt.bar(names, spends, color='skyblue')
        plt.xlabel("Customers")
        plt.ylabel("Total Spent (after discount)")
        plt.title("Total Amount Spent by Each Customer")
        plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels if necessary
        plt.tight_layout()  # Adjust layout to avoid clipping of labels
        plt.show()


# Main code to use the system
cafe_system = CafeSystem()
cafe_system.menu.display_menu()

# Take orders for multiple customers and display each total bill immediately
while True:
    customer_name = input("\nEnter the customer's name (type 'done' to finish): ")
    if customer_name.lower() == 'done':
        break
    cafe_system.take_order(customer_name)

# Display average spending after all orders
cafe_system.average_spent_per_customer()
