import os

def clear():
    """
    Clear the console screen.
    """
    os.system('cls' if os.name == 'nt' else 'clear')