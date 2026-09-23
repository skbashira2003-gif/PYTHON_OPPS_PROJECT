#  Virtual Queue Tracking System Using Python OOP and CSV

# Project Name: Reliance Electronics & Appliances Service Desk

# Project Description:
# A menu-driven Virtual Queue Tracking System developed using
# Python Object-Oriented Programming (OOP) and CSV file handling.
# It helps manage customer tokens, service queues, delayed services,
# completed services, and customer feedback.

# Concepts Used:
# 1. Classes and Objects
# 2. Constructors (__init__)
# 3. Instance Methods
# 4. Static Methods
# 5. Dictionaries
# 6. Lists and Loops
# 7. Conditional Statements
# 8. Exception-Free Input Validation
# 9. CSV File Handling
# 10. File Handling (Read, Write, Append)
# 11. Date and Time Handling
# 12. Functions and Methods

# Project Features:
# 1. Add Customer and Generate Token
# 2. View Active Queue
# 3. Track Customer Queue Position
# 4. Call Next Customer
# 5. Complete Service and Collect Feedback
# 6. Mark Service as Delayed / Incomplete
# 7. Resume Delayed Service
# 8. Search Customer Details
# 9. Display Served Customers
# 10. Exit the Application

# CSV Files:
# 1. queue_data.csv - Stores customer and queue details
# 2. feedback_data.csv - Stores customer feedback

# Developed By: shaik Basheerunnisa

import csv
import os
from datetime import datetime

FILE_NAME = "queue_data.csv"
FEEDBACK_FILE = "feedback_data.csv"

QUEUE_FIELDS = [
    "Token", "Name", "Service", "Time", "Status", "Delay Reason"
]

FEEDBACK_FIELDS = [
    "Token", "Name", "Rating", "Comment", "Submitted At"
]

STORE_NAME = "RELIANCE ELECTRONICS & APPLIANCES SERVICE DESK"

SERVICES = {
    "1": "Mobile Phone Repair / Support",
    "2": "Laptop / Computer Support",
    "3": "Television Installation / Repair",
    "4": "Refrigerator Repair",
    "5": "Washing Machine Repair",
    "6": "Air Conditioner Service / Repair",
    "7": "Microwave / Kitchen Appliance Repair",
    "8": "Product Demo / Setup Assistance",
    "9": "Warranty / Extended Protection Plan",
    "10": "Billing, Exchange, or Delivery Support"
}

