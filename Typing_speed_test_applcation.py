import tkinter as tk  # tkinter imported
import time

root = tk.Tk()  # main window created
root.title("Typing Speed Test")  # title to the window given 
root.geometry("600x420")

# --- Paragraph to type ---
text_to_type = """Python is an easy to learn, powerful programming language. It has efficient high level data structures 
and a simple but effective approach to object oriented programming."""

# --- Variables ---
start_time = 0
running = False
time_limit = 30  # seconds

# --- Functions ---
def start_test():
    """Start timing and reset everything."""
    global start_time, running
    entry.delete(0, tk.END)  # Deletes anything from the entry box before starting the test
    result_label.config(text="")  # removes all the text from the label
    timer_label.config(text=f"Time Left: {time_limit}s")  # keeps updating the label to tell how much time is left
    start_time = time.time()  # tells the time from a fixed point
    running = True
    entry.config(state="normal")  # state=normal means the user can type inside
    entry.focus()  # gives keyboard focus to the entry widget
    update_timer()  # start countdown


def check_text(event=None):  # event=None helps in calling the function manually, not through Tkinter.
    """Check if user finished typing the paragraph."""
    global running
    if not running:  # stops the function if the test is not running
        return

    typed = entry.get()
    if typed == text_to_type:
        finish_test()


def update_timer():
    """Update timer every second."""
    global running
    if not running:
        return

    elapsed = time.time() - start_time  # how much time has passed since start
    remaining = time_limit - int(elapsed)  # how much time is left before the test ends

    if remaining <= 0:
        finish_test(time_up=True)
    else:
        timer_label.config(text=f"Time Left: {remaining}s")
        root.after(1000, update_timer)  # call this function again after 1 sec


def finish_test(time_up=False):
    """End the test and calculate results."""
    global running
    running = False
    end_time = time.time()
    total_time = round(end_time - start_time, 2)
    typed = entry.get()

    # --- Split both paragraphs into word lists ---
    original_words = text_to_type.split()
    typed_words = typed.split()

    # --- Count correctly spelled words ---
    correct_words = 0
    for i in range(min(len(original_words), len(typed_words))):
        if typed_words[i] == original_words[i]:
            correct_words += 1

    # --- Calculate WPM based on correct words only ---
    if total_time <= 0:
        total_time = 1  # avoid division by zero
    wpm = round((correct_words / total_time) * 60)

    # --- Calculate accuracy ---
    accuracy = round((correct_words / len(original_words)) * 100, 2)

    # --- Disable entry ---
    entry.config(state="disabled")

    # --- Show results ---
    if time_up:
        result_label.config(text=f"⏰ Time's up!\nSpeed: {wpm} WPM\nAccuracy: {accuracy}%")
    else:
        result_label.config(text=f"✅ Done!\nTime: {total_time}s\nSpeed: {wpm} WPM\nAccuracy: {accuracy}%")


# --- GUI Layout ---
tk.Label(root, text="Typing Speed Test", font=("Arial", 18, "bold")).pack(pady=10)

tk.Label(root, text=text_to_type, wraplength=550, font=("Arial", 12), justify="left").pack(pady=10)

entry = tk.Entry(root, width=70, font=("Arial", 12))
entry.pack(pady=10)
entry.bind("<KeyRelease>", check_text)

tk.Button(root, text="Start", command=start_test, bg="lightgreen", width=12).pack(pady=5)

timer_label = tk.Label(root, text=f"Time Left: {time_limit}s", font=("Arial", 12, "bold"), fg="red")
timer_label.pack(pady=5)

result_label = tk.Label(root, text="", font=("Arial", 12, "bold"))
result_label.pack(pady=10)

root.mainloop()