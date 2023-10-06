import tkinter as tk
import turtle
import random
import re
import time

# Load words from the "GroupProject2/files/sgb-words.txt" file into a list
with open("GroupProject2/files/sgb-words.txt", "r") as file:
    word_list = file.read().splitlines()

# Initialize the game state
current_word = None
attempts_left = 5
current_attempt = 0
previous_attempts = []
timer_seconds = 60

# Function to update the timer label
def update_timer():
    global timer_seconds
    timer_label.config(text=f"Time left: {timer_seconds} seconds")
    if timer_seconds > 0:
        timer_seconds -= 1
        root.after(1000, update_timer)
    else:
        results_label.config(text="Time's up! You lost. The word was: " + current_word)
        play_again_button.config(state=tk.NORMAL)
        entry.config(state=tk.DISABLED)

# Function to enable the input box after a delay
def enable_input():
    entry.config(state=tk.NORMAL)

# Function to initialize the game
def initialize_game():
    global current_word, attempts_left, current_attempt, previous_attempts, timer_seconds
    current_word = random.choice(word_list)
    attempts_left = 5
    current_attempt = 0
    previous_attempts = []
    timer_seconds = 60
    update_timer()
    results_label.config(text="")
    entry.config(state=tk.NORMAL)
    entry.delete(0, tk.END)
    canvas.delete("all")  # Clear the canvas
    play_again_button.config(state=tk.DISABLED)  # Disable the "Play Again" button until the game ends

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
timer_label = tk.Label(root, text=f"Time left: {timer_seconds} seconds")
timer_label.pack()

# Create a "Play Again" button
play_again_button = tk.Button(root, text="Play Again", command=initialize_game, state=tk.DISABLED)
play_again_button.pack()

# Function to draw a single attempt
def draw_attempt(user_input, feedback, y_offset):
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
    global current_word, current_attempt, attempts_left, previous_attempts
    if current_attempt >= 5:
        return  # No more input after 5 attempts

    user_input = entry.get().lower()
    entry.delete(0, tk.END)


    if not re.match("^[a-zA-Z]*$", user_input):
        results_label.config(text="Enter a 5-letter word using only English letters")
        return

    if len(user_input) != 5:
        results_label.config(text="Enter a 5-letter word")
        return

    if current_word is None:
        current_word = random.choice(word_list)
        play_again_button.config(state=tk.NORMAL)

    current_attempt += 1
    feedback = ""
    for i in range(5):
        if user_input[i] == current_word[i]:
            feedback += "G"
        elif user_input[i] in current_word:
            feedback += "Y"
        else:
            feedback += "X"

    results_label.config(text=feedback)

    previous_attempts.append((user_input, feedback))

    entry.config(state=tk.DISABLED)

    draw_attempt(user_input, feedback, (current_attempt - 1) * 40)

    if feedback == "GGGGG":
        results_label.config(text="Congratulations! You guessed the word: " + current_word)
        play_again_button.config(state=tk.NORMAL)
    elif current_attempt >= 5:
        results_label.config(text="You lost. The word was: " + current_word)
        play_again_button.config(state=tk.NORMAL)

    root.after(400, enable_input)

# Bind the Enter key to the check_word function
entry.bind("<Return>", lambda event=None: check_word())

# Initialize the game when the program starts
initialize_game()

# Start the tkinter main loop
root.mainloop()
