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


def menu(seating):
    """Displays a menu system for guests."""
    while True:
        print("Menu:")
        print("[V] View/display available seating")
        print("[Q] Quit")
        choice = input("Enter your choice: ").strip().upper()

        if choice == "V":
            print_seating_chart(seating)
        elif choice == "Q":
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


# Main logic
seating = create_seating(N_ROW, N_COL, AVAILABLE_SEAT)
menu(seating)
