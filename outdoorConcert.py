"""
This example code creates a 2D list (2D matrix) that can store seating.
The matrix is populated with "A" since all seats are available and "X" for sold seats.
The code also includes a function to print the seating chart and a function to sell tickets.
"""

# Constants for seating dimensions and seat states
N_ROW = 4
N_COL = 10
AVAILABLE_SEAT = "A"
SOLD_SEAT = "X"


def create_seating(rows, cols, available_seat):
    """Creates a seating chart with all seats available."""
    return [[available_seat for _ in range(cols)] for _ in range(rows)]


def print_seating_chart(seating):
    """Prints the seating chart."""
    print("Seating Chart:")
    for r, row in enumerate(seating, start=1):
        print(f"{r}\t" + " ".join(row))


# Main logic
seating = create_seating(N_ROW, N_COL, AVAILABLE_SEAT)
print_seating_chart(seating)
