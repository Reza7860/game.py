import tkinter as tk
import random

WINDOW_SIZE = 400
GRID_SIZE = 20
SNAKE_COLOR = "green"
FOOD_COLOR = "red"
BG_COLOR = "black"

snake_direction = "Right"
snake_positions = [(100, 100), (80, 100), (60, 100)]
food_position = (random.randint(0, (WINDOW_SIZE - GRID_SIZE) // GRID_SIZE) * GRID_SIZE,
                 random.randint(0, (WINDOW_SIZE - GRID_SIZE) // GRID_SIZE) * GRID_SIZE)
score = 0
high_score = 0
game_paused = False
game_running = True
speed = 150 


window = tk.Tk()
window.title("Snake Game")
window.resizable(False, False)

canvas = tk.Canvas(window, bg=BG_COLOR, width=WINDOW_SIZE, height=WINDOW_SIZE)
canvas.pack()

score_label = tk.Label(window, text=f"Score: {score}", font=("Arial", 14))
score_label.pack()

high_score_label = tk.Label(window, text=f"High Score: {high_score}", font=("Arial", 14))
high_score_label.pack()

def create_food():
    global food_position
    food_position = (random.randint(0, (WINDOW_SIZE - GRID_SIZE) // GRID_SIZE) * GRID_SIZE,
                     random.randint(0, (WINDOW_SIZE - GRID_SIZE) // GRID_SIZE) * GRID_SIZE)
    canvas.create_rectangle(*food_position, food_position[0] + GRID_SIZE, food_position[1] + GRID_SIZE, fill=FOOD_COLOR, tags="food")

def draw_snake():
    canvas.delete("snake")
    for pos in snake_positions:
        canvas.create_rectangle(*pos, pos[0] + GRID_SIZE, pos[1] + GRID_SIZE, fill=SNAKE_COLOR, tags="snake")

def move_snake():
    global snake_positions, score, game_running, game_paused, high_score, speed
    if game_paused or not game_running:
        return

    head_x, head_y = snake_positions[0]

    if snake_direction == "Up":
        new_head = (head_x, head_y - GRID_SIZE)
    elif snake_direction == "Down":
        new_head = (head_x, head_y + GRID_SIZE)
    elif snake_direction == "Left":
        new_head = (head_x - GRID_SIZE, head_y)
    elif snake_direction == "Right":
        new_head = (head_x + GRID_SIZE, head_y)

    if (
        new_head in snake_positions or 
        new_head[0] < 0 or new_head[0] >= WINDOW_SIZE or
        new_head[1] < 0 or new_head[1] >= WINDOW_SIZE
    ):
        game_over()
        return

    snake_positions = [new_head] + snake_positions[:-1]

    if new_head == food_position:
        snake_positions.append(snake_positions[-1])
        score += 1
        score_label.config(text=f"Score: {score}")
        canvas.delete("food")
        create_food()

        speed = max(50, 150 - (score * 5))

    draw_snake()
    window.after(speed, move_snake)

def change_direction(new_direction):
    global snake_direction
    opposite_directions = {"Up": "Down", "Down": "Up", "Left": "Right", "Right": "Left"}
    if new_direction != opposite_directions.get(snake_direction):  # Avoid reversing direction
        snake_direction = new_direction

def game_over():
    global game_running, high_score
    game_running = False
    if score > high_score:
        high_score = score
        high_score_label.config(text=f"High Score: {high_score}")
    canvas.delete("all")
    canvas.create_text(WINDOW_SIZE / 2, WINDOW_SIZE / 2, text="Game Over", fill="white", font=("Arial", 24))
    canvas.create_text(WINDOW_SIZE / 2, WINDOW_SIZE / 2 + 40, text=f"Score: {score}", fill="white", font=("Arial", 18))
    restart_button.pack()

def toggle_pause():
    global game_paused
    game_paused = not game_paused
    pause_button.config(text="Resume" if game_paused else "Pause")
    if not game_paused:
        move_snake()

def restart_game():
    global snake_positions, snake_direction, score, game_running, game_paused, speed
    snake_positions = [(100, 100), (80, 100), (60, 100)]
    snake_direction = "Right"
    score = 0
    speed = 150
    score_label.config(text=f"Score: {score}")
    game_running = True
    game_paused = False
    pause_button.config(text="Pause")
    canvas.delete("all")
    create_food()
    draw_snake()
    move_snake()
    restart_button.pack_forget()

window.bind("<Up>", lambda event: change_direction("Up"))
window.bind("<Down>", lambda event: change_direction("Down"))
window.bind("<Left>", lambda event: change_direction("Left"))
window.bind("<Right>", lambda event: change_direction("Right"))

pause_button = tk.Button(window, text="Pause", command=toggle_pause)
pause_button.pack()

restart_button = tk.Button(window, text="Restart", command=restart_game)

create_food()
move_snake()
window.mainloop()
