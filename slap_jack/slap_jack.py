from tkinter import *
from tkinter import messagebox
import random
import time


class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    @property
    def name(self):
        if 1 < self.value < 11:
            return str(self.value) + " of " + self.suit
        elif self.value == 11:
            return "Jack" + " of " + self.suit
        elif self.value == 12:
            return "Queen" + " of " + self.suit
        elif self.value == 13:
            return "King" + " of " + self.suit
        elif self.value == 14:
            return "Ace" + " of " + self.suit


class Player:
    def __init__(self, name):
        self.name = name
        self.deck = []


class Game:
    def __init__(self,root):
        self.root = root
        self.human = Player("human")
        self.compy = Player("compy")
        self.deck = self.setup_deck()
        self.human.deck = self.deck[:len(self.deck) // 2]
        self.compy.deck = self.deck[len(self.deck) // 2:]
        self.varCard = IntVar()  # varCard is the text of the "pile" button, which gets clicked to generate a slap.
        self.varCard.set(" ")
        self.varTurn = IntVar()  # varTurn keeps track of how many turns there have been
        self.varTurn.set(0)
        self.slapped = False
        self.pile = []

    def setup_deck(self):
        # Creates and shuffles an array of Card objects to make a complete, shuffled deck.
        setup_deck = []
        suits = ["Spades", "Hearts", "Diamonds", "Clubs"]
        for j in range(0, 4):
            for i in range(2, 15):
                setup_deck.append(Card(suits[j], i))
        random.shuffle(setup_deck)
        return setup_deck

    def deal(self):
        self.slapped = False  # reset the state of "slapped" every time a new card is drawn.
    #    Check for win conditions
        if len(self.human.deck) == 0 or len(self.compy.deck) == 0:
            if len(self.human.deck) == 0:
                winner = "Compy wins!"
            else:
                winner = "You win!"
            self.root.messagebox.showinfo("Game Over", winner)
    #    Human's turn
        if self.varTurn.get() % 2 == 0:
            self.pile.append(self.human.deck[0])
            self.human.deck.remove(self.human.deck[0])
            self.update_label()  # varTurn is incremented in this method.
            self.root.update()
            self.check_for_slap()  # tells the AI to check for valid slap condition, and will resolve here if necessary
            print("Human: " + str(len(self.human.deck)))
            self.deal()  # recursively calls deal() for the AI to take its turn.
        else:
            # AI's turn. This block gets entered on an odd turn number
            timex = time.time()
            global btn_deal
            btn_deal.config(state=DISABLED)  # prevent player from clicking "deal" in the middle of AI's turn
            while time.time() - timex < 2:  # two second delay between player's turn and AI's.
                root.update()
            if not self.slapped:  # either player may have slapped in the 2 sec. delay.
                # this If statement aborts the turn if that's the case.
                self.pile.append(self.compy.deck[0])
                self.compy.deck.remove(self.compy.deck[0])
                self.update_label()
                root.update()
                self.check_for_slap()
                print("Compy: " + str(len(self.compy.deck)))
            btn_deal.config(state=NORMAL)
            root.update()

    def check_for_slap(self):
        # AI runs this method after each card is played. Result is a possible slap action.
        make_bad_slap_int = random.randint(1, 50)  # allows the AI to make a "mistake" and make an invalid slap.
        make_bad_slap = make_bad_slap_int == 1

        # valid slap conditions are "jack" or "top two match"
        correct_to_slap = self.pile[len(self.pile) - 1].value == 11 or len(self.pile) > 1 and (
            self.pile[len(self.pile) - 1].value == self.pile[len(self.pile) - 2].value)

        if (correct_to_slap and not make_bad_slap) or (not correct_to_slap and make_bad_slap):
            delay = .5 + random.triangular(.1, 1)  # Randomized delay before AI slaps.
            timex = time.time()
            while time.time() - timex < delay:
                root.update()
            self.slap(self.compy)

    def slap(self, player):
        print(player.name + " slapped.")
        if not self.slapped:  # skips over logic if another slap has already arrived.
            self.slapped = True
            root.update()
            # Check for valid slap conditions.
            if self.pile[len(self.pile) - 1].value == 11 or len(self.pile) > 1 and (
                    self.pile[len(self.pile) - 1].value == self.pile[len(self.pile) - 2].value):
                if player.name == "human":
                    self.root.messagebox.showinfo("Slap!", "You WON the slap!")
                    print("human takes pile")
                    # transfer the cards in pile to the pile of the player
                    for card in self.pile:
                        self.human.deck.append(card)
                        self.pile = []
                else:
                    self.root.messagebox.showinfo("Slap!", "You LOST the slap!")
                    print("compy takes pile")
                    for card in self.pile:
                        self.compy.deck.append(card)
                        self.pile = []
            else:
                # handles the one card penalty for slapping at the wrong time.
                print("bad slap")
                if player.name == "human":
                    self.root.messagebox.showinfo("Slap!", "You slapped at the wrong time.")
                    self.pile.append(self.human.deck[0])
                    self.human.deck.remove(self.human.deck[0])
                    self.update_label()
                    root.update()
                else:
                    self.root.messagebox.showinfo("Slap!", "Computer slapped at the wrong time.")
                    self.pile.append(self.compy.deck[0])
                    self.compy.deck.remove(self.compy.deck[0])
                    self.update_label()
                    root.update()

    def update_label(self):
        # updates the label on the "slap pile"
        # increments the turn.
        print("pile: " + str(len(self.pile)))
        self.varCard.set(self.pile[len(self.pile) - 1].name)
        self.varTurn.set(self.varTurn.get() + 1)
        if self.varTurn.get() % 2 == 0:
            root.configure(background='green')
        else:
            root.configure(background='red')

root = Tk()
root.geometry("300x200")
messagebox.showinfo("Test", "It worked")
game = Game(root)

Button(root, textvariable=game.varCard, command=lambda: game.slap(game.human)).pack()
btn_deal = Button(root, text="deal", command=lambda: game.deal())
btn_deal.pack()

root.mainloop()
