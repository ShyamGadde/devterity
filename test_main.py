from unittest.mock import MagicMock, mock_open, patch

import pytest

from main import (
    calculate_accuracy,
    generate_test_string,
    get_user_input,
    update_leaderboard,
)


@pytest.fixture
def mock_json_load():
    with patch("json.load") as mock_json:
        yield mock_json


@pytest.fixture
def mock_json_dump():
    with patch("json.dump") as mock_json:
        yield mock_json


@pytest.fixture
def mock_open_file():
    with patch("builtins.open", new_callable=mock_open) as mock_file:
        yield mock_file


def test_update_leaderboard_new_user(mock_json_load, mock_json_dump, mock_open_file):
    mock_json_load.return_value = {}
    username = "test_user"
    wpm = 100
    accuracy = 90

    update_leaderboard(username, wpm, accuracy)

    mock_open_file.assert_any_call("leaderboard.json")
    mock_json_dump.assert_called_once_with(
        {username: {"wpm": wpm, "accuracy": accuracy}}, mock_open_file(), indent=2
    )


def test_update_leaderboard_existing_user_higher_wpm(
    mock_json_load, mock_json_dump, mock_open_file
):
    username = "test_user"
    wpm = 100
    accuracy = 90
    mock_json_load.return_value = {username: {"wpm": 80, "accuracy": 85}}

    update_leaderboard(username, wpm, accuracy)

    mock_open_file.assert_any_call("leaderboard.json")
    mock_json_dump.assert_called_once_with(
        {username: {"wpm": wpm, "accuracy": accuracy}}, mock_open_file(), indent=2
    )


@patch("curses.echo")
@patch("curses.noecho")
def test_get_user_input(mock_noecho, mock_echo):
    mock_stdscr = MagicMock()
    mock_stdscr.getstr.return_value = b"test_input"

    result = get_user_input(mock_stdscr)

    mock_echo.assert_called_once()
    mock_noecho.assert_called_once()
    mock_stdscr.getstr.assert_called_once()
    assert result == "test_input"


@patch("main.select_category")
@patch("main.load_words")
@patch("random.shuffle")
def test_generate_test_string(mock_shuffle, mock_load_words, mock_select_category):
    mock_stdscr = MagicMock()
    mock_select_category.return_value = "category"
    mock_load_words.return_value = [
        "word1",
        "word2",
        "word3",
        "word4",
        "word5",
        "word6",
        "word7",
        "word8",
        "word9",
        "word10",
        "word11",
        "word12",
        "word13",
        "word14",
        "word15",
        "word16",
        "word17",
        "word18",
        "word19",
        "word20",
        "word21",
    ]

    result = generate_test_string(mock_stdscr)

    mock_select_category.assert_called_once_with(mock_stdscr)
    mock_load_words.assert_called_once_with("category")
    mock_shuffle.assert_called_once_with(mock_load_words.return_value)
    words_in_result = result.split(" ")
    assert len(words_in_result) == 20
    assert set(words_in_result).issubset(set(mock_load_words.return_value))


@pytest.mark.parametrize(
    "target, current, expected",
    [
        ("hello", ["h", "e", "l", "l", "o"], 100),
        ("hello", ["h", "e", "l", "l", "p"], 80),
        ("hello", ["h", "e", "l", "l"], 100),
        ("hello", [], 100),
    ],
)
def test_calculate_accuracy(target, current, expected):
    assert calculate_accuracy(target, current) == expected
