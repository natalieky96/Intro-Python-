#################################################################
# FILE : quadratic_equation.py
# WRITER : natalie_kern_iacob
# EXERCISE : intro2cse ex4 2020
# DESCRIPTION: The program is a variation of the 'hangman' game.
# WEB PAGES I USED: None.
# NOTES: None.
#################################################################
import hangman_helper as hp

DISPLAY_MESSAGE = "Try to save the HANGMAN!"
WRONG_INPUT = "invalid/already guessed letter, Please try again:"
ALREADY_GUESSED = "This letter was already guessed, Try again:"
OK_CHOICE = "Great Choice!"
WRONG_LETTER = "Wrong letter!"
CORRECT_WORD = "You guessed the right word!"
TIMES_SCORE_PLAY_AGAIN = "You played {} times, and your score is {}. Would " \
                         "you like to play again?"
YOU_WON = "Congratulations, You won!"
YOU_LOST = "Sorry, You lost!"
BLANK = '_'


def update_word_pattern(word, pattern, letter):
    """Gets a pattern, word and letter and returns an updated pattern.
    :param word: The word the player suppose to guess.
    :param pattern: The pattern of the unfilled word.
    :param letter: The letter that suppose to fill the word
    :return: Updated pattern, with the new filled letters at the right places.
    """
    # Making a list from the word so we'll be able to access it
    list_word = list(word)
    # Making a list from the pattern so we'll be able to change it
    list_pattern = list(pattern)
    # Saves the indexes of where the letter appears in the word
    idx_letter = [i for i, x in enumerate(list_word) if x == letter]
    # Insert the letters ("counter_letter" times) to the pattern
    for j in idx_letter:
        # Enter according to the j time in the idx_letter list
        list_pattern[j] = letter
    return "".join(list_pattern)


def valid_letter(the_letter):
    """Check if the letter is ok, if it's one letter and lowercase
    :param the_letter: The letter
    :return: True if it's ok, otherwise False
    """
    if the_letter.isalpha() and the_letter.islower() and len(the_letter) == 1:
        return True
    return False


def repeated_letter(the_letter, wrong_letters, pattern):
    """Check if the letter was already guessed
    :param wrong_letters: List of the wrong guessed words
    :param the_letter: The letter we want to check on
    :param pattern: The curent pattern
    :return: True if it was already guessed, otherwise False
    """
    if the_letter in wrong_letters or the_letter in pattern:
        return True
    return False


