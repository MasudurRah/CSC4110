"""Modules to import tkinter, turtle, random, and re functionality"""
import tkinter as tk
import turtle
import random
import re

# Load words from the "GroupProject2/files/sgb-words.txt" file into a list
with open("GroupProject2/files/sgb-words.txt", "r", encoding="utf-8") as file:
    word_list = file.read().splitlines()

# Initialize the game state
CURRENT_WORD = None
ATTEMPTS_LEFT = 5
CURRENT_ATTEMPT = 0
PREVIOUS_ATTEMPTS = []
TIMER_SECONDS = 90
TIMER_ACTIVE = False
GAME_WON = False

# Create a function to clear the turtle graphics
def clear_screen():
    """Clear screen function"""
    t.reset()
    t.speed(0)
    t.penup()
    t.goto(0, 0)
    t.pendown()

# Function to update the timer label
def update_timer():
    """Update timer function"""
    global TIMER_SECONDS, TIMER_ACTIVE
    timer_label.config(text=f"Time left: {TIMER_SECONDS} seconds")
    if TIMER_SECONDS > 0 and TIMER_ACTIVE:
        TIMER_SECONDS -= 1
        root.after(1000, update_timer)
    else:
        if CURRENT_ATTEMPT < 5 and not GAME_WON:
            results_label.config(text="Time's up! You lost. The word was: " + CURRENT_WORD)
        play_again_button.config(state=tk.NORMAL)
        entry.config(state=tk.DISABLED)
        TIMER_ACTIVE = False

# Function to enable the input box after a delay
def enable_input():
    """Function to enable the input"""
    entry.config(state=tk.NORMAL)

# Function to initialize the app
def initialize_app():
    """Function to initialize app on startup"""
    canvas.config(bg="green")
    clear_screen()
    t.color("yellow")
    t.write("Welcome to Wordle", align="center", font=("Arial", 24, "bold"))
    entry.delete(0, tk.END)
    entry.insert(0, "Enter a word to start")
    entry.config(state=tk.DISABLED)
    play_again_button.config(text="Start Game", state=tk.NORMAL)

# Function to initialize the game
def initialize_game():
    """Function to initialize game on startup"""
    global CURRENT_WORD, ATTEMPTS_LEFT, CURRENT_ATTEMPT
    global PREVIOUS_ATTEMPTS, TIMER_SECONDS, TIMER_ACTIVE, GAME_WON
    CURRENT_WORD = None
    ATTEMPTS_LEFT = 5
    CURRENT_ATTEMPT = 0
    PREVIOUS_ATTEMPTS = []
    TIMER_SECONDS = 90
    TIMER_ACTIVE = False
    GAME_WON = False
    timer_label.config(text=f"Time left: {TIMER_SECONDS} seconds")
    results_label.config(text="")
    entry.config(state=tk.NORMAL)
    entry.delete(0, tk.END)
    canvas.config(bg="white")
    play_again_button.config(text="Play Again", state=tk.DISABLED)
    clear_screen()

# Create a tkinter window
root = tk.Tk()
root.title("Wordle Clone")

# Create a Canvas widget for the turtle graphics
canvas = tk.Canvas(root, width=500, height=500)
canvas.pack()

# Create a Turtle screen within the canvas
screen = turtle.TurtleScreen(canvas)
t = turtle.RawTurtle(screen)
t.speed(0)

# Create an Entry widget for user input
entry = tk.Entry(root)
entry.pack()

# Create a Label for displaying feedback
results_label = tk.Label(root, text="")
results_label.pack()

# Create a Label for displaying the timer
timer_label = tk.Label(root, text=f"Time left: {TIMER_SECONDS} seconds")
timer_label.pack()

# Function to draw a single attempt
def draw_attempt(user_input, feedback, y_offset):
    """Function to draw the user attempts"""
    for i in range(5):
        t.penup()
        t.goto(-100 + i * 40, 100 - y_offset)
        t.pendown()
        t.pencolor("black")

        if feedback[i] == "G":
            t.fillcolor("green")
        elif feedback[i] == "Y":
            t.fillcolor("yellow")
        else:
            t.fillcolor("red")

        t.begin_fill()
        for _ in range(4):
            t.forward(40)
            t.left(90)
        t.end_fill()

        t.penup()
        t.goto(-80 + i * 40, 105 - y_offset)
        t.pendown()
        t.pencolor("black")
        t.write(user_input[i], align="center", font=("Arial", 16, "normal"))

# Create a function to check the user's input and update the visual representation
def check_word():
    """Function to check and validate user input"""
    global CURRENT_WORD, CURRENT_ATTEMPT, TIMER_ACTIVE, GAME_WON

    if CURRENT_ATTEMPT >= 5 or GAME_WON:
        return

    user_input = entry.get().lower()
    entry.delete(0, tk.END)

    if not re.match("^[a-zA-Z]*$", user_input):
        results_label.config(text="Enter a 5-letter word using only English letters")
        return

    if len(user_input) != 5:
        results_label.config(text="Enter a 5-letter word")
        return

    if CURRENT_WORD is None:
        CURRENT_WORD = random.choice(word_list)
        TIMER_ACTIVE = True
        update_timer()

    CURRENT_ATTEMPT += 1
    feedback = ""
    for i in range(5):
        if user_input[i] == CURRENT_WORD[i]:
            feedback += "G"
        elif user_input[i] in CURRENT_WORD:
            feedback += "Y"
        else:
            feedback += "X"

    results_label.config(text=feedback)

    PREVIOUS_ATTEMPTS.append((user_input, feedback))

    entry.config(state=tk.DISABLED)

    draw_attempt(user_input, feedback, (CURRENT_ATTEMPT - 1) * 40)

    if feedback == "GGGGG":
        results_label.config(text="Congratulations! You guessed the word: " + CURRENT_WORD)
        GAME_WON = True
        play_again_button.config(state=tk.NORMAL)
        entry.config(state=tk.DISABLED)
        TIMER_ACTIVE = False
    elif CURRENT_ATTEMPT >= 5:
        results_label.config(text="You lost. The word was: " + CURRENT_WORD)
        play_again_button.config(state=tk.NORMAL)
        entry.config(state=tk.DISABLED)
        TIMER_ACTIVE = False

    root.after(400, enable_input)

# Bind the Enter key to the check_word function
entry.bind("<Return>", lambda event=None: check_word())

# Create a "Play Again" button
play_again_button = tk.Button(root, text="Start Game", command=initialize_game, state=tk.DISABLED)
play_again_button.pack()

# Initialize the app when the program starts
initialize_app()

# Start the tkinter main loop
root.mainloop()
