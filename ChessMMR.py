#!/usr/bin/env python
"""
Allows admin to rank and rate player for zero-sum games using the Elo Rating System.
    - admin can login with password or set new password
    - register new player
    - add results of new match
    - request elo ratings or rankings report (for everyone)
    - see manual instructions (for chess)
    - quit program

P.S. All data is stored in the ChessMMR_DataFile.txt file

Resources used:
    - "Chess Ratings - How They Work" by Erik from chess.com
        <https://www.chess.com/article/view/chess-ratings---how-they-work>
    - "Elo rating system" from Wikipedia
        <https://en.wikipedia.org/wiki/Elo_rating_system>
    - "How Elo Ratings Are Calculated" from Spirit Of The Law
        <https://www.youtube.com/watch?v=GTaAWtuLHuo>
    - "The Elo Rating System for Chess and Beyond" by singingbanana
        <https://www.youtube.com/watch?v=AsYfbmp0To0>
"""

__author__ = "Dhruba Jyoti Paul"
__version__ = "0.0.1"
__date__ = "2021/09/27"

__copyright__ = "Copyright 2021, The Lazy Company"
__email__ = "dhrubajyotipaul3@gmail.com"
__maintainer__ = "Dhruba Jyoti Paul"
__status__ = "Production"

import os

# Constants
FILE_NAME = "ChessMMR_DataFile.txt"
PASSWORD_INDEX = 0
PLAYER_INDEX = 0
TOTAL_GAMES_INDEX = 1
WINS_INDEX = 2
LOSSES_INDEX = 3
DRAWS_INDEX = 4
RATING_INDEX = 5

# Dynamic global Var for Convenience (needs to be updated before use)
FILE_CONTENT = []


def read_file():
    """
    read and updated FILE_CONTENT global variable with data file content

    :return: file content
    """
    f = open(FILE_NAME, 'r')
    file_content = f.readlines()
    f.close()
    global FILE_CONTENT
    FILE_CONTENT = file_content
    return file_content


def write_file(file_content="", mode='w'):
    """
    Write content to data file.

    :param file_content: string to write on file
    :param mode: edit mode ('a' - append, or 'w' - overwrite everything with new file content)
    :return: None
    """
    f = open(FILE_NAME, mode)
    f.write(file_content)
    f.close()


def write_file_array(array):
    """
    Write content to data file

    :param array: array of strings
    :return: None
    """
    f = open(FILE_NAME, 'w')
    f.writelines(array)
    f.close()


def set_new_password():
    """
    Allows user to set new password

    :return: None
    """
    read_file()

    # If requesting password to update password
    if request_password(True):
        new_password = input("Enter new password: ")

        # Saving to Password
        FILE_CONTENT[0] = "Password: " + new_password + "\n"
        write_file_array(FILE_CONTENT)
        print("New Password Saved")


def request_password(update_password=False):
    """
    Requests password from the user

    :param update_password: True if password is requested to set new password
    :return: True if user input correct password, False otherwise
    """
    read_file()

    # Prompting user different if password is being updated
    if update_password:
        user_input = input("Provide old Password: ")
    else:
        user_input = input("Provide Password: ")

    # Comparing user input to password in database
    if user_input == FILE_CONTENT[0].replace("Password: ", "").strip():
        print("Password Correct")
        return True
    else:
        print("Wrong Password!")
        return False


def login():
    """
    Provides actions for user who is not logged in

    :return: None
    """
    # is data file doesn't exist
    if not os.path.isfile(FILE_NAME):
        print("You have no data file. Creating data file...\nPlease set a password\n")
        new_password = input("Enter new password: ")

        # Saving to Password
        write_file("Password: " + new_password + "\n")
        print("New Password Saved\n")

    # login actions' loop
    while True:
        user_input = input("Choose an action:\n\t[l] - login with password\n\t[s] - set new password\n").lower()
        if user_input == "l":
            # Ask for password to login
            if request_password():
                print("You've been logged in\n")
                return
        elif user_input == "s":
            # update password
            if set_new_password():
                return
        else:
            print("invalid action. Try again\n")
            continue


def register_new_player():
    """
    Registers new user and saves name in data file

    :return: None
    """
    user_input = input("Enter player name: ").title()
    write_file(user_input + ", total games: 0, wins: 0, losses: 0, draws: 0, rating: 100\n", 'a')
    print("New player registered\n")