def right_letter(the_word, ok_letter, scores, pattern):
    """The letter is in the word, we update the pattern,
    calculate and return the new score
    :param the_word: the word the user suppose to guess
    :param ok_letter: A valid letter
    :param scores: The updated scores until now
    :param pattern: the updated pattern until now
    :return: 2 values: the new score and the new pattern
    """
    # Update the word's pattern with the new letters
    pattern = update_word_pattern(the_word, pattern, ok_letter)
    # Count the number of times the letter appears in the word
    n = the_word.count(ok_letter)
    # Adding to the current score n n*(n+1)//2 points
    scores += (n*(n+1)//2)
    return scores, pattern


def right_word(score, pattern):
    """Added the score points according to the number of letters were guessed
    :param score: The current score
    :param pattern: the current pattern
    :return: The new score the player gained
    """
    # n the number of letter which were discovered until now
    n = pattern.count(BLANK)
    # Adding to the current score n n*(n+1)//2 points
    score += (n*(n+1)//2)
    return score


def word_close_pattern(word_list, pattern):
    """Filter the words that equal to the pattern according to the showing
    letters
    :param word_list: The words list we filter from
    :param pattern: The pattern that we compare to
    :return: a new filtered list
    """
    is_valid = True  # helps us to see that all the letters are ok
    filtered_list = []  # Saving the words that similar to the pattern
    # Going through the words in the list
    for idx in word_list:
        # Going through the letter in the pattern
        for idx2 in range(len(pattern)):
            # Check that the letter isn't empty
            if pattern[idx2] != BLANK:
                if idx[idx2] != pattern[idx2]:
                     is_valid = False
            # If it isn't empty and isn't equal go the the next word
            if is_valid == False:
                break
            # Add the word that passed all the test to the list
        if is_valid:
            filtered_list.append(idx)
        is_valid = True
    return filtered_list


def doesnt_show_more(word_list, pattern):
    """Filter the word list the words that included more letter than
    suppose to according to the shown letters in the pattern.
    :param word_list: The list we want to filter from
    :param pattern: The updated pattern
    :return: a new filtered list
    """
    # For example, if the pattern is "a__l_", all the words that the letter 'a'
    # appears more than once will be filtered.'
    new_filter_list = []  # The list into we'll save the ok words
    # Passes all the letters that aren't '_' in the pattern
    for j in word_list:
        for i in range(len(pattern)):
            if pattern[i] != BLANK:
                if pattern.count(pattern[i]) != j.count(pattern[i]):
                    break
        # Add the word that passed all the test to the list
            new_filter_list.append(j)
    return new_filter_list


def wrong_letter_not_appear(list_word, wrong_letter):
    """Filter the words that includes the letters from the wrong letters list
    :param list_word: list of words
    :param wrong_letter: list of wrong guessed letters
    :return: a new list without the words with the letters from the wrong
    letters list
    """
    new_ok_list = []  # The list into we'll save the ok words
    for i in list_word:
        for j in wrong_letter:
            # If the letter wasn't found in the word the function returns -1
            if i.find(j) != -1:
                break
        new_ok_list.append(i)
    return new_ok_list


def filter_words_list(words, pattern, wrong_guess_lst):
    """Get a list and filtered it according to several conditions.
    :param words: The list of words
    :param pattern: The current pattern
    :param wrong_guess_lst: wrong guessed letter list
    :return: A new list of words that fit to the pattern and to the conditions.
    """
    # You can read the conditions in these functions documentation:
    # word_close_pattern, doesnt_show_more, wrong_letter_not_appear
    fit_words = []  # List that saves the fit words
    pattern_len = len(pattern)
    for i in words:
        if len(i) == pattern_len:
            fit_words.append(i)
    fit_words = word_close_pattern(fit_words, pattern)
    fit_words = doesnt_show_more(fit_words, pattern)
    fit_words = wrong_letter_not_appear(fit_words, wrong_guess_lst)
    return fit_words


def hint_list(full_list, pattern, wrong_guess_lst):
    """filtered a list and return a new list with HINT_LENGTH items.
    :param full_list: The full list
    :param pattern: The current pattern
    :param wrong_guess_lst: wrong guessed letter list
    :return: A new list with HINT_LENGTH items
    """
    # The words will be chosen by this formula,
    # The index of the chosen words are: n is the length of the "full_list"
    # 0, n//HINT_LENGTH, 2*n//HINT_LENGTH, …, (HINT_LENGTH - 1)*n//HINT_LENGTH
    # filter the list according the conditions (for more info, go to the
    # filter_words_list function.
    full_list = filter_words_list(full_list, pattern, wrong_guess_lst)
    new_list = []  # The returned list with HINT_LENGTH items
    n = len(full_list)  # n is the length of the "full_list"
    if n <= hp.HINT_LENGTH:
        return full_list
    for i in range(hp.HINT_LENGTH):
        new_list.append(full_list[i*n//hp.HINT_LENGTH])
    return new_list


def word_chosen(score, user_word, the_word, pattern):
    """What will happen if the user chose to guess a words.
    :param score: The current score
    :param user_word: The word the user tried to guess
    :param the_word: The real word
    :param pattern: the current pattern
    :return: the new score and the correct message
    """
    # Because it is a guess -1 points
    score -= 1
    # If the guess word is right
    if user_word == the_word:
        # Add these points to the score
        score = right_word(score, pattern)
    return score, CORRECT_WORD


def letter_chosen(score, word, user_letter, pattern, wrong_letters):
    """What happens if the user chose to guess a letter.
    :param score: The current score
    :param word: the word
    :param user_letter: The user's letter
    :param pattern: the current pattern
    :param wrong_letters: The guessed wrong letters list
    :return: The new score, the current pattern and the message to the user
    """
    score -= 1
    # If the letter appears in the word do the following:
    if not (word.find(user_letter) == -1):
        score, pattern = right_letter(word, user_letter, score, pattern)
        current_message = OK_CHOICE
    # If not do that:
    else:
        # Add the letter to the wrong guess letter list
        wrong_letters.append(user_letter)
        current_message = WRONG_LETTER

    return score, pattern, current_message


def win_or_lose(pattern, wrong_guess_lst, points):
    """Decides if the player won or lost and according to that print a
    message and his current details: (the parmeters above):
    :param pattern: The current pattern
    :param wrong_guess_lst: The current wrong_guess_lst
    :param points: The current points
    :param msg: A message that say if the player won or not
    :return: None
    """
    if points > 0:
        hp.display_state(pattern, wrong_guess_lst, points, YOU_WON)
    else:
        hp.display_state(pattern, wrong_guess_lst, points, YOU_LOST)


def run_single_game(words_list, score):
    """Run a single game of the hangman.
    :param words_list: The word list from we take a random word
    :param score: the current score
    :return: The score we finished the game with
    """
    # Get a random word from the words list
    word = hp.get_random_word(words_list)
    guess_letter = []  # The list of the letters' guess
    pattern = "".join([BLANK] * len(word))
    # The updated message that will appear in the display state
    current_message = DISPLAY_MESSAGE
    while score > 0 and BLANK in pattern:
        hp.display_state(pattern, guess_letter, score, current_message)
        user_input = hp.get_input()  # Save the user's input
        # If The input is a letter so do this:
        if user_input[0] == hp.LETTER:
            # Saving the value of the user's input
            letter = user_input[1]
            if not valid_letter(letter) or repeated_letter(letter,
                                                           guess_letter,
                                                           pattern):
                # Update the current message to wrong input
                current_message = WRONG_INPUT
                # Back to the start of the loop so the user can insert valid
                # or un repeated letter
                continue

            score, pattern, current_message \
                = letter_chosen(score, word, letter, pattern, guess_letter)

        # If the user input is to guess a word
        elif user_input[0] == hp.WORD:
            score, current_message = word_chosen(score, user_input[1], word,
                                                 pattern)

        # If the user input is to get a hint
        elif user_input[0] == hp.HINT:
            score -= 1
            # This function shows HINT_LENGTH Hints
            hp.show_suggestions(hint_list(hp.load_words(), pattern,
                                          guess_letter))
    win_or_lose(pattern, guess_letter, score)
    return score


def main():
    """This function runs the games until the player stops"""
    list_of_words = hp.load_words()
    score = run_single_game(list_of_words, hp.POINTS_INITIAL)
    counter = 1  # The number of games were played
    # Ask if you want to play again
    another_game = hp.play_again(TIMES_SCORE_PLAY_AGAIN.format(counter, score))

    # another_game saves a boolean value if the player want to play
    # or not, it will run at least one time first
    while another_game:
        if score > 0:
            score = run_single_game(list_of_words, score)
            another_game = hp.play_again(TIMES_SCORE_PLAY_AGAIN.format(counter,
                                                                       score))
        else:
            counter = 0
            score = hp.POINTS_INITIAL
            another_game = hp.play_again(TIMES_SCORE_PLAY_AGAIN.format(counter,
                                                                       score))


if __name__ == "__main__":
    main()




















