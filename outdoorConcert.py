"""
This example code creates a 2D list (2D matrix) that can store seating.
The matrix is populated with "a" since all seats are available and "X" for sold seats.
The code includes a menu system for guests to view the seating chart.
"""

# Constants for seating dimensions and seat states
N_ROW = 4
N_COL = 10
AVAILABLE_SEAT = "a"
SOLD_SEAT = "X"


def create_seating(rows, cols, available_seat):
    """Creates a seating chart with all seats available."""
    return [[available_seat for _ in range(cols)] for _ in range(rows)]


def print_seating_chart(seating):
    """Prints the seating chart."""
    print("\nSeating Chart:")
    for r, row in enumerate(seating, start=1):
        print(f"{r}\t" + " ".join(row))
    print()


def purchase_ticket(seating, row, col):
    """Purchases a ticket at the specified row and column, enforcing social distancing in the row and between rows."""
    if seating[row][col] != AVAILABLE_SEAT:
        print("Seat is already occupied. Please choose another seat.")
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
        seating[row - 1] = [" " if seat == AVAILABLE_SEAT else seat for seat in seating[row - 1]]

    # Enforce one row distance below
    if row + 1 < N_ROW:
        seating[row + 1] = [" " if seat == AVAILABLE_SEAT else seat for seat in seating[row + 1]]

    print(f"Ticket purchased at row {row + 1}, column {col + 1}.")


def menu(seating):
    """Displays a menu system for guests."""
    while True:
        print("Menu:")
        print("[V] View/display available seating")
        print("[P] Purchase a ticket")
        print("[Q] Quit")
        choice = input("Enter your choice: ").strip().upper()

        if choice == "V":
            print_seating_chart(seating)
        elif choice == "P":
            try:
                row = int(input("Enter the row number (1-4): ")) - 1
                col = int(input("Enter the column number (1-10): ")) - 1
                if 0 <= row < N_ROW and 0 <= col < N_COL:
                    purchase_ticket(seating, row, col)
                else:
                    print("Invalid row or column. Please try again.")
            except ValueError:
                print("Invalid input. Please enter valid numbers.")
        elif choice == "Q":
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


# Main logic
seating = create_seating(N_ROW, N_COL, AVAILABLE_SEAT)
menu(seating)