def get_player_name(player_list, player_number):
    """
    Request user to provide user name that already exists in the player list (data file)

    :param player_list: list of player names
    :param player_number: Player 1 or Player 2
    :return: a player name the user provides from the player list
    """
    player_number = str(player_number)
    while True:
        player = input("Provide player" + player_number + " name: ").lower()
        if player in player_list:
            return player
        else:
            print("Player" + player_number + " not in player list... Try again")


def add_new_match_results():
    """
    Allows user to add results of a new match to update player rank and ratings

    :return: None
    """
    read_file()
    player_list = []
    for i in range(1, len(FILE_CONTENT)):
        player_list.append(FILE_CONTENT[i].split(", ")[PLAYER_INDEX].lower())

    # Getting the names of player 1 and 2
    print("Select a player from the player list: ", player_list)
    player1 = get_player_name(player_list, 1)
    player2 = get_player_name(player_list, 2)

    player_info = file_content_to_player_info()

    while True:
        player1_result = input("What was the result for player1? "
                               + "Did player1:\n\t[w] - win?\n\t[l] - lose?\n\t[d] - draw?\n").lower()
        if player1_result == 'w' or player1_result == 'l' or player1_result == 'd':
            update_player_data(player_info, player_list.index(player1), player_list.index(player2), player1_result)
            break
        else:
            print("Invalid command... Try again\n")


def file_content_to_player_info():
    """
    Extracts information of all players and stores it in a list

    :return: return the list with the data of all players
    """
    read_file()
    player_info = []
    for i in range(1, len(FILE_CONTENT)):
        player_info.append(FILE_CONTENT[i].split(", "))
        player_info[i - 1][TOTAL_GAMES_INDEX] = int(player_info[i - 1][TOTAL_GAMES_INDEX].replace("total games: ", ""))
        player_info[i - 1][WINS_INDEX] = int(player_info[i - 1][WINS_INDEX].replace("wins: ", ""))
        player_info[i - 1][LOSSES_INDEX] = int(player_info[i - 1][LOSSES_INDEX].replace("losses: ", ""))
        player_info[i - 1][DRAWS_INDEX] = int(player_info[i - 1][DRAWS_INDEX].replace("draws: ", ""))
        player_info[i - 1][RATING_INDEX] = int(player_info[i - 1][RATING_INDEX].replace("rating: ", "").strip())

    return player_info


def player_info_to_file_content(player_info):
    """
    converts list with all player data to content to write back into data file

    :param player_info: list with data of all players
    :return: updated file content
    """
    read_file()

    # Converting every element's type to string to write on file
    for i in range(len(player_info)):
        for j in range(len(player_info[i])):
            player_info[i][j] = str(player_info[i][j])

    # Editing file content (updating)
    for i in range(len(player_info)):
        FILE_CONTENT[i + 1] = player_info[i][PLAYER_INDEX].title() \
                              + ", total games: " + player_info[i][TOTAL_GAMES_INDEX] \
                              + ", wins: " + player_info[i][WINS_INDEX] \
                              + ", losses: " + player_info[i][LOSSES_INDEX] \
                              + ", draws: " + player_info[i][DRAWS_INDEX] \
                              + ", rating: " + player_info[i][RATING_INDEX] \
                              + "\n"
    return FILE_CONTENT


