import tkinter as tk
import string
from tkinter import scrolledtext, messagebox
import random
from datetime import datetime

# Global user_name initialization
user_name = "User"
conversation_log = []

# ----------------- Bot Logic -----------------
def get_bot_response(user_input):
    global user_name
    user_input = user_input.lower()
    user_input = user_input.translate(str.maketrans('', '', string.punctuation))  # Remove punctuation

    # Single-word and phrase-based matching
    if any(word in user_input for word in ["hi", "hello", "hey"]):
        return random.choice([
            f"Hello {user_name}! How can I support your wellness today?",
            f"Hey {user_name}, hope you're feeling great!",
            f"Hi {user_name}! Let’s talk about health. Ask me anything!"
        ])

    elif any(word in user_input for word in ["diet", "food", "eat", "nutrition"]):
        return random.choice([
            "Eat more fruits and veggies 🌿",
            "Avoid junk food and stay hydrated 🥦",
            "A balanced diet means energy and focus 🔋"
        ])

    elif any(word in user_input for word in ["exercise", "workout", "fitness", "fit"]) or \
         any(phrase in user_input for phrase in ["stay fit", "healthy body", "get fit", "keep fit"]):
        return random.choice([
            "30 mins of movement daily keeps the doctor away 💪",
            "Exercise boosts your mood and health 😄",
            "Consistency in workouts builds discipline 🏃‍♂️"
        ])

    elif any(word in user_input for word in ["sleep", "rest", "tired", "insomnia"]):
        return random.choice([
            "Aim for 7–8 hours of sleep 😴",
            "Avoid screens 1 hour before bed 📵",
            "Good sleep = good memory 🧠"
        ])

    elif any(word in user_input for word in ["stress", "anxiety", "mental health", "depression"]):
        return random.choice([
            "Try deep breathing and mindfulness 🧘‍♀️",
            "Journaling helps release built-up stress ✍️",
            "Talk to someone you trust 💬"
        ])

    elif any(word in user_input for word in ["water", "hydrate", "drink"]):
        return random.choice([
            "Drink 2–3L of water daily 💧",
            "Start your day with a glass of water 🚰",
            "Hydration helps with energy and skin 🌞"
        ])

    elif any(word in user_input for word in ["help", "options", "what can you do"]):
        return "You can ask about 🥗 diet, 🏋️‍♀️ exercise, 💤 sleep, 😌 stress, or 💧 hydration."

    elif any(word in user_input for word in ["bye", "exit", "thank you", "thanks"]):
        return "Take care! Stay healthy. 👋"

    else:
        return random.choice([
            "Hmm... I didn't understand that. Try asking about diet or stress.",
            "Could you rephrase? I’m best with health-related queries.",
            "I'm still learning! Try asking about hydration, sleep, or fitness."
        ])

# ----------------- Welcome Window -----------------
def get_user_name():
    # Create a modal welcome window on top of root
    name_window = tk.Toplevel(root)
    name_window.title("Welcome!")
    window_width = 400
    window_height = 200

    # Get screen width and height
    screen_width = name_window.winfo_screenwidth()
    screen_height = name_window.winfo_screenheight()

    # Calculate position x, y to center the window
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)

    name_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
    name_window.grab_set()
    name_window.transient(root)

    tk.Label(name_window, text="Welcome to Health Tips Chatbot!", font=("Arial", 14)).pack(pady=10)
    tk.Label(name_window, text="What's your name?", font=("Arial", 12)).pack(pady=5)

    name_var = tk.StringVar()
    name_entry = tk.Entry(name_window, font=("Arial", 12), textvariable=name_var, width=30)
    name_entry.pack(pady=10)
    name_entry.focus()

    def submit_name():
        global user_name
        entered = name_var.get().strip()
        user_name = entered if entered else "User"
        # Update greeting in chat_display after getting name
        update_greeting()
        name_window.destroy()

    tk.Button(name_window, text="Submit", font=("Arial", 12), command=submit_name).pack(pady=10)

# ----------------- Update greeting with user_name -----------------
def update_greeting():
    chat_display.config(state=tk.NORMAL)
    chat_display.insert(tk.END,
                        f"Bot ({datetime.now().strftime('%H:%M:%S')}): Hi {user_name}! 👋 I'm your health assistant. Ask me about wellness.\n\n")
    chat_display.config(state=tk.DISABLED)
    chat_display.see(tk.END)

# ----------------- Chat Handling -----------------
def send_message(event=None):
    user_msg = user_entry.get().strip()
    if user_msg == "":
        return
    timestamp = datetime.now().strftime('%H:%M:%S')

    chat_display.config(state=tk.NORMAL)
    chat_display.insert(tk.END, f"You ({timestamp}): {user_msg}\n")
    conversation_log.append(f"You ({timestamp}): {user_msg}")

    bot_msg = get_bot_response(user_msg)
    bot_time = datetime.now().strftime('%H:%M:%S')
    chat_display.insert(tk.END, f"Bot ({bot_time}): {bot_msg}\n\n")
    conversation_log.append(f"Bot ({bot_time}): {bot_msg}")
    chat_display.config(state=tk.DISABLED)
    chat_display.see(tk.END)

    user_entry.delete(0, tk.END)

    if "bye" in user_msg.lower() or "exit" in user_msg.lower():
        save_chat()

# ----------------- Save Chat to File -----------------
def save_chat():
    filename = f"{user_name}_chat_history.txt"
    with open(filename, "w", encoding="utf-8") as file:
        file.write("Health Chatbot - Conversation History\n")
        file.write("-" * 40 + "\n")
        for line in conversation_log:
            file.write(line + "\n")
    messagebox.showinfo("Chat Saved", f"Chat saved as {filename}")
    root.quit()

# ----------------- GUI Setup -----------------
root = tk.Tk()
root.title("Health Tips Chatbot")
root.geometry("550x600")
root.resizable(False, False)

# Conversation storage
conversation_log = []

# Chat display box
chat_display = scrolledtext.ScrolledText(root, font=("Segoe UI Emoji", 12), wrap=tk.WORD, state=tk.DISABLED)
chat_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# User entry
user_entry = tk.Entry(root, font=("Arial", 12))
user_entry.pack(padx=10, pady=(0, 10), fill=tk.X)
user_entry.bind("<Return>", send_message)

# Send button
send_btn = tk.Button(root, text="Send", font=("Arial", 12), command=send_message)
send_btn.pack(pady=(0, 10))

# Focus on user entry
user_entry.focus()

# Show welcome dialog after main window appears
root.after(0, get_user_name)

root.mainloop()

