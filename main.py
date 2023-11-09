import curses
import time


def start_screen(stdscr):
    stdscr.clear()
    stdscr.addstr("Welcome to Devterity!")
    stdscr.addstr("\nPress any key to start typing.")
    stdscr.refresh()
    stdscr.getkey()


def display_text(stdscr, target: str, current: list, wpm=0):
    stdscr.addstr(target)
    stdscr.addstr(2, 0, f"WPM: {wpm}")

    for i, c in enumerate(current):
        correct_c = target[i]
        color = 1
        if c != correct_c:
            color = 2
            if c == " ":
                c = "_"
        stdscr.addstr(0, i, c, curses.color_pair(color))


def wpm_test(stdscr):
    target_text = "The quick brown fox jumps over the lazy dog"
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
            stdscr.nodelay(False)
            break

        try:
            key = stdscr.getkey()
        except Exception:
            continue

        if ord(key) == 27:
            break

        if key in ("KEY_BACKSPACE", "\b", "\x7f") and current_text:
            current_text.pop()
        elif len(current_text) < len(target_text):
            current_text.append(key)


def main(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

    start_screen(stdscr)

    while True:
        wpm_test(stdscr)
        stdscr.addstr(4, 0, "Completed!\nPress any key to continue or ESC to exit.")
        key = stdscr.getkey()

        if ord(key) == 27:
            break


if __name__ == "__main__":
    curses.wrapper(main)
