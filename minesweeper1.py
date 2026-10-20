import random
import tkinter as tk
import tkinter.font as font

# Constants
DISPLAY_WIDTH = 1000
DISPLAY_HEIGHT = 800

GAME_WIDTH = 10
GAME_HEIGHT = 10

set_clickable = True

game_field = []
amount_mines = GAME_HEIGHT * GAME_WIDTH // 10  # Integer division
mine_found_counter = 0
reveal_count = 0
total_count = GAME_WIDTH * GAME_HEIGHT

# Initialize the game board
def initialize_board():
    board = [[0 for _ in range(GAME_HEIGHT)] for _ in range(GAME_WIDTH)] 
    place_mines(board)
    calculate_adjacent_mines(board)
    return board

def place_mines(board):   
    placed_mines = 0
    while placed_mines < amount_mines:
        row = random.randint(0, GAME_HEIGHT - 1)
        col = random.randint(0, GAME_WIDTH - 1)
        if board[row][col] != 'M':
            board[row][col] = 'M'
            placed_mines += 1

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

# Reveal cell and handle the game logic
def reveal_cell(row, col, board):
    global set_clickable 
    if not set_clickable:
        return
    
    if board[row][col] == 'M':
        buttons[row][col].config(text="M", bg="red")
        label.configure(text="Sadly, You got blown up!")
        set_clickable = False

        button1 = tk.Button(master=buttons_line, text="Go Back", command=end_of_game)
        button1.pack(side="left", padx=5)

        button2 = tk.Button(master=buttons_line, text="Start New Game", command=start_game)
        button2.pack()

    else:
        buttons[row][col].config(text=str(board[row][col]) if board[row][col] > 0 else "", 
                                 state="disabled", relief="sunken")
        
        # If the cell has no adjacent mines, reveal neighbors recursively
        if board[row][col] == 0:
            reveal_neighbors(row, col, board)

def reveal_neighbors(row, col, board):
    global reveal_count
    for r in range(max(0, row - 1), min(GAME_HEIGHT, row + 2)):
        for c in range(max(0, col - 1), min(GAME_WIDTH, col + 2)):
            if (r, c) != (row, col) and buttons[r][c]["state"] != "disabled":
                reveal_cell(r, c, board)
                reveal_count += 1

def right_click_cell(event, row, col, buttons, board):
    global mine_found_counter, set_clickable
    if not set_clickable:
        return
    
    if board[row][col] == 'M':
        buttons[row][col].config(text="M", bg="green")
        mine_found_counter += 1
        label2.configure(text=f"{amount_mines - mine_found_counter}")

        if (mine_found_counter >= amount_mines):
            label.configure(text="Congratulations! You found all the mines!")

            button1 = tk.Button(master=buttons_line, text="Go Back", command=end_of_game)
            button1.pack(side="left", padx=5)

            button2 = tk.Button(master=buttons_line, text="Start New Game", command=start_game)
            button2.pack()
    else:
        buttons[row][col].config(text=str(board[row][col]) if board[row][col] > 0 else "", state="disabled", relief="sunken")
        if board[row][col] == 0:
            reveal_neighbors(row, col, board)
        buttons[row][col].config(bg="red")
        label.configure(text="Sadly, You got blown up!")
        set_clickable = False

        button1 = tk.Button(master=buttons_line, text="Go Back", command=end_of_game)
        button1.pack(side="left", padx=5)

        button2 = tk.Button(master=buttons_line, text="Start New Game", command=start_game)
        button2.pack()

# Initialize the game UI
def start_game():
    global reveal_count, buttons_line, label2, main, set_clickable

    set_clickable = True

    buttons_line = tk.Frame(master=root)
    buttons_line.pack(pady=20)

    for widget in sideInner.winfo_children():
        widget.destroy()

    for widget in main.winfo_children():
        widget.destroy()

    for widget in buttons_line.winfo_children():
        widget.destroy()
        

    label1 = tk.Label(sideInner, text="Mines left:", font=("Arial", 12, "bold"), background="#DDDDDD")
    label1.pack()

    label2 = tk.Label(sideInner, text=f"{amount_mines - mine_found_counter}", font=("Arial", 16), background="#DDDDDD")
    label2.pack()

    label.configure(text="You get that")

    global buttons
    buttons = [[None for _ in range(GAME_WIDTH)] for _ in range(GAME_HEIGHT)]
  
    board = initialize_board()
    for row in range(GAME_HEIGHT):
        for col in range(GAME_WIDTH):
            button = tk.Button(main, width=3, height=1, command=lambda r=row, c=col: reveal_cell(r, c, board))
            button.grid(row=row, column=col)  # Grid inside the frame
            buttons[row][col] = button
            
            button.bind("<Button-3>", lambda event, r=row, c=col: right_click_cell(event, r, c, buttons, board))

    empty_cells = [(r, c) for r in range(GAME_HEIGHT) for c in range(GAME_WIDTH) if board[r][c] == 0]
    if empty_cells:
        ran_row, ran_col = random.choice(empty_cells)
        reveal_cell(ran_row, ran_col, board)
        reveal_count += 1   

def end_of_game():
    for widget in main.winfo_children():
        widget.destroy()
    
    for widget in buttons_line.winfo_children():
        widget.destroy()
        
    label.configure(text="Start a New Game")
    
    button = tk.Button(master=main, text="Play Again", command=start_game)
    button.pack()

def main_screen():
    global side, sideInner, main

    label.configure(text="Welcome to the Game")

    side = tk.Frame(root, background="#DDDDDD")
    side.pack(side="left", fill="y")

    sideInner = tk.Frame(side, background="#DDDDDD")
    sideInner.pack(pady=10, padx=30)

    label1 = tk.Label(sideInner, text="Start now", font=("Arial", 12, "bold"), background="#DDDDDD")
    label1.pack()

    main = tk.Frame(root, bd=2)
    main.pack(pady=20)

    # Button using ttk with custom style
    button = tk.Button(master=main, text="Start Game", command=start_game)
    button.pack()

root = tk.Tk()
root.title("Minesweeper")
root.geometry("800x600")

header = tk.Frame(root, bg="#AAAAAA")
header.pack(fill="x")

header_inner = tk.Frame(header)
header_inner.pack(pady=10, padx=10)

label = tk.Label(master=header_inner, text="Welcome", background="#AAAAAA", font=("Arial", 18, "bold"))
label.pack()

main_screen()

root.mainloop()