def update_player_data(player_info, player1_index, player2_index, player1_result):
    """
    Updates player data after user adds match results
    Writes updated data to file

    :param player_info: list will data of all players
    :param player1_index: index of player 1
    :param player2_index: index of player 2
    :param player1_result: match result for player1 ('w' - win, 'l' - loss, 'd' - draw)
    :return: None
    """
    # GET old ratings for the players
    # To calculate new ratings!
    player1_rating = player_info[player1_index][RATING_INDEX]
    player2_rating = player_info[player2_index][RATING_INDEX]

    # expected scores for the players
    # To calculate new ratings!
    player1_expected_score = expected_score(player1_rating, player2_rating)
    player2_expected_score = expected_score(player2_rating, player1_rating)

    # actual scores for the players
    # To calculate new ratings!
    player1_score = None
    player2_score = None
    if player1_result == 'w':
        player1_score = 1
        player2_score = 0
    elif player1_result == 'l':
        player2_score = 1
        player1_score = 0
    elif player1_result == 'd':
        player1_score = 0.5
        player2_score = 0.5

    # calculating new ratings for the players
    player1_new_rating = new_rating(player1_rating, player1_score, player1_expected_score)
    player2_new_rating = new_rating(player2_rating, player2_score, player2_expected_score)

    # UPDATING! ################################################################
    # Update total games for players
    player_info[player1_index][TOTAL_GAMES_INDEX] += 1
    player_info[player2_index][TOTAL_GAMES_INDEX] += 1

    # Update total wins, loses, and draws for the players
    if player1_result == 'w':
        player_info[player1_index][WINS_INDEX] += 1
        player_info[player2_index][LOSSES_INDEX] += 1
    elif player1_result == 'l':
        player_info[player1_index][LOSSES_INDEX] += 1
        player_info[player2_index][WINS_INDEX] += 1
    elif player1_result == 'd':
        player_info[player1_index][DRAWS_INDEX] += 1
        player_info[player2_index][DRAWS_INDEX] += 1

    # Update ratings for the players
    player_info[player1_index][RATING_INDEX] = player1_new_rating
    player_info[player2_index][RATING_INDEX] = player2_new_rating

    # Writing to file ##########################################################
    # Converting every element's type to string to write on file
    for i in range(len(player_info)):
        for j in range(len(player_info[i])):
            player_info[i][j] = str(player_info[i][j])

    # Editing file content (updating)
    player_info_to_file_content(player_info)
    # writing the updated content to file
    write_file_array(FILE_CONTENT)
    print("Data has been updated\n")


def new_rating(player_rating, player_score, player_expected_score):
    """
    Returns the new rating by using the three main ranges of k-factor formerly used by the US Chess Federation:
        - Players below 2100: K-factor of 32 used
        - Players between 2100 and 2400: K-factor of 24 used
        - Players above 2400: K-factor of 16 used.

    Formula from Wikipedia <https://en.wikipedia.org/wiki/Elo_rating_system#Mathematical_details>

    :param player_rating: player's old rating (before a match)
    :param player_score: player's win_rate without past games
    :param player_expected_score: player win_rate
    :return: new rating for player
    """
    k_factor = 0
    if k_factor < 2100:
        k_factor = 32
    elif 2100 <= player_rating <= 2400:
        k_factor = 24
    elif player_rating > 2400:
        k_factor = 16

    player_new_rating = player_rating + k_factor * (player_score - player_expected_score)

    # TODO: Ask user if a rating_floor is desired
    if player_new_rating < 100:
        player_new_rating = 100

    # rounding new rating from float to the nearest int
    player_new_rating = round(player_new_rating)

    return player_new_rating


def expected_score(player1_rating, player2_rating):
    """
    Returns the expected score for the player whose rating is the first argument

    Formula from Wikipedia <https://en.wikipedia.org/wiki/Elo_rating_system#Mathematical_details>

    :param player1_rating: Rating of player 1
    :param player2_rating: Rating of player 2
    :return: the expected score for player 1
    """
    return 1 / (1 + 10 ** ((player2_rating - player1_rating) / 400))


def print_rankings():
    """
    Formats the data from the data file, order the players in descending order according to their ratings, and prints
    the formatted data from the data file.

    :return: the formatted data from the data file
    """
    player_info = file_content_to_player_info()

    player_info.sort(key=lambda x: x[RATING_INDEX], reverse=True)

    txt_template = '{:<20}' * 8 + "\n"
    txt = ""
    # txt += txt_template.format("", "PLayer", "Total", "Total", "Total", "Total", "", "")
    txt += txt_template.format("Rank", "Name", "Wins", "Losses", "Draws", "Games", "Rating", "Class")
    txt += txt_template.format(".......", ".......", ".......", ".......", ".......", ".......", ".......", ".......")

    for i in range(len(player_info)):
        txt += txt_template.format(i + 1, player_info[i][PLAYER_INDEX], player_info[i][WINS_INDEX],
                                   player_info[i][LOSSES_INDEX], player_info[i][DRAWS_INDEX],
                                   player_info[i][TOTAL_GAMES_INDEX], player_info[i][RATING_INDEX],
                                   get_player_class(player_info[i][RATING_INDEX]))

    print(txt)
    return txt


