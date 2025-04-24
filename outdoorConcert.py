"""
This example code creates a 2D list (2D matrix) that can store seating. 
The matrix is populated with "A" since all seats are available and "X" for sold seats.
The code also includes a function to print the seating chart and a function to sell tickets.
"""

# out test matrix has 4 rows and 10 columns
N_ROW = 4
N_COL = 10

# available seats are represented by 'A' and sold seats by 'X'
available_seat = 'A'
sold_seat = 'X'

# create some available seating
seating = []
for r in range(N_ROW):
    row = []
    for c in range(N_COL):
        row.append(available_seat)
    seating.append(row)

# function to print the seating chart
for r in range(N_ROW):
    print(r+1, end="\t")
    for c in range(N_COL):
        print(seating[r][c], end=" ")
    print()