class VirtualQueue:

    def __init__(self):
        self.file_name = FILE_NAME
        self.create_files()

    def create_files(self):
        if not os.path.exists(self.file_name):
            with open(self.file_name, "w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=QUEUE_FIELDS)
                writer.writeheader()

        if not os.path.exists(FEEDBACK_FILE):
            with open(FEEDBACK_FILE, "w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=FEEDBACK_FIELDS)
                writer.writeheader()

    def read_data(self):
        with open(self.file_name, "r", newline="", encoding="utf-8") as file:
            return list(csv.DictReader(file))

    def save_data(self, data):
        with open(self.file_name, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=QUEUE_FIELDS)
            writer.writeheader()
            writer.writerows(data)

    def generate_token(self):
        data = self.read_data()
        return max(
            (int(row["Token"]) for row in data),
            default=1000
        ) + 1

    @staticmethod
    def get_non_empty_input(prompt):
        while True:
            value = input(prompt).strip()

            if value:
                return value

            print("This field cannot be empty. Please try again.")

    def get_valid_token(self, prompt="Enter token number: "):
        while True:
            token = input(prompt).strip()

            if token.isdigit():
                return token

            print("Token number must contain digits only.")

    def add_customer(self):
        name = self.get_non_empty_input("Enter customer name: ")

        if not all(char.isalpha() or char.isspace() for char in name):
            print("Name can contain letters and spaces only.")
            return

        service = self.select_service()
        token = self.generate_token()

        joined_at = datetime.now().strftime("%d-%m-%Y %I:%M %p")

        with open(self.file_name, "a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=QUEUE_FIELDS)

            writer.writerow({
                "Token": token,
                "Name": name,
                "Service": service,
                "Time": joined_at,
                "Status": "Waiting",
                "Delay Reason": ""
            })

        print("\nCustomer added successfully!")
        print("Your token number:", token)

    @staticmethod
    def display_services():
        print("\n--- AVAILABLE SERVICES ---")

        for number, service in SERVICES.items():
            print(f"{number}. {service}")

    def select_service(self):
        self.display_services()

        while True:
            choice = input("Select a service number (1-10): ").strip()

            if choice in SERVICES:
                return SERVICES[choice]

            print("Invalid service choice. Select a number from 1 to 10.")

    def view_queue(self):
        data = self.read_data()

        active_customers = [
            row for row in data
            if row["Status"] != "Completed"
        ]

        if not active_customers:
            print("Queue is empty!")
            return

        print("\n--- ACTIVE VIRTUAL QUEUE ---")
        print("-" * 75)

        for row in active_customers:
            delay_note = (
                f" | Reason: {row.get('Delay Reason', '')}"
                if row["Status"] == "Service Delayed"
                and row.get("Delay Reason", "")
                else ""
            )

            print(
                f"Token: {row['Token']} | "
                f"Name: {row['Name']} | "
                f"Service: {row['Service']} | "
                f"Status: {row['Status']}"
                f"{delay_note}"
            )

        print("-" * 75)

    def display_served_customers(self):
        served_customers = [
            row for row in self.read_data()
            if row["Status"] == "Completed"
        ]

        if not served_customers:
            print("No customers have been served yet.")
            return

        print("\n--- SERVED CUSTOMERS ---")
        print("-" * 75)

        for row in served_customers:
            print(
                f"Token: {row['Token']} | "
                f"Name: {row['Name']} | "
                f"Service: {row['Service']} | "
                f"Joined: {row['Time']}"
            )

        print("-" * 75)

    def track_customer(self):
        token = self.get_valid_token()
        data = self.read_data()

        waiting = [
            row for row in data
            if row["Status"] == "Waiting"
        ]

        for position, row in enumerate(waiting, start=1):
            if row["Token"] == token:
                print("\nCustomer found!")
                print("Name:", row["Name"])
                print("Token:", row["Token"])
                print("Queue position:", position)
                print("Status:", row["Status"])
                return

        for row in data:
            if row["Token"] == token:
                print("\nCustomer found!")
                print("Name:", row["Name"])
                print("Status:", row["Status"])
                return

        print("Invalid token number!")

    def call_next_customer(self):
        data = self.read_data()

        if any(row["Status"] == "Serving" for row in data):
            print("A customer is already being served. Complete that service first.")
            return

        for row in data:
            if row["Status"] == "Waiting":
                row["Status"] = "Serving"
                self.save_data(data)

                print("\nNow serving customer")
                print("Token:", row["Token"])
                print("Name:", row["Name"])
                print("Service:", row["Service"])
                return

        print("No customers waiting!")

    def complete_service(self):
        token = self.get_valid_token()
        data = self.read_data()

        for row in data:
            if row["Token"] == token and row["Status"] == "Serving":
                row["Status"] = "Completed"
                self.save_data(data)

                print("Service completed successfully!")
                self.collect_feedback(row)
                return

        print("Serving customer not found!")

    def mark_service_delayed(self):
        token = self.get_valid_token(
            "Enter the serving customer's token number: "
        )

        data = self.read_data()

        for row in data:
            if row["Token"] == token and row["Status"] == "Serving":
                reason = self.get_non_empty_input(
                    "Enter the reason for delay/incomplete service: "
                )

                row["Status"] = "Service Delayed"
                row["Delay Reason"] = reason

                self.save_data(data)

                print("Service marked as delayed/incomplete.")
                print("The customer can be resumed later.")
                return

        print("A serving customer with that token was not found!")

    def resume_delayed_service(self):
        data = self.read_data()

        if any(row["Status"] == "Serving" for row in data):
            print("Complete or delay the current service first.")
            return

        token = self.get_valid_token(
            "Enter delayed customer's token number: "
        )

        for row in data:
            if row["Token"] == token and row["Status"] == "Service Delayed":
                row["Status"] = "Serving"
                row["Delay Reason"] = ""

                self.save_data(data)

                print(
                    f"Service resumed for token {row['Token']} "
                    f"({row['Name']})."
                )
                return

        print("A delayed customer with that token was not found!")

    def collect_feedback(self, customer):
        print("\n--- CUSTOMER FEEDBACK ---")

        while True:
            rating = input(
                "Rate the service from 1 to 5 (or press Enter to skip): "
            ).strip()

            if not rating:
                print("Feedback skipped.")
                return

            if rating in {"1", "2", "3", "4", "5"}:
                break

            print("Please enter a whole-number rating from 1 to 5.")

        comment = input("Enter a comment (optional): ").strip()

        with open(FEEDBACK_FILE, "a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=FEEDBACK_FIELDS)

            writer.writerow({
                "Token": customer["Token"],
                "Name": customer["Name"],
                "Rating": rating,
                "Comment": comment,
                "Submitted At": datetime.now().strftime("%d-%m-%Y %I:%M %p")
            })

        print("Thank you. Feedback saved successfully!")

    def search_customer(self):
        token = self.get_valid_token()

        for row in self.read_data():
            if row["Token"] == token:
                print("\n--- CUSTOMER DETAILS ---")

                for key, value in row.items():
                    print(f"{key}: {value}")

                return

        print("Customer not found!")

class QueueApp:

    def __init__(self):
        self.queue = VirtualQueue()

    def menu(self):
        while True:
            print("\n===== VIRTUAL QUEUE TRACKING SYSTEM =====")
            print(f"\n===== {STORE_NAME} =====")

            print("1. Add Customer")
            print("2. View Active Queue")
            print("3. Track Queue Position")
            print("4. Call Next Customer")
            print("5. Complete Service and Collect Feedback")
            print("6. Mark Service Delayed / Incomplete")
            print("7. Resume Delayed Service")
            print("8. Search Customer")
            print("9. Display Served Customers")
            print("10. Exit")

            choice = input("Enter your choice (1-10): ").strip()

            actions = {
                "1": self.queue.add_customer,
                "2": self.queue.view_queue,
                "3": self.queue.track_customer,
                "4": self.queue.call_next_customer,
                "5": self.queue.complete_service,
                "6": self.queue.mark_service_delayed,
                "7": self.queue.resume_delayed_service,
                "8": self.queue.search_customer,
                "9": self.queue.display_served_customers
            }

            if choice == "10":
                print("Thank you for using Virtual Queue System!")
                break

            if choice in actions:
                actions[choice]()
            else:
                print("Invalid choice. Please select a number from 1 to 10.")


if __name__ == "__main__":
    QueueApp().menu()