def get_player_class(player_rating):
    """
    United States Chess Federation ratings classification for players:

    2400 and above: Senior Master
    2200–2399: National Master
    2000–2199: Expert or Candidate Master
    1800–1999: Class A
    1600–1799: Class B
    1400–1599: Class C
    1200–1399: Class D
    1000–1199: Class E
    800–999: Class F
    600–799: Class G
    400–599: Class H
    200–399: Class I
    100–199: Class J

    :returns: the Classification of the player based on the player's rating
    """
    if 100 <= player_rating <= 199:
        return "Class J"
    elif 200 <= player_rating <= 399:
        return "Class I"
    elif 400 <= player_rating <= 599:
        return "Class H"
    elif 600 <= player_rating <= 799:
        return "Class G"
    elif 800 <= player_rating <= 999:
        return "Class F"
    elif 1000 <= player_rating <= 1199:
        return "Class E"
    elif 1200 <= player_rating <= 1399:
        return "Class D"
    elif 1400 <= player_rating <= 1599:
        return "Class C"
    elif 1600 <= player_rating <= 1799:
        return "Class B"
    elif 1800 <= player_rating <= 1999:
        return "Class A"
    elif 2000 <= player_rating <= 2199:
        return "Expert"
    elif 2200 <= player_rating <= 2399:
        return "National Master"
    elif 2400 <= player_rating:
        return "Senior Master"
    else:
        return "N/A"


def manual_instructions():
    """
    Provides the user basic knowledge about how the Elo System Works. Prints the message to terminal

    :returns: None
    """
    print()
    print()
    print("The Class System is based on the United States Chess Federation ratings Classifications: "
          "\n<https://en.wikipedia.org/wiki/Elo_rating_system#United_States_Chess_Federation_ratings>"
          "\n\t2400 and above: Senior Master"
          "\n\t2200–2399: National Master"
          "\n\t2000–2199: Expert or Candidate Master"
          "\n\t1800–1999: Class A"
          "\n\t1600–1799: Class B"
          "\n\t1400–1599: Class C"
          "\n\t1200–1399: Class D"
          "\n\t1000–1199: Class E"
          "\n\t800–999: Class F"
          "\n\t600–799: Class G"
          "\n\t400–599: Class H"
          "\n\t200–399: Class I"
          "\n\t100–199: Class J\n")
    print("Player Rating Floor is set to 100")
    print("Player Rating is calculated with the following formulas:"
          "\n\t- expected score = 1 / (1 + 10 ^ ((player2_rating - player1_rating) / 400))"
          "\n\t- new_player_rating = old_player_rating + k_factor * (player_score - player_expected_score)\n")
    print("The k-factor determines how drastically a player's rating changes.\n"
          "This app is using the three main ranges of k-factor formerly used by the US Chess Federation:"
          "\n\t- Players below 2100: K-factor of 32 used"
          "\n\t- Players between 2100 and 2400: K-factor of 24 used"
          "\n\t- Players above 2400: K-factor of 16 used.\n")
    print()


def admin_actions():
    """
    Allows user, after user logs in, to rank and rate player for zero-sun games using the Elo Rating System.
    - register new player
    - add results of new match
    - request elo ratings or rankings report (for everyone)
    - see manual instructions (for chess)
    - quit program

    :return: None
    """
    # admin actions' loop
    while True:
        user_input = input("Choose an action:\n\t[r] - register new player\n\t[a] - add new match results"
                           + "\n\t[s] - show player rankings\n\t[m] - manual instructions (for chess)"
                           + "\n\t[q] - quit program\n").lower()
        if user_input == "r":
            # register new player
            register_new_player()
        elif user_input == "a":
            # add new match results
            add_new_match_results()
        elif user_input == "s":
            # show player rankings
            print_rankings()
        elif user_input == "m":
            # show manual instructions
            manual_instructions()
        elif user_input == "q":
            print("Goodbye!")
            return
        else:
            print("invalid action. Try again\n")
            continue


if __name__ == '__main__':
    # Login
    login()

    # Admin Actions
    admin_actions()