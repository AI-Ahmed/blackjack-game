__author__ = "{D/R}"

import random
try:
    import tkinter
except ImportError:  # Python 2.0
    import Tkinter as tkinter


def load_images(card_images):
    suits = ['heart', 'club', 'diamond', 'spade']
    face_cards = ['jack', 'queen', 'king']

    if tkinter.TkVersion >= 8.6:
        extension = 'png'
    else:
        extension = 'ppm'

    # for each suit, retrieve the images for the cards
    for suit in suits:
        # for the number 1 to 10
        for card in range(1, 11):
            name = 'Blackjack/{}_{}.{}'.format(str(card), suit, extension)
            image = tkinter.PhotoImage(file=name).subsample(2, 2)
            card_images.append((card, image,))

        # next the face cards
        for card in face_cards:
            name = 'Blackjack/{}_{}.{}'.format(str(card), suit, extension)
            image = tkinter.PhotoImage(file=name).subsample(2, 2)
            card_images.append((10, image,))


def deal_card(frame):
    # pop the first cards
    next_card = deck.pop(0)
    # add the image to the label
    tkinter.Label(frame, image=next_card[1], relief="raised").pack(side='left')
    return next_card


def ace_holding(hand_list):
    """
       Calculate the total score of all the cards in the list.
       Only one ace can have the value 11, and this will be reduce to 1 if the hand would bust.
    """
    score = 0
    ace = False

    for next_card in hand_list:
        card_value = next_card[0]
        if card_value == 1 and not ace:
            ace = True
            card_value = 11

        score += card_value
        # if we would bust, check if there's an ace and subtract 10
        if score > 21 and ace:
            score -= 10
            ace = False

    return score


def rules(dscore, pscore):
    if pscore == 21 and dscore == 21:
        result_text.set("Draw!")

    elif dscore > 21 or pscore == 21:
        result_text.set("Player Wins")
    elif pscore > 21 or dscore == 21:
        result_text.set("Dealer Wins")

    elif (15 <= pscore <= 21) and dealer_score > 21:
        result_text.set("Player Wins")
    elif (15 <= dscore <= 21) and player_score > 21:
        result_text.set("Dealer Wins")

    else:
        result_text.set("")


def deal_dealer():
    dealer_score = ace_holding(dealer_hand)  # use the list to caculate the dealer score
    # This[loop] will give the dealer the chance to select the # No.Of.Cards that will help him to reach the range 17-21 may or may not lose depend on the random cards he choose
    while 0 < dealer_score < 17:
        dealer_hand.append(deal_card(dealer_card_canvas))   # append the images into the list
        dealer_score = ace_holding(dealer_hand)
        dealer_score_label.set(dealer_score)

    rules(dealer_score, player_score)


def deal_player():
    player_hand.append(deal_card(player_card_canvas))
    player_score = ace_holding(player_hand)

    player_score_label.set(player_score)
    rules(dealer_score, player_score)


def new_game():
    # we've to make both canavas global varaible and lists, so we can destroy them and recreate them normally for new Game
    global dealer_card_canvas
    global player_card_canvas
    global dealer_hand
    global player_hand
    # reset the lists
    dealer_hand.clear()
    player_hand.clear()

    # clear scores
    result_text.set("")
    dealer_score_label.set(0)
    player_score_label.set(0)

    # clear the canavas
    dealer_card_canvas.grid_remove()
    player_card_canvas.grid_remove()

    dealer_card_canvas = tkinter.Canvas(card_frame, borderwidth=2, relief="sunken", background="green")
    dealer_card_canvas.grid(row=0, column=1, sticky='ew', rowspan=2)

    player_card_canvas = tkinter.Canvas(card_frame, borderwidth=2, relief="sunken", background="green")
    player_card_canvas.grid(row=2, column=1, sticky='ew', rowspan=2)


def _initialize__():    # Protected function
    """Automated randow check in table for two cards. 1 for player and other card for the dealer"""
    deal_player()
    dealer_hand.append(deal_card(dealer_card_canvas))
    dealer_score_label.set(ace_holding(dealer_hand))     # this will help to saw the dealer number at the beginning
    deal_player()


def content_reset():
    global deck
    new_game()
    random.shuffle(deck)

    dealer_score_label.set(dealer_hand)
    player_score_label.set(player_hand)

    _initialize__()


def play():
    _initialize__()
    mainWindows.mainloop()


mainWindows = tkinter.Tk()
mainWindows.geometry("800x630")
mainWindows.title("BlackJack")
mainWindows.configure(background="green")

result_text = tkinter.StringVar()
result = tkinter.Label(mainWindows, textvariable=result_text)
result.grid(row=0, column=0, columnspan=3, sticky='n')

card_frame = tkinter.Frame(mainWindows, relief="sunken", borderwidth=1, background="green")
card_frame.grid(row=1, column=0, sticky='ew', rowspan=2, columnspan=3)

# Dealer Index variable result
dealer_score_label = tkinter.IntVar()
dealer_score = 0
tkinter.Label(card_frame, text="Dealer", background="green", fg="white").grid(row=0, column=0)
tkinter.Label(card_frame, textvariable=dealer_score_label, background="green", fg="white").grid(row=1, column=0)

# Embedded Dealer Canvas
dealer_card_canvas = tkinter.Canvas(card_frame, borderwidth=2, relief="sunken", background="green")
dealer_card_canvas.grid(row=0, column=1, sticky='ew', rowspan=2)

# Player Index variable result
player_score_label = tkinter.IntVar()
player_score = 0
tkinter.Label(card_frame, text="Player", background="green", fg="white").grid(row=2, column=0)
tkinter.Label(card_frame, textvariable=player_score_label, background="green", fg="white").grid(row=3, column=0)

# Embedded Player Canvas
player_card_canvas = tkinter.Canvas(card_frame, borderwidth=2, relief="sunken", background="green")
player_card_canvas.grid(row=2, column=1, sticky='ew', rowspan=2)

# Dealer and Player Buttons
button_frame = tkinter.Frame(mainWindows, relief="sunken", borderwidth=1, background="grey")
button_frame.grid(row=3, column=0, sticky='w', rowspan=2)

# Dealer Button
dealer_button = tkinter.Button(button_frame, text="Dealer", command=deal_dealer)
dealer_button.grid(row=0, column=0)

# Player Button
Player_button = tkinter.Button(button_frame, text="Player", command=deal_player)
Player_button.grid(row=0, column=1, columnspan=1)

# New Game Button
new_button = tkinter.Button(button_frame, text="New Game", command=content_reset)
new_button.grid(row=0, column=2, columnspan=1)

# Exit Button
exit_button = tkinter.Button(button_frame, text="Exit", command=exit)
exit_button.grid(row=0, column=3, columnspan=1)

# load cards
cards = []
load_images(cards)
print(cards)
# create new deck of cards
deck = list(cards)

random.shuffle(deck)
# create a handler for each user (Player and dealer)
dealer_hand = []
player_hand = []

if __name__ == '__main__':  # We're using __main__ for keeping the program run into one file instead of being imported and hacked by another files
    play()
