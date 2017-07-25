from tkinter import *
from tkinter import messagebox
import random
import time


class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
        self.name = self.get_name(suit, value)

    def get_name(self, suit, value):
        if 1 < value < 11:
            return str(value) + " of " + suit
        elif value == 11:
            return "Jack" + " of " + suit
        elif value == 12:
            return "Queen" + " of " + suit
        elif value == 13:
            return "King" + " of " + suit
        elif value == 14:
            return "Ace" + " of " + suit


class Player:
    def __init__(self, name):
        self.name = name
        self.deck = []


def setup_deck():
    # Creates and shuffles an array of Card objects to make a complete, shuffled deck.
    setup_deck = []
    suits = ["Spades", "Hearts", "Diamonds", "Clubs"]
    for j in range(0, 4):
        for i in range(2, 15):
            setup_deck.append(Card(suits[j], i))
    random.shuffle(setup_deck)
    return setup_deck


root = Tk()
root.geometry("300x200")

# set up the shuffled deck, and split the array down the middle, giving half to each player
deck = []
deck = setup_deck()
human = Player("human")
compy = Player("compy")
human.deck = deck[:len(deck) // 2]
compy.deck = deck[len(deck) // 2:]


varCard = IntVar()  # varCard is the text of the "pile" button, which gets clicked to generate a slap.
varCard.set(" ")
varTurn = IntVar()  # varTurn keeps track of how many turns there have been
varTurn.set(0)

Button(root, textvariable=varCard, command=lambda: slap(human)).pack()
btn_deal = Button(root, text="deal", command=lambda: deal())
btn_deal.pack()

slapped = False
pile = []


def deal():
    global slapped
    slapped = False  # reset the state of "slapped" every time a new card is drawn.
#    Check for win conditions
    if len(human.deck) == 0 or len(compy.deck) == 0:
        if len(human.deck) == 0:
            winner = "Compy wins!"
        else:
            winner = "You win!"
        messagebox.showinfo("Game Over", winner)
#    Human's turn
    if varTurn.get() % 2 == 0:
        pile.append(human.deck[0])
        human.deck.remove(human.deck[0])
        update_label()  # varTurn is incremented in this method.
        root.update()
        check_for_slap()  # tells the AI to check for a valid slap condition, and will resolve here if necessary
        print("Human: " + str(len(human.deck)))
        deal()  # recursively calls deal() for the AI to take its turn.
    else:
        # AI's turn. This block gets entered on an odd turn number
        timex = time.time()
        global btn_deal
        btn_deal.config(state=DISABLED)  # prevent player from clicking "deal" in the middle of AI's turn
        while time.time() - timex < 2:  # two second delay between player's turn and AI's.
            root.update()
        if not slapped:  # either player may have slapped in the 2 sec. delay. this If statement aborts the turn if that's the case.
            pile.append(compy.deck[0])
            compy.deck.remove(compy.deck[0])
            update_label()
            root.update()
            check_for_slap()
            print("Compy: " + str(len(compy.deck)))
        btn_deal.config(state=NORMAL)
        root.update()


def check_for_slap():
    # AI runs this method after each card is played. Result is a possible slap action.
    make_bad_slap_int = random.randint(1, 50)  # allows the AI to make a "mistake" and make an invalid slap.
    if make_bad_slap_int == 1:
        make_bad_slap = True
    else:
        make_bad_slap = False
    # valid slap conditions are "jack" or "top two match"
    if pile[len(pile) - 1].value == 11 or len(pile) > 1 and (pile[len(pile) - 1].value == pile[len(pile) - 2].value):
        correct_to_slap = True
    else:
        correct_to_slap = False

    if (correct_to_slap and not make_bad_slap) or (not correct_to_slap and make_bad_slap):
        delay = .25 + random.triangular(.1, 1)  # Randomized delay before AI slaps.
        timex = time.time()
        while time.time() - timex < delay:
            root.update()
        slap(compy)


def update_label():
    # updates the label on the "slap pile"
    # increments the turn.
    print("pile: " + str(len(pile)))
    varCard.set(pile[len(pile) - 1].name)
    varTurn.set(varTurn.get() + 1)
    if varTurn.get() % 2 == 0:
        root.configure(background='green')
    else:
        root.configure(background='red')


def slap(player):
    print(player.name + " slapped.")
    global slapped
    if not slapped:  # skips over logic if another slap has already arrived.
        slapped = True
        root.update()
        global pile
        # Check for valid slap conditions.
        if pile[len(pile) - 1].value == 11 or len(pile) > 1 and (pile[len(pile) - 1].value == pile[len(pile) - 2].value):
            if player.name == "human":
                messagebox.showinfo("Slap!", "You WON the slap!")
                print("human takes pile")
                # transfer the cards in pile to the pile of the player
                for card in pile:
                    human.deck.append(card)
                    pile = []
            else:
                messagebox.showinfo("Slap!", "You LOST the slap!")
                print("compy takes pile")
                for card in pile:
                    compy.deck.append(card)
                    pile = []
        else:
            # handles the one card penalty for slapping at the wrong time.
            print("bad slap")
            if player.name == "human":
                messagebox.showinfo("Slap!", "You slapped at the wrong time.")
                pile.append(human.deck[0])
                human.deck.remove(human.deck[0])
                update_label()
                root.update()
            else:
                messagebox.showinfo("Slap!", "Computer slapped at the wrong time.")
                pile.append(compy.deck[0])
                compy.deck.remove(compy.deck[0])
                update_label()
                root.update()


root.mainloop()
