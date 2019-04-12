import random

class Player: 
    
    def __init__(self, role, wallet):
        self.cards = []
        self.score = 0
        self.stand = False
        self.role = role
        self.wallet = wallet
    
    def deal(self):
        self.cards.append(get_card())
        self.cards.append(get_card())
        if self.role == "dealer":
            print(f"Dealer has a {self.cards[1]}")
    
    def hit(self):
        self.cards.append(get_card())
    
    def calc_score(self):    
        s = 0
        for c in self.cards:
            if c[0] in ["1","J","Q","K"]:
                s += 10
            elif c[0] == "A":
                s += 11
            elif int(c[0]) in [2,3,4,5,6,7,8,9]:
                s += int(c[0])
        if s > 21:
            s = 0
            for c in self.cards:
                if c[0] in ["1","J","Q","K"]:
                    s += 10
                elif c[0] == "A":
                    s += 1
                elif int(c[0]) in [2,3,4,5,6,7,8,9]:
                    s += int(c[0])
        if s > 21:
            self.score = "BUST"
            return (self.cards, self.score)
        else:
            self.score = s
            return (self.cards, self.score)

    def hit_prompt(self):
        while True:
            r = input("Hit? y/n ")
            if r in ["Y", "y"]:
                self.stand = False
                return True
            elif r in ["N", "n"]:
                self.stand = True
                return False
    
       
def get_card():
    c = random.choice(deck)
    deck.remove(c)
    return c    
        
deck = ["2C","3C","4C","5C","6C","7C","8C","9C","10C","JC","QC","KC","AC","2S","3S","4S","5S","6S","7S","8S","9S","10S","JS","QS","KS","AS","2D","3D","4D","5D","6D","7D","8D","9D","10D","JD","QD","KD","AD","2H","3H","4H","5H","6H","7H","8H","9H","10H","JH","QH","KH","AH"]

You = Player("player", 1000)
Dealer = Player("dealer", 1000000)

while You.wallet > 0 and Dealer.wallet > 0:
    You.cards = []
    You.stand = False
    Dealer.cards = []

    You.deal()
    Dealer.deal()

    bet = 0

    while bet <= 0 or bet > You.wallet:
        bet = int(input(f"Current funds: ${You.wallet}\nHow much would you like to bet? $"))
        if bet <= 0 or bet > You.wallet:
            print("Let's try that again")

    You.wallet = You.wallet - bet

    You.calc_score()
    Dealer.calc_score()

    if You.score == 21:
        print("Blackjack!")

    while You.stand == False:
        print(f"Cards: {You.cards} - {You.score}")
        if You.score in [21, "BUST"]:
            break
        elif You.hit_prompt() == True:
            You.hit()
            You.calc_score()
        else:
            You.calc_score()

    if You.score == "BUST":
        print("You busted")         

    print(f"Dealer's cards: {Dealer.cards}")

    if Dealer.score == 21:
        print("Blackjack!")

    while Dealer.score != "BUST":
        if Dealer.score <= 16:
            Dealer.hit()
            Dealer.calc_score()
            print(f"Dealer's cards: {Dealer.cards}")
        else:
            break
        
    if Dealer.score == "BUST":
        print("Dealer busted")

    print(f"You:    {You.cards} - {You.score}\nDealer: {Dealer.cards} - {Dealer.score}")

    if You.score != "BUST" and (Dealer.score == "BUST" or Dealer.score < You.score):
        if You.score == 21:
            print(f"You win ${round(1.5*bet)}")
            You.wallet = You.wallet + round(2.5*bet)
            Dealer.wallet = Dealer.wallet - round(1.5*bet)
        else:
            print(f"You win ${bet}")
            You.wallet = You.wallet + 2*bet
            Dealer.wallet = Dealer.wallet - bet
    elif You.score != "BUST" and (Dealer.score == You.score):
        print(f"You get your ${bet} back")
        You.wallet = You.wallet + bet
    else:
        print(f"You lost your ${bet}")

