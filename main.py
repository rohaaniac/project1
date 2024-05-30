import nltk
import random
import tkinter as tk
from tkinter import scrolledtext

# Download necessary NLTK data (run once)
nltk.download('punkt')

# Conversation history list
conversation_history = []

# Greeting messages
greetings = [
    "hi", "hello", "hey", "what's up"
]

# Farewell messages
farewell_options = [
    "See you later!", "Have a great day!", "Talk to you soon!", "Bye!"
]

# Questions and answers dictionary
questions_answers = {
    "what is your name?": "I don't have a name, but you can call me Chatbot.",
    "how are you doing?": "I'm doing well, thanks for asking!",
    "what can you do?": "I can answer some basic questions for now. I'm still under development!",
    "what is the weather like?": "I don't have access to weather information yet.",
    "what is your favorite color?": "As a large language model, I don't have preferences like colors.",
}

follow_up_questions = [
    "how old are you?",
    "what's your favorite hobby?",
    "do you have any pets?",
    "what's your favorite food?"
]

asked_follow_up_questions = []  # To keep track of asked follow-up questions
last_question = None  # To keep track of the last asked follow-up question

def handle_greetings(user_input):
    """Provides a response based on greetings."""
    if any(greeting_word in user_input for greeting_word in greetings):
        return "Hi! How can I help you today?"
    else:
        return None

def check_questions(user_input):
    """Checks user input against the question-answer dictionary."""
    return questions_answers.get(user_input, None)

def handle_unknown_input(user_input):
    """Provides a friendly response for unrecognized input."""
    if not user_input:
        return "You didn't enter anything. Please try again!"
    else:
        return "Sorry, I don't understand that question. Could you rephrase?"

def ask_follow_up_question():
    """Asks the next follow-up question based on the current index."""
    remaining_questions = [q for q in follow_up_questions if q not in asked_follow_up_questions]
    if remaining_questions:
        question = random.choice(remaining_questions)
        asked_follow_up_questions.append(question)
        return question
    else:
        return None

def handle_follow_up_response(follow_up_question, follow_up_response):
    """Handles the response to the follow-up question."""
    if follow_up_question == "how old are you?":
        try:
            age = int(follow_up_response)
            if age >= 18:
                return "That's cool! What are you interested in?"
            else:
                return "Nice to meet you! What do you like to do for fun?"
        except ValueError:
            return "That doesn't seem like a valid age. How old are you?"
    else:
        responses = {
            "what's your favorite hobby?": "Sounds fun!",
            "do you have any pets?": "Pets are great!",
            "what's your favorite food?": "Sounds delicious!"
        }
        return responses.get(follow_up_question, handle_unknown_input(follow_up_response))

def choose_farewell():
    """Selects a random farewell message."""
    return random.choice(farewell_options)

def show_conversation_history():
    """Returns the conversation history as a formatted string."""
    history = "Conversation History:\n"
    for i, entry in enumerate(conversation_history):
        history += f"{i+1}. {entry}\n"
    return history

def chatbot_response(user_input):
    """Generates a response from the chatbot based on user input."""
    global last_question

    conversation_history.append(f"You: {user_input}")

    # Check for exit signal
    if user_input in ["bye", "exit"]:
        farewell = choose_farewell()
        conversation_history.append(f"Bot: {farewell}")
        return farewell

    # Check if user asked for conversation history
    if user_input == "history":
        return show_conversation_history()

    # Handle greetings first
    response = handle_greetings(user_input)
    if response:
        conversation_history.append(f"Bot: {response}")
        return response

    # Check for existing questions and answers
    if last_question:
        response = handle_follow_up_response(last_question, user_input)
        conversation_history.append(f"Bot: {response}")
        last_question = None  # Reset last question after handling
    else:
        response = check_questions(user_input)
        if response:
            conversation_history.append(f"Bot: {response}")
        else:
            # Handle unknown input
            response = handle_unknown_input(user_input)
            conversation_history.append(f"Bot: {response}")

        # Ask follow-up questions (up to three questions)
        for _ in range(3):
            question = ask_follow_up_question()
            if question:
                conversation_history.append(f"Bot: {question}")
                last_question = question  # Remember last asked follow-up question
                break  # Wait for user response before asking next follow-up question

    return response

def send_message():
    """Handles the sending of a message and updating the UI."""
    user_input = entry.get()
    if user_input:
        entry.delete(0, tk.END)
        chat_box.configure(state=tk.NORMAL)
        chat_box.insert(tk.END, "You: " + user_input + "\n")
        bot_response = chatbot_response(user_input)
        chat_box.insert(tk.END, "Bot: " + bot_response + "\n")
        chat_box.configure(state=tk.DISABLED)
        chat_box.yview(tk.END)

# Create the main window
root = tk.Tk()
root.title("Chatbot")

# Create a ScrolledText widget for the chat history
chat_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, state=tk.DISABLED)
chat_box.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Create an entry widget for user input
entry = tk.Entry(root, width=100)
entry.pack(padx=10, pady=10, fill=tk.X, expand=True)
entry.bind("<Return>", lambda event: send_message())

# Create a button to send the message
send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack(pady=10)

# Run the main event loop
root.mainloop()
