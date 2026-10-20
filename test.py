import tkinter as tk
import random

# Global game settings
GAME_WIDTH = 8      # Width of the board (columns)
GAME_HEIGHT = 8     # Height of the board (rows)
amount_mines = 10   # Number of mines

# Initialize board with mines and mine counts
def initialize_board():
    board = [[0 for _ in range(GAME_WIDTH)] for _ in range(GAME_HEIGHT)] 
    place_mines(board)
    calculate_adjacent_mines(board)
    return board

def place_mines(board):
    placed_mines = 0
    while placed_mines < amount_mines:
        row = random.randint(0, GAME_HEIGHT - 1)
        col = random.randint(0, GAME_WIDTH - 1)
        
        # Place a mine only if there isn't already one at this location
        if board[row][col] != 'M':
            board[row][col] = 'M'
            placed_mines += 1
    print("placed mines:", placed_mines)

def calculate_adjacent_mines(board):
    for row in range(GAME_HEIGHT):
        for col in range(GAME_WIDTH):
            if board[row][col] != 'M':
                mine_count = sum(
                    board[r][c] == 'M'
                    for r in range(max(0, row - 1), min(GAME_HEIGHT, row + 2))
                    for c in range(max(0, col - 1), min(GAME_WIDTH, col + 2))
                )
                board[row][col] = mine_count

# Function to reveal the cell when clicked
def reveal_cell(row, col):
    if board[row][col] == 'M':
        buttons[row][col].config(text="M", bg="red")
        tk.messagebox.showinfo("Game Over", "You clicked on a mine!")
        root.quit()
    else:
        # Display the number of adjacent mines or blank if 0
        buttons[row][col].config(text=str(board[row][col]) if board[row][col] > 0 else "", state="disabled", relief="sunken")
        
        # If the cell has no adjacent mines, reveal neighbors recursively
        if board[row][col] == 0:
            reveal_neighbors(row, col)

def reveal_neighbors(row, col):
    for r in range(max(0, row - 1), min(GAME_HEIGHT, row + 2)):
        for c in range(max(0, col - 1), min(GAME_WIDTH, col + 2)):
            if (r, c) != (row, col) and buttons[r][c]["state"] != "disabled":
                reveal_cell(r, c)

# Initialize main tkinter window
root = tk.Tk()
root.title("Minesweeper")

# Create board and button grid
board = initialize_board()  # Call with the global variables
buttons = [[None for _ in range(GAME_WIDTH)] for _ in range(GAME_HEIGHT)]

for row in range(GAME_HEIGHT):
    for col in range(GAME_WIDTH):
        button = tk.Button(root, width=3, height=1, command=lambda r=row, c=col: reveal_cell(r, c))
        button.grid(row=row, column=col)
        buttons[row][col] = button

# Run the main loop
root.mainloop()
