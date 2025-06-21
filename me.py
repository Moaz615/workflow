import os 
os.system('cls')
print("Welcome to the Hangman Game!")
import random
def get_word():
    words = ["python", "hangman", "challenge", "programming", "developer"]
    return random.choice(words).upper()