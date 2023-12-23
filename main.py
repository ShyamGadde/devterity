import curses
import json
import random
import time

from prettytable import PrettyTable


def main(stdscr):
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_GREEN, -1)
    curses.init_pair(2, curses.COLOR_RED, -1)
    curses.init_pair(3, curses.COLOR_YELLOW, -1)
    curses.init_pair(4, curses.COLOR_BLUE, -1)

    assci_art = """
     ___           __          _ __
    / _ \___ _  __/ /____ ____(_) /___ __
   / // / -_) |/ / __/ -_) __/ / __/ // /
  /____/\__/|___/\__/\__/_/ /_/\__/\_, /
                                  /___/ """

    stdscr.clear()
    stdscr.addstr(1, 1, assci_art, curses.color_pair(4) | curses.A_BOLD)
    stdscr.refresh()

    subwin = stdscr.derwin(10, 2)
    subwin.addstr("Welcome to ")
    subwin.addstr("Devterity!", curses.color_pair(3))
    subwin.addstr("\n\nPlease enter your username: ")
    subwin.refresh()

    username = get_user_input(subwin)

    while True:
        subwin.clear()
        subwin.addstr("\n1. Start Typing Test")
        subwin.addstr("\n2. View Leaderboard")
        subwin.addstr("\n3. Exit")
        subwin.addstr("\n\n# [1/2/3]: ")
        subwin.refresh()

        choice = get_user_input(subwin)

        if choice == "1":
            target_text = generate_test_string(subwin)
            wpm_test(subwin, username, target_text)
        elif choice == "2":
            display_leaderboard(subwin)
        elif choice == "3":
            break
        else:
            subwin.addstr(6, 0, "Invalid choice!")
            subwin.refresh()
            time.sleep(1)


def get_user_input(stdscr):
    curses.echo()
    user_input = stdscr.getstr().decode("utf-8")
    curses.noecho()
    return user_input


def wpm_test(stdscr, username, target_text):
    current_text = []
    wpm = 0
    accuracy = 100
    start_time = time.time()

    while True:
        wpm = calculate_wpm(start_time, current_text)
        accuracy = calculate_accuracy(target_text, current_text)

        update_window(stdscr, target_text, current_text, wpm, accuracy)

        if len(current_text) == len(target_text):
            update_leaderboard(username, wpm, accuracy)
            stdscr.addstr(4, 0, "Completed!")
            stdscr.addstr(5, 0, "Press any TAB to retry or any key to exit to menu...")
            key = stdscr.getkey()
            if key == "\t":
                wpm_test(stdscr, username, target_text)
            break

        key = stdscr.getkey()

        if key in ("KEY_BACKSPACE", "\b", "\x7f") and current_text:
            current_text.pop()
        elif len(current_text) < len(target_text):
            if ord(key) == 27:
                stdscr.addstr(4, 0, "Exiting...")
                stdscr.refresh()
                time.sleep(0.5)
                break

            current_text.append(key)


def display_leaderboard(stdscr):
    stdscr.clear()
    stdscr.addstr("Leaderboard\n\n", curses.A_UNDERLINE | curses.color_pair(3))

    table = PrettyTable()
    table.field_names = ["Username", "WPM", "Accuracy"]

    try:
        with open("leaderboard.json") as f:
            data = list(json.load(f).items())
            sorted_data = sorted(
                data, key=lambda x: (x[1]["wpm"], x[1]["accuracy"]), reverse=True
            )

            for name, stats in sorted_data:
                table.add_row([name, stats["wpm"], stats["accuracy"]])

            stdscr.addstr(table.get_string())
    except FileNotFoundError:
        stdscr.addstr("The leaderboard is empty!\n")

    stdscr.addstr("\n\nPress any key to continue...")
    stdscr.refresh()
    stdscr.getkey()


def generate_test_string(stdscr):
    category = select_category(stdscr)
    words = load_words(category)
    random.shuffle(words)
    return " ".join(words[:20])


def calculate_wpm(start_time, current_text):
    time_elapsed = max(time.time() - start_time, 1)
    return round(len(current_text) / 5 / (time_elapsed / 60))


def calculate_accuracy(target: str, current: list):
    incorrect_chars = sum(c != target[i] for i, c in enumerate(current))
    return round((1 - incorrect_chars / (len(current) or 1)) * 100)


def update_window(stdscr, target: str, current: list, wpm=0, accuracy=100):
    stdscr.clear()

    stdscr.addstr(0, 0, f"WPM: {wpm}\t\tAccuracy: {accuracy}%", curses.color_pair(3))
    stdscr.addstr(2, 0, target)

    for i, c in enumerate(current):
        color = 1
        if c != target[i]:
            color = 2
            # Replace incorrect whitespace with underscore
            if c == " ":
                c = "_"
        stdscr.addstr(2, i, c, curses.color_pair(color))

    stdscr.refresh()


def update_leaderboard(username: str, wpm: int, accuracy: int):
    try:
        with open("leaderboard.json") as f:
            leaderboard = json.load(f)
    except FileNotFoundError:
        leaderboard = {}

    if username not in leaderboard or wpm >= leaderboard[username]["wpm"]:
        leaderboard[username] = {"wpm": wpm, "accuracy": accuracy}

    with open("leaderboard.json", "w") as f:
        json.dump(leaderboard, f, indent=2)


def select_category(stdscr):
    categories = load_categories()
    while True:
        stdscr.clear()
        stdscr.addstr("Choose a category:\n\n")
        for i, category in enumerate(categories, start=1):
            stdscr.addstr(f"{i}. {category}\n")
        stdscr.addstr("\n# Enter category name: ")
        stdscr.refresh()
        category = get_user_input(stdscr)

        if category in categories:
            break
        stdscr.addstr(len(categories) + 5, 0, "Invalid category!")
        stdscr.refresh()
        time.sleep(1)

    return category


def load_categories():
    with open("words.json") as f:
        return list(json.load(f).keys())


def load_words(category: str):
    with open("words.json") as f:
        return json.load(f)[category]


if __name__ == "__main__":
    curses.wrapper(main)
