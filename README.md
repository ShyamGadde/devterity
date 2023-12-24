# Devterity



https://github.com/ShyamGadde/devterity/assets/73636812/e85fdb98-36eb-4393-ba79-adb73ac2aaab



## Description

Welcome to Devterity, a unique blend of a typing test and a programming language drill designed to help you improve your typing speed and accuracy with _programming keywords_. This command-line interface (CLI) application is not your traditional typing test. It’s specifically tailored for programmers who want to enhance their coding speed and precision.

Upon launching Devterity, you’re greeted with a warm welcome message and prompted to enter your username. The main menu then presents three options: Start Typing Test, View Leaderboard, and Exit. Choosing to start the typing test triggers the generation of a test string. A _category_ (a specific programming language) is selected and the corresponding keywords are loaded. The keywords are then shuffled and a subset is selected to form the target text for the typing test. This dynamic generation of test strings ensures a fresh challenge every time.

The heart of Devterity is the `wpm_test` function. It calculates words per minute (WPM) and accuracy in real-time, providing immediate feedback. The function also handles user input, accommodating backspaces and escape sequences. The color-coded feedback for correct and incorrect keystrokes enhances the user experience and facilitates learning.

Devterity also features a **leaderboard** that maintains a record of the users’ performances, storing the best WPM and accuracy for each user. The leaderboard is displayed in a well-structured table, making it easy for users to compare their performance with others. This element of competition can motivate users to improve their typing skills.

The `leaderboard.json` file is used to store the leaderboard data. This file contains the usernames of users along with their best WPM and accuracy scores. The `words.json` file contains a list of words that are used to generate the typing tests.

In summary, Devterity is a comprehensive and engaging typing test application tailored for programmers. Its focus on programming keywords, real-time performance feedback, and competitive leaderboard make it a valuable tool for anyone looking to improve their coding efficiency.
