import random
import tkinter as tk
import customtkinter as ctk

# Constants
DISPLAY_WIDTH = 1000
DISPLAY_HEIGHT = 800

GAME_WIDTH = 10
GAME_HEIGHT = 10

amount_mines = GAME_HEIGHT * GAME_WIDTH // 10  # Integer division
mine_found_counter = 0
reveal_count = 0
game_ended = False

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

def reveal_cell(row, col, board):
    if board[row][col] == 'M':
        buttons[row][col].configure(text="M", bg="red")
        label.configure(text="Sadly, You got blown up!")
        create_end_buttons()
    else:
        buttons[row][col].configure(
            text=str(board[row][col]) if board[row][col] > 0 else "",
            state="disabled", 
            bg="lightgray" # Optional: Round the corners slightly
        )

        if board[row][col] == 0:
            reveal_neighbors(row, col, board)

def reveal_neighbors(row, col, board):
    global reveal_count
    for r in range(max(0, row - 1), min(GAME_HEIGHT, row + 2)):
        for c in range(max(0, col - 1), min(GAME_WIDTH, col + 2)):
            if (r, c) != (row, col) and buttons[r][c].cget("state") != "disabled":
                reveal_cell(r, c, board)
                reveal_count += 1

def right_click_cell(event, row, col):
    global mine_found_counter
    if board[row][col] == 'M':
        buttons[row][col].configure(text="M", bg="green")
        mine_found_counter += 1
        label2.configure(text=f"{amount_mines - mine_found_counter}")
        if mine_found_counter >= amount_mines:
            label.configure(text="Congratulations! You found all the mines!")
            create_end_buttons()
    else:
        buttons[row][col].configure(bg="red", state="disabled")
        label.configure(text="Sadly, You got blown up!")
        create_end_buttons()

def create_end_buttons():
    global game_ended
    if game_ended == False:
        button1 = ctk.CTkButton(master=buttons_line, text="Go Back", command=end_of_game)
        button1.pack(side="left", padx=5)
        button2 = ctk.CTkButton(master=buttons_line, text="Start New Game", command=start_game)
        button2.pack()
        game_ended = True

def start_game():
    global reveal_count, buttons_line, label2, main, board, buttons, mine_found_counter
    reveal_count, mine_found_counter = 0, 0

    buttons_line = ctk.CTkFrame(master=root)
    buttons_line.pack(pady=20)

    # Clear previous widgets
    for widget in side.winfo_children():
        widget.destroy()
    for widget in main.winfo_children():
        widget.destroy()
    for widget in buttons_line.winfo_children():
        widget.destroy()

    label1 = ctk.CTkLabel(side, text="Mines left:", font=("Arial", 12, "bold"), pady=20, padx=30)
    label1.pack()
    label2 = ctk.CTkLabel(side, text=f"{amount_mines}", font=("Arial", 16))
    label2.pack()

    label.configure(text="Game Started")
    buttons = [[None for _ in range(GAME_WIDTH)] for _ in range(GAME_HEIGHT)]
    board = initialize_board()

    for row in range(GAME_HEIGHT):
        for col in range(GAME_WIDTH):
            button = tk.Button(main, width=6, height=2, text="", command=lambda r=row, c=col: reveal_cell(r, c, board))
            button.grid(row=row, column=col)
            buttons[row][col] = button
            
            # Right-click event binding
            button.bind("<Button-3>", lambda event, r=row, c=col: right_click_cell(event, r, c))

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
    button = ctk.CTkButton(master=main, text="Play Again", command=start_game)
    button.pack()

def main_screen():
    global side, side, main
    label.configure(text="Welcome to the Game")

    side = ctk.CTkFrame(root, fg_color="#CCCCCC", corner_radius=0)
    side.pack(side="left", fill="y")
    main = ctk.CTkFrame(root, corner_radius=0)
    main.pack(pady=20)

    button = ctk.CTkButton(master=main, text="Start Game", command=start_game)
    button.pack()

root = ctk.CTk()
root.title("Minesweeper")
root.geometry("800x600")

header = ctk.CTkFrame(root, fg_color="#AAAAAA", corner_radius=0)
header.pack(fill="x")
header_inner = ctk.CTkFrame(header)
header_inner.pack(pady=10, padx=10)
label = ctk.CTkLabel(master=header_inner, text="Welcome", fg_color="#AAAAAA", font=("Arial", 18, "bold"))
label.pack()

main_screen()
root.mainloop()
