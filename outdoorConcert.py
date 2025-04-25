import os
import json

"""
This example code creates a 2D list (2D matrix) that can store seating.
The matrix is populated with "a" since all seats are available and "X" for sold seats.
The code includes a menu system for guests to view the seating chart.
"""

# Constants for seating dimensions and seat states
N_ROW = 20  # Number of rows
N_COL = 26  # Number of columns
AVAILABLE_SEAT = "a"
SOLD_SEAT = "X"
FRONT_SEAT_PRICE = 80
MIDDLE_SEAT_PRICE = 50
BACK_SEAT_PRICE = 25
STATE_TAX_RATE = 0.0725
MASK_FEE = 5.00

SEATING_FILE = "seating.json"
PURCHASES_FILE = "purchases.json"

purchases = {}  # Dictionary to store user purchases


def create_seating(rows, cols, available_seat):
    """Creates a seating chart with all seats available."""
    return [[available_seat for _ in range(cols)] for _ in range(rows)]


def print_seating_chart(seating):
    """Prints the seating chart with rows labeled by numbers and columns labeled by letters."""
    # Generate column labels (A, B, C, ...)
    column_labels = "   " + " ".join(
        chr(65 + i) for i in range(len(seating[0]))
    )  # A, B, C, ...
    print("\nSeating Chart:")
    print(column_labels)  # Print column labels

    # Print each row with its row number
    for r, row in enumerate(seating, start=1):
        print(f"{r:2} " + " ".join(row))  # Row number followed by seats
    print()


def purchase_ticket(seating, row, col):
    """Purchases a ticket at the specified row and column, enforcing social distancing in the row and between rows."""
    if seating[row][col] != AVAILABLE_SEAT:
        print("Seat is already occupied. Please choose another seat.")
        return

    # Ask for user details
    name = input("Enter your name: ").strip()
    email = input("Enter your email address: ").strip()

    # Determine the price based on the row
    if 0 <= row <= 4:
        price = FRONT_SEAT_PRICE
    elif 5 <= row <= 10:
        price = MIDDLE_SEAT_PRICE
    elif 11 <= row <= 19:
        price = BACK_SEAT_PRICE
    else:
        print("Invalid row for ticket pricing.")
        return

    # Mark the selected seat as sold
    seating[row][col] = SOLD_SEAT

    # Enforce two available seats to the left
    if col - 1 >= 0:
        seating[row][col - 1] = " "  # Block seat
    if col - 2 >= 0:
        seating[row][col - 2] = " "  # Block seat

    # Enforce two available seats to the right
    if col + 1 < N_COL:
        seating[row][col + 1] = " "  # Block seat
    if col + 2 < N_COL:
        seating[row][col + 2] = " "  # Block seat

    # Enforce one row distance above
    if row - 1 >= 0:
        seating[row - 1] = [
            " " if seat == AVAILABLE_SEAT else seat for seat in seating[row - 1]
        ]

    # Enforce one row distance below
    if row + 1 < N_ROW:
        seating[row + 1] = [
            " " if seat == AVAILABLE_SEAT else seat for seat in seating[row + 1]
        ]

    # Record the purchase
    ticket_info = f"Row {row + 1}, Column {col + 1}, Price: ${price:.2f}"
    if name in purchases:
        purchases[name].append(ticket_info)
    else:
        purchases[name] = [ticket_info]

    # Calculate total cost
    tax = price * STATE_TAX_RATE
    total_cost = price + tax + MASK_FEE

    # Print receipt
    print("\nReceipt:")
    print(f"Name: {name}")
    print(f"Email: {email}")
    print(f"Row: {row + 1}, Column: {col + 1}")
    print(f"Base Price: ${price:.2f}")
    print(f"State Tax (7.25%): ${tax:.2f}")
    print(f"Mandatory Mask Fee: ${MASK_FEE:.2f}")
    print(f"Total Cost: ${total_cost:.2f}\n")


def purchase_bulk_tickets(seating, row, start_col, num_tickets):
    """Purchases bulk tickets in the specified row, allowing adjacent seats."""
    if start_col + num_tickets > N_COL:
        print("Not enough seats available in this row for the bulk purchase.")
        return

    # Ask for user details
    name = input("Enter your name: ").strip()
    email = input("Enter your email address: ").strip()

    # Check if all seats in the range are available
    for col in range(start_col, start_col + num_tickets):
        if seating[row][col] != AVAILABLE_SEAT:
            print(
                "One or more seats in the selected range are not available. Please choose another range."
            )
            return

    # Determine the price based on the row
    if 0 <= row <= 4:
        price = FRONT_SEAT_PRICE
    elif 5 <= row <= 10:
        price = MIDDLE_SEAT_PRICE
    elif 11 <= row <= 19:
        price = BACK_SEAT_PRICE
    else:
        print("Invalid row for ticket pricing.")
        return

    # Mark the selected seats as sold
    for col in range(start_col, start_col + num_tickets):
        seating[row][col] = SOLD_SEAT

    # Record the purchase
    ticket_info = f"Row {row + 1}, Columns {start_col + 1} to {start_col + num_tickets}, Price: ${price:.2f} each"
    if name in purchases:
        purchases[name].append(ticket_info)
    else:
        purchases[name] = [ticket_info]

    # Calculate total cost
    tax = price * STATE_TAX_RATE * num_tickets
    total_cost = (price * num_tickets) + tax + (MASK_FEE * num_tickets)

    # Print receipt
    print("\nReceipt:")
    print(f"Name: {name}")
    print(f"Email: {email}")
    print(f"Row: {row + 1}, Columns: {start_col + 1} to {start_col + num_tickets}")
    print(f"Base Price (per ticket): ${price:.2f}")
    print(f"Number of Tickets: {num_tickets}")
    print(f"State Tax (7.25%): ${tax:.2f}")
    print(f"Mandatory Mask Fee (per ticket): ${MASK_FEE:.2f}")
    print(f"Total Cost: ${total_cost:.2f}\n")


