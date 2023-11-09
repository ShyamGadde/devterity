import curses
import json
import random
import time

username = "Guest"


def get_input(stdscr):
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
    username = get_input(stdscr)


def display_menu(stdscr):
    while True:
        stdscr.clear()
        stdscr.addstr("\n1. Start Typing Test")
        stdscr.addstr("\n2. View Leaderboard")
        stdscr.addstr("\n3. Exit")
        stdscr.addstr("\n\n# [1/2/3]: ")
        stdscr.refresh()

        choice = get_input(stdscr)

        if choice == "1":
            wpm_test(stdscr)
        elif choice == "2":
            show_leaderboard(stdscr)
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


def show_leaderboard(stdscr):
    stdscr.clear()
    stdscr.addstr("Leaderboard\n\n")

    try:
        with open("leaderboard.json") as f:
            stdscr.addstr("\tUsername\t\tWPM\n", curses.color_pair(3))
            leaderboard = json.load(f)
            for i, (username, wpm) in enumerate(
                sorted(leaderboard.items(), key=lambda entry: entry[1], reverse=True),
                start=1,
            ):
                stdscr.addstr(f"{i}.\t{username}\t\t\t{wpm} WPM\n")
    except FileNotFoundError:
        stdscr.addstr("The leaderboard is empty!\n")

    stdscr.addstr("\n\nPress any key to continue...")
    stdscr.refresh()
    stdscr.getkey()


def update_leaderboard(wpm: int):
    try:
        with open("leaderboard.json") as f:
            leaderboard = json.load(f)
    except FileNotFoundError:
        leaderboard = {}

    if username in leaderboard:
        leaderboard[username] = max(leaderboard[username], wpm)
    else:
        leaderboard[username] = wpm

    with open("leaderboard.json", "w") as f:
        json.dump(leaderboard, f, indent=2)


def display_text(stdscr, target: str, current: list, wpm=0):
    stdscr.addstr(2, 0, target)
    incorrect_chars = 0

    for i, c in enumerate(current):
        correct_c = target[i]
        color = 1
        if c != correct_c:
            incorrect_chars += 1
            color = 2
            # Replace incorrect whitespace with underscore
            if c == " ":
                c = "_"
        stdscr.addstr(2, i, c, curses.color_pair(color))

    accuracy = round((1 - incorrect_chars / (len(current) or 1)) * 100)
    stdscr.addstr(0, 0, f"WPM: {wpm}\t\tAccuracy: {accuracy}%", curses.color_pair(3))


def wpm_test(stdscr):
    categories = load_categories()
    while True:
        stdscr.clear()
        stdscr.addstr("Choose a category:\n\n")
        for i, category in enumerate(categories, start=1):
            stdscr.addstr(f"{i}. {category}\n")
        stdscr.addstr("\n# Enter category name: ")
        stdscr.refresh()
        category = get_input(stdscr)

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
    start_time = time.time()
    stdscr.nodelay(True)

    while True:
        time_elapsed = max(time.time() - start_time, 1)
        wpm = round(len(current_text) / 5 / (time_elapsed / 60))

        stdscr.clear()
        display_text(stdscr, target_text, current_text, wpm)
        stdscr.refresh()

        if "".join(current_text) == target_text:
            update_leaderboard(wpm)
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
            break

        if key in ("KEY_BACKSPACE", "\b", "\x7f") and current_text:
            current_text.pop()
        elif len(current_text) < len(target_text):
            current_text.append(key)


def main(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    start_screen(stdscr)
    display_menu(stdscr)


if __name__ == "__main__":
    curses.wrapper(main)
