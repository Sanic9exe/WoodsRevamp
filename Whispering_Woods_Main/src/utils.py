"""
Utility functions for the game
"""

import os
import sys
import time
import random
import textwrap
from typing import Optional
from .colors import Colors, colored_text


def slow_type(text: str, delay: float = 0.03, color: str = Colors.WHITE):
    """Type text slowly character by character."""
    colored = colored_text(text, color)
    for char in colored:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()


def instant_print(text: str):
    """Print text instantly."""
    print(text)


def clear_screen():
    """Clear the screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def get_input(prompt: str = "> ") -> str:
    """Get user input with a prompt."""
    return input(colored_text(prompt, Colors.CYAN))


def get_number_input(prompt: str, min_val: int = None, max_val: int = None) -> Optional[int]:
    """Get numeric input from user with validation."""
    while True:
        try:
            user_input = get_input(prompt)
            number = int(user_input)
            
            if min_val is not None and number < min_val:
                instant_print(colored_text(f"Please enter a number at least {min_val}.", Colors.RED))
                continue
            if max_val is not None and number > max_val:
                instant_print(colored_text(f"Please enter a number no more than {max_val}.", Colors.RED))
                continue
            
            return number
        except ValueError:
            instant_print(colored_text("Please enter a valid number.", Colors.RED))
            continue


def roll_dice(sides: int = 6, num_dice: int = 1) -> int:
    """Roll dice and return the result."""
    return sum(random.randint(1, sides) for _ in range(num_dice))


def press_enter_to_continue():
    """Wait for user to press Enter."""
    input(colored_text("\nPress Enter to continue...", Colors.DIM))


def format_stat_bar(current: int, maximum: int, length: int = 20, filled_char: str = "█", empty_char: str = "░") -> str:
    """Create a visual stat bar."""
    filled = int((current / maximum) * length)
    empty = length - filled
    return f"{filled_char * filled}{empty_char * empty}"


def format_health_bar(current: int, maximum: int) -> str:
    """Create a colored health bar."""
    bar = format_stat_bar(current, maximum)
    percentage = current / maximum
    
    if percentage > 0.6:
        color = Colors.GREEN
    elif percentage > 0.3:
        color = Colors.YELLOW
    else:
        color = Colors.RED
    
    return colored_text(bar, color) + f" {current}/{maximum}"


def format_list_numbered(items: list, color: str = Colors.WHITE) -> str:
    """Format a list of items with numbers."""
    output = []
    for i, item in enumerate(items, 1):
        output.append(colored_text(f"{i}. {item}", color))
    return "\n".join(output)


def confirm_choice(prompt: str = "Are you sure?") -> bool:
    """Ask for yes/no confirmation."""
    while True:
        response = get_input(f"{prompt} (y/n): ").lower()
        if response in ['y', 'yes']:
            return True
        elif response in ['n', 'no']:
            return False
        else:
            instant_print(colored_text("Please enter 'y' or 'n'.", Colors.YELLOW))


def display_title():
    """Display the game title."""
    title = """
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║        LOST IN THE WHISPERING WOODS                       ║
║        A Text-Based Adventure Game                        ║
║                                                           ║
║        Version 2.0 - Revamped Edition                     ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
    """
    instant_print(colored_text(title, Colors.BOLD_CYAN))


def display_separator(char: str = "=", length: int = 60, color: str = Colors.CYAN):
    """Display a separator line."""
    instant_print(colored_text(char * length, color))


def wrap_text(text: str, width: int = 70) -> str:
    """Wrap text to a specific width."""
    return textwrap.fill(text, width=width)


def pause(duration: float):
    """Pause for a specified duration."""
    time.sleep(duration)