def search_by_name():
    """Searches for tickets purchased by a user with a specific name."""
    name = input("Enter the name to search for: ").strip()
    if name in purchases:
        print(f"\nTickets purchased by {name}:")
        for ticket in purchases[name]:
            print(f"- {ticket}")
    else:
        print(f"No tickets found for {name}.")


def display_all_purchases():
    """Displays all purchases made by all users and calculates total income."""
    if not purchases:
        print("No purchases have been made yet.")
        return

    total_income = 0  # Variable to track total income

    print("\nAll Purchases:")
    for name, tickets in purchases.items():
        print(f"\n{name}:")
        for ticket in tickets:
            print(f"- {ticket}")
            # Extract the price from the ticket string and add to total income
            price_start = ticket.rfind("$") + 1
            total_income += float(ticket[price_start:])

    print(f"\nTotal Income: ${total_income:.2f}")


def save_data(seating, purchases):
    """Saves seating and purchase data to .json files."""
    with open(SEATING_FILE, "w") as seating_file:
        json.dump(seating, seating_file)
    with open(PURCHASES_FILE, "w") as purchases_file:
        json.dump(purchases, purchases_file)
    print("Data saved successfully.")


def load_data():
    """Loads seating and purchase data from .json files or creates default files if they do not exist."""
    if not os.path.exists(SEATING_FILE) or not os.path.exists(PURCHASES_FILE):
        print("No saved data found. Creating default files...")
        seating = create_seating(N_ROW, N_COL, AVAILABLE_SEAT)
        purchases = {}
        save_data(seating, purchases)  # Create default files
        return seating, purchases

    try:
        with open(SEATING_FILE, "r") as seating_file:
            seating = json.load(seating_file)
        with open(PURCHASES_FILE, "r") as purchases_file:
            purchases = json.load(purchases_file)
        print("Data loaded successfully.")
        return seating, purchases
    except Exception as e:
        print(f"Error loading data: {e}")
        seating = create_seating(N_ROW, N_COL, AVAILABLE_SEAT)
        purchases = {}
        return seating, purchases


def menu(seating):
    """Displays a menu system for guests."""
    print("Welcome to Concert Guru! How can I help you today?")  # Add welcome message
    while True:
        print("Menu:")
        print("[V] View/display available seating")
        print("[P] Purchase tickets")
        print("[S] Search by name")
        print("[D] Display all purchases")
        print("[Q] Quit")
        choice = input("Enter your choice: ").strip().upper()

        if choice == "V":
            print_seating_chart(seating)
        elif choice == "P":
            print("Purchase Options:")
            print("[ST] Single ticket")
            print("[BT] Bulk tickets")
            sub_choice = input("Enter your choice: ").strip().upper()

            if sub_choice == "ST":
                try:
                    row = int(input("Enter the row number (1-20): ")) - 1
                    col = int(input("Enter the column number (1-26): ")) - 1
                    if 0 <= row < N_ROW and 0 <= col < N_COL:
                        purchase_ticket(seating, row, col)
                        save_data(
                            seating, purchases
                        )  # Save data after each transaction
                    else:
                        print("Invalid row or column. Please try again.")
                except ValueError:
                    print("Invalid input. Please enter valid numbers.")
            elif sub_choice == "BT":
                try:
                    row = int(input("Enter the row number (1-20): ")) - 1
                    start_col = (
                        int(input("Enter the starting column number (1-26): ")) - 1
                    )
                    num_tickets = int(
                        input("Enter the number of tickets to purchase: ")
                    )
                    if (
                        0 <= row < N_ROW
                        and 0 <= start_col < N_COL
                        and start_col + num_tickets <= N_COL
                    ):
                        purchase_bulk_tickets(seating, row, start_col, num_tickets)
                        save_data(
                            seating, purchases
                        )  # Save data after each transaction
                    else:
                        print("Invalid input. Please try again.")
                except ValueError:
                    print("Invalid input. Please enter valid numbers.")
            else:
                print("Invalid choice. Please try again.")
        elif choice == "S":
            search_by_name()
        elif choice == "D":
            display_all_purchases()
        elif choice == "Q":
            save_data(seating, purchases)  # Save data before quitting
            print("Concert Guru says Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


# Main logic
seating, purchases = load_data()
menu(seating)
