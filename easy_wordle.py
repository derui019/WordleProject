# Peter de Ruiter
# CSCI 1913
# Prof. Kluver
# Project 1 - Easy Wordle
# 03/17/2023

import random
import wordle
from words import words


def filter_word_list(word, clues):
    """This function takes the list of words and the list of clues tuples and creates a new list with
    all of the possible words."""
    green_list = get_green_letter(clues)  # calls function to get list of green letters
    grey_list = get_grey_letters(clues)  # calls function to get list of all grey letters
    yellow_tup_list = get_yellow_letter(clues)  # calls function to get list of tuples with yellow letters and indexes
    possible_words_list = []
    new_list = []
    if clues == []:
        return word
    for f in range(len(clues)):  # searches through all of the given clues
        row = clues[f]
        row_guess = row[0]
        row_guess = row_guess.lower()
        row_clue = row[1]
        if row_clue == ["green", "green", "green", "green", "green"]:  # if the word is correct it returns only the word
            possible_words_list.append(row_guess)
            return possible_words_list
    for i in range(len(word)):
        if check_possible(yellow_tup_list, green_list, grey_list, word[i]):  # if the check word function returns
            # true the word is added to the possible word list
            possible_words_list.append(word[i])
    for j in range(len(clues)):  # ensures that none of the guesses are in the possible word list
        clue_row = clues[j]
        row_guess = clue_row[0]
        row_guess = row_guess.lower()
        for k in range(len(possible_words_list)):
            if row_guess != possible_words_list[k]:
                new_list.append(possible_words_list[k])
    possible_words_list = set(new_list)  # turns possible words to a set to remove duplicates
    possible_words_list = list(possible_words_list)
    return possible_words_list


def get_green_letter(clues):
    """This function takes the list of clues and returns a list 0s in the indexes where the letter is
    unknown and the letter in the known indexes"""
    know_letter = ["0", "0", "0", "0", "0"]
    for i in range(len(clues)):  # Searches through all of the clues
        clue_row = clues[i]
        row_guess = clue_row[0]
        row_guess = row_guess.lower()
        row_clue = clue_row[1]
        for j in range(5):  # If a letter is green it is added to the known letter list
            if row_clue[j] == "green":
                know_letter[j] = row_guess[j]
    return know_letter


def get_yellow_letter(clues):
    """This function takes the list of clues and returns a list of tuples that contains both the letter
    and the index of the yellow letter"""
    yellow_letter = []
    for i in range(len(clues)):  # Searches through all of the clues
        clue_row = clues[i]
        row_guess = clue_row[0]
        row_guess = row_guess.lower()
        row_clue = clue_row[1]
        for j in range(5):
            if row_clue[j] == "yellow":  # If a letter is yellow it is added as a tuple with its index to yellow list
                index_num = j
                yellow_letter.append((row_guess[j], index_num))
    yellow_set = set(yellow_letter)  # removes duplicates from the list
    yellow_letter = list(yellow_set)
    return yellow_letter


def get_grey_letters(clues):
    """This function takes a list of clues and returns the list of letter that are not in the word"""
    str_grey = wordle.no_letters(clues)  # this calls the no_letters function from wordle that has all of the grey
    # letters
    str_grey = str_grey.lower()
    lst_grey = []
    for i in range(len(str_grey)):  # each letter is added individually to the list
        lst_grey.append(str_grey[i])
    return lst_grey


def check_possible(yellow_list, green_list, grey_list, word):
    """This function takes the list of green, grey and yellow letters and the word and returns true if valid
    word and false if not a valid word"""
    possible_word = ["false", "false", "false", "false", "false"]
    count = 0
    for q in range(len(grey_list)):  # if any of the grey letters are in word false is returned
        if grey_list[q] in word:
            return False
    for k in range(5):
        if green_list[k] != 0 and green_list[k] == word[k]:  # if the green letter is in the word that index
            possible_word[k] = "true"
        elif green_list[k] == "0":  # if the index of know letter is 0 the possible word index is true
            possible_word[k] = "true"
        else:
            possible_word[k] = "false"
    for nums in range(len(possible_word)):
        if (possible_word[nums]) == "true":  # counts the number of true positions
            count = count + 1
    if count == 5:  # if all five indexes are true then it checks the yellow indexes
        counter = 0
        for k in range(len(yellow_list)):  # Finds all words that contain all of the yellow letter in different indexes
            yellow_words = yellow_list[k]
            yellow_row_letter = str(yellow_words[0])
            yellow_index = yellow_words[1]
            ltr_count = word.count(yellow_row_letter)  # counts the number of the yellow letter in the word
            if ltr_count > 1 and word.find(yellow_row_letter) != -1 and word.find(yellow_row_letter) != yellow_index:  # if there are more the one yellow letter in list
                counter_2 = 0
                start = 0
                for g in range(ltr_count):  # find the indexes of the yellow letters
                    ltr_index = word.find(yellow_row_letter, start, 5)
                    if ltr_index != -1 and ltr_index != yellow_index:
                        counter_2 = counter_2 + 1
                    start = ltr_index + 1
                if counter_2 == ltr_count:  # if all of the indexes are possible 1 is added to counter
                    counter = counter + 1
                else:
                    return False
            elif word.find(yellow_row_letter) != -1 and word.find(yellow_row_letter) != yellow_index and ltr_count <= 1:  # if there is one appearence of the yellow letter it checks that it is in the proper index
                counter = counter + 1
            else:
                return False
        if counter == len(yellow_list):  # if the correct number of yellow letter in the correct indexes are present
            # trues is returned
            return True
    else:
        return False


def take_guess_2(sets):
    """This function takes the list the of words and returns the guess once the inputted gues is valid"""
    print("> ")
    guess1 = input()
    while wordle.valid_word(guess1, sets) == 0:  # Runs until a valid word is inputted
        print("> ")
        guess1 = input()
    guess1 = guess1.upper()
    return guess1


def print_easy_stuff(words_2, clues):
    """This function takes the list of words and the list of clues and print the amount of possible words and 5 random
     words if there are more than 5 possible words or else all possible words are printed"""
    wordle.print_color(clues)
    print(len(filter_word_list(words, clues)), "words possible:")
    lst_4 = filter_word_list(words_2, clues)
    if len(filter_word_list(words_2, clues)) > 5:
        random.shuffle(lst_4)  # shuffles this list so the 5 words are chosen at random
        for a in range(5):  # prints 5 words
            print(lst_4[a])
    else:
        for z in range(len(lst_4)):
            print(lst_4[z])


if __name__ == "__main__":
    set_words = set(words)
    secrets = random.choice(words)  # Chooses a random word from the words list to be the "secret" word
    cluess = []
    for i in range(6):  # The loop takes 6 guesses or until secret word guessed correctly
        guess2 = take_guess_2(words)
        hints = wordle.check_word(secrets, guess2)
        cluess.append((guess2, hints))
        print_easy_stuff(words, cluess)
        guess2 = guess2.upper()
        secrets = secrets.upper()
        if guess2 == secrets:  # If the word is guessed correctly
            print_easy_stuff(words, cluess)
            break
    print("Answer: ", secrets)