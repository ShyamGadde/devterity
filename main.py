import curses
import json
import random
import time

username = "Guest"


def get_user_input(stdscr):
    curses.echo()
    user_input = stdscr.getstr().decode("utf-8")
    curses.noecho()
    return user_input


def start_screen(stdscr):
    stdscr.clear()
    stdscr.addstr("Welcome to ")
    stdscr.addstr("Devterity!", curses.color_pair(3))
    stdscr.addstr("\n\nPlease enter your username: ")
    stdscr.refresh()

    global username
    username = get_user_input(stdscr)


def display_menu(stdscr):
    while True:
        stdscr.clear()
        stdscr.addstr("\n1. Start Typing Test")
        stdscr.addstr("\n2. View Leaderboard")
        stdscr.addstr("\n3. Exit")
        stdscr.addstr("\n\n# [1/2/3]: ")
        stdscr.refresh()

        choice = get_user_input(stdscr)

        if choice == "1":
            wpm_test(stdscr)
        elif choice == "2":
            display_leaderboard(stdscr)
        elif choice == "3":
            break
        else:
            stdscr.addstr(6, 0, "Invalid choice!")
            stdscr.refresh()
            time.sleep(1)


def load_categories():
    with open("words.json") as f:
        return list(json.load(f).keys())


def load_words(category: str):
    with open("words.json") as f:
        return json.load(f)[category]


def display_leaderboard(stdscr):
    stdscr.clear()
    stdscr.addstr("Leaderboard\n\n")

    try:
        with open("leaderboard.json") as f:
            stdscr.addstr("\tUsername\t\tWPM\t\tAccuracy\n", curses.color_pair(3))
            data = list(json.load(f).items())
            sorted_data = sorted(
                data, key=lambda x: (x[1]["wpm"], x[1]["accuracy"]), reverse=True
            )

            for name, stats in sorted_data:
                stdscr.addstr(
                    f"\t{name}\t\t\t{stats['wpm']} WPM\t\t{stats['accuracy']}\n"
                )
    except FileNotFoundError:
        stdscr.addstr("The leaderboard is empty!\n")

    stdscr.addstr("\n\nPress any key to continue...")
    stdscr.refresh()
    stdscr.getkey()


def update_leaderboard(wpm: int, accuracy: int):
    try:
        with open("leaderboard.json") as f:
            leaderboard = json.load(f)
    except FileNotFoundError:
        leaderboard = {}

    if username not in leaderboard or wpm >= leaderboard[username]["wpm"]:
        leaderboard[username] = {"wpm": wpm, "accuracy": accuracy}

    with open("leaderboard.json", "w") as f:
        json.dump(leaderboard, f, indent=2)


def calculate_accuracy(target: str, current: list):
    incorrect_chars = sum(c != target[i] for i, c in enumerate(current))
    return round((1 - incorrect_chars / (len(current) or 1)) * 100)


def update_window(stdscr, target: str, current: list, wpm=0, accuracy=100):
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

    return accuracy


def wpm_test(stdscr):
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

    words = load_words(category)
    random.shuffle(words)
    target_text = " ".join(words[:20])

    current_text = []
    wpm = 0
    accuracy = 100
    start_time = time.time()
    stdscr.nodelay(True)

    while True:
        time_elapsed = max(time.time() - start_time, 1)
        wpm = round(len(current_text) / 5 / (time_elapsed / 60))
        accuracy = calculate_accuracy(target_text, current_text)

        stdscr.clear()
        update_window(stdscr, target_text, current_text, wpm, accuracy)
        stdscr.refresh()

        if len(current_text) == len(target_text):
            update_leaderboard(wpm, accuracy)
            stdscr.addstr(4, 0, "Completed!")
            stdscr.addstr(5, 0, "Press any key to continue...")
            stdscr.nodelay(False)
            stdscr.getkey()
            break

        try:
            key = stdscr.getkey()
        except Exception:
            continue

        if ord(key) == 27:
            stdscr.addstr(4, 0, "Exiting...")
            stdscr.refresh()
            time.sleep(0.5)
            break

        if key in ("KEY_BACKSPACE", "\b", "\x7f") and current_text:
            current_text.pop()
        elif len(current_text) < len(target_text):
            current_text.append(key)


def main(stdscr):
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_GREEN, -1)
    curses.init_pair(2, curses.COLOR_RED, -1)
    curses.init_pair(3, curses.COLOR_YELLOW, -1)

    start_screen(stdscr)
    display_menu(stdscr)


if __name__ == "__main__":
    curses.wrapper(main)
