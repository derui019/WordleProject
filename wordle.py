# Peter de Ruiter
# CSCI 1913
# Prof. Kluver
# Project 1 - Wordle
# 03/17/2023

from words import words
import random
import display_utility


def check_word(secret, guess):
    """This function takes the parameters of two strings, one being the secret word the other being
    the word that was guessed, the function creates a list that stores green in the position's of the
    list that match and stores yellow in the list for all indexes where the letter is contained in the
    secret word but not at that position, all other indexes are assigned "grey". The function returns
    the list of hints."""
    hint = ["grey", "grey", "grey", "grey", "grey"]
    secret_clue = [2, 2, 2, 2, 2]
    guess = guess.lower()
    secret = secret.lower()
    for i in range(5):  # loop checks if the letters at the indexes match and assignd "green" if true
        if secret[i] == guess[i]:
            hint[i] = "green"
            secret_clue[i] = 3
    for j in range(5):  # loop checks if letter exists in list and is not "green" or "yellow" assigns "yellow" if true
        for i in range(5):
            if secret_clue[j] == 2:
                if guess[i] == secret[j] and hint[i] != "green":
                    hint[i] = "yellow"
                    secret_clue[j] = 3
    return hint


def known_word(clues):
    """This function takes a list of tuples that contain both the guess and the clue, the function
    uses all known letters to return a string of the word know so far with '_' representing
    positions not yet known."""
    known = ["_"] * 5
    for i in range(len(clues)):
        clue_row = clues[i]
        row_guess = clue_row[0]
        row_clue = clue_row[1]
        for j in range(5):
            if row_clue[j] == "green":
                known[j] = row_guess[j]
    known_wrd = "".join(known)  # turns a list into a string
    return known_wrd


def no_letters(clues):
    """This function takes a list of tuples containg the previous guess and hint and creates a list
       of the letters that are know to not be in the secret word, the function returns all unique letters
       know to not be in the list and returns them as a string of letter in alphabetical order and uppercase"""
    all_letters = []
    yes_string = yes_letters(clues)
    yes_list = []
    yes_list[:0] = yes_string
    for nums in range(len(clues)):  # This loop creates a list of all letters
        clue_row = clues[nums]
        row_guess = clue_row[0]
        row_clue = clue_row[1]
        for j in range(5):
            all_letters.append(row_guess[j])
    unique_list = []
    for ltr in all_letters:  # This loop filters out all identical letter so all letters appear in the list only once
        if ltr not in unique_list:
            unique_list.append(ltr)
    unique_list.sort()  # This method sorts the list
    for i in range(len(yes_list)):  # This loops removes all known letters from the list of letters
        unique_list.remove(yes_list[i])
    str_no = "".join(unique_list)  # This method turns the list into a string of letters
    return str_no


def yes_letters(clues):
    """This function takes a list of tuples contains the previous guesses and hints and returns
    a string of all of the known/"green" or "yellow" letters alphabetically"""
    yes_list = []
    for i in range(len(clues)):  # This function adds all of the "green" and "yellow" letters to a list
        clue_row = clues[i]
        row_guess = clue_row[0]
        row_clue = clue_row[1]
        for j in range(5):
            if row_clue[j] == "green" or row_clue[j] == "yellow":
                yes_list.append(row_guess[j])
    unique_list = []
    for ltr in yes_list:  # This function removes all duplicate letters from the list
        if ltr not in unique_list:
            unique_list.append(ltr)
    unique_list.sort()  # This method sorts the list alphabetically
    str_yes = "".join(unique_list)  # This turns the list of letters into a string
    return str_yes


def valid_word(guess, sets):
    """This function takes the guess and the set of all valid 5-letter words from words.py and determines
    if the guess is a valid word, the function returns 0 if invalid word 1 if valid"""
    if len(guess) != 5:  # Checks if there are 5 letters in the guess
        return 0
    guess = guess.lower()
    if guess in sets:  # Checks if the guess is a word in the set of words
        return 1
    else:
        return 0


def take_guess(sets, clues):
    """This function takes prints the statements and values required for the project and takes the input
    of the guess, the function returns the guess once the guess is determined to be valid"""
    print("Known: " + known_word(clues))
    print("Green/Yellow Letters: " + yes_letters(clues))
    print("Grey Letters: " + no_letters(clues))
    print_color(clues)
    print("> ")
    guess1 = input()
    while valid_word(guess1, sets) == 0:  # Runs until a valid word is inputted
        print("> ")
        guess1 = input()
    guess1 = guess1.upper()
    return guess1


def print_color(clues):
    """This function takes the list of clues and prints the letters in the correct colors
    using the functions from display_utility provided to us."""
    for num in range(len(clues)):
        clue_row = clues[num]
        row_guess = clue_row[0]
        row_guess = row_guess.upper()
        row_clue = clue_row[1]
        for j in range(5):  # This loop determines the color the letter needs to be and prints in in that color
            if row_clue[j] == "green":
                display_utility.green(row_guess[j])
            elif row_clue[j] == "yellow":
                display_utility.yellow(row_guess[j])
            else:
                display_utility.grey(row_guess[j])
        print()


if __name__ == "__main__":
    set_words = set(words)
    secrets = random.choice(words)  # Chooses a random word from the words list to be the "secret" word
    cluess = []
    for i in range(6):  # The loop takes 6 guesses or until secret word guessed correctly
        guess2 = take_guess(set_words, cluess)
        hints = check_word(secrets, guess2)
        cluess.append((guess2, hints))
        guess2 = guess2.upper()
        secrets = secrets.upper()
        if guess2 == secrets:  # If the word is guessed correctly
            print("Known: " + known_word(cluess))
            print("Green/Yellow Letters: " + yes_letters(cluess))
            print("Grey Letters: " + no_letters(cluess))
            print_color(cluess)
            break
    print("Answer: ", secrets)