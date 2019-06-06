
import random

    
class Card(object):
    VALUES= [2,3,4,5,6,7,8,9,10,11,12,13,14]
    SUITS = [" clubs", " spades", " hearts", " diamonds"]

    def __init__(self, value, suit):
        self.value= value
        self.suit = suit
        
    def __str__(self):
        if self.value == 14:
            value = 'A'
        elif self.value ==13:
            value = 'K'
        elif self.value ==12:
            value = 'Q'
        elif self.value ==11:
            value = 'J'
        else:
            value = self.value
        return str(value) + self.suit

    def __equal__(self, other):
        return self.value == other.value

    def __lt__(self, other):
        return self.value < other.value

    def __gt__(self, other):
        return self.value > other.value

class Deck(object):
    def __init__(self):
        self.deck = []
        for suit in Card.SUITS:
            for val in Card.VALUES:
                self.deck.append(Card(val, suit))
                
    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        if len(self.deck) == 0:
            return None
        else:
            return self.deck.pop(random.choice(self.deck).value)

class Hand(object):
    def __init__(self, players):
        self.deck = Deck()
        self.deck.shuffle()
        self.players = players
        self.dealt=[ ]
        self.hand_type= ' '
        self.breaker = [ ]

        for i in range(int(self.players)):
            hand=[ ]
            for j in range(5):
                hand.append(self.deck.deal())
            self.dealt.append(hand)

    def sortHand(self):
        for i in range(self.players):
            sort_Hand = sorted(self.dealt[i], reverse = True)
            hand = ''
            count =0
            for card in sort_Hand:
                count += 1
                if count !=5:
                    hand = hand + str(card) + ', '
                else:
                    hand = hand + str(card) + ' '
            print ('Player ' + str(i + 1) + "\'s hand: " + hand)


    def isRoyalFlush(self, hand):
        sort_Hand = sorted(hand, reverse = False)
        flag = True
        current_suit= sort_Hand[0].suit
        current_val= 14
        for card in sort_Hand:
            if card.suit != current_suit or card.value != (current_val):
                flag = False
                break
            else:
                current_val-=1
        if flag:
            self.hand_type="Royal Flush"
            self.breaker = [10, ]
            #how to break to royal flush ties?
        else:
            self.isStraightFlush(sort_Hand)

    def isStraightFlush(self,hand):
        sort_Hand = sorted(hand, reverse = False)
        flag = True
        current_suit= sort_Hand[0].suit
        current_val= sort_Hand[0].value
        for card in sort_Hand:
            if card.suit != current_suit or card.value != (current_val):
                flag = False
                break
            else:
                current_val+=1
        if flag:
            self.hand_type="Straight Flush"
            self.breaker = [9,current_val]
        else:
            self.isFourofaKind(sort_Hand)

    def isFourofaKind(self,hand):
        sort_Hand = sorted(hand, reverse = False)
        current_val= sort_Hand[0].value
        if sort_Hand[0].value == sort_Hand[3].value or sort_Hand[1].value == sort_Hand[4].value:
            self.hand_type="Four of a Kind"
            self.breaker = [8,sort_Hand[3].value]
        else:
            self.isFullHouse(sort_Hand)
            
    def isFullHouse(self,hand):
        sort_Hand = sorted(hand, reverse = False)
        if (sort_Hand[0].value == sort_Hand[1].value and sort_Hand[2].value == sort_Hand[4].value) or (sort_Hand[0].value == sort_Hand[2].value and sort_Hand[3].value == sort_Hand[4].value):
            self.hand_type="Full House"
            #return [7,sort_Hand[3].value], how to find the highest of the 3?
            #self.breaker = 
        else:
            self.isThreeofaKind(sort_Hand)

    def isFlush(self,hand):
        sort_Hand = sorted(hand, reverse = False)
        flag = True
        current_suit= sort_Hand[0].suit
        for card in sort_Hand:
            if card.suit != current_suit:
                flag = False
                break
        if flag:
            self.hand_type="Flush"
            self.breaker = [6,max(sort_Hand)]
        else:
            self.isStraight(sort_Hand)

    def isStraight(self,hand):
        sort_Hand = sorted(hand, reverse = False)
        flag = True
        current_val= sort_Hand[0].value
        for card in sort_Hand:
            if card.value != current_val:
                flag = False
                break
            else:
                current_val+=1
        if flag:
            self.hand_type="Straight"
            self.breaker = [5,max(sort_Hand)]
        else:
            self.isThreeofaKind(sort_Hand)
            
    def isThreeofaKind(self,hand):
        sort_Hand = sorted(hand, reverse = False)
        current_val= sort_Hand[0].value
        if (sort_Hand[2].value == sort_Hand[4].value) or (sort_Hand[0].value == sort_Hand[2].value) or (sort_Hand[1].value == sort_Hand[3].value):
            self.hand_type="Three of a Kind"
            #return [6,max(sort_Hand)], highest trio?
            #self.breaker =
        else:
            self.isTwoPairs(sort_Hand)
            

    def isTwoPairs(self,hand):
        sort_Hand = sorted(hand, reverse = False)
        if (sort_Hand[0].value == sort_Hand[1].value and sort_Hand[2].value == sort_Hand[3].value) or (sort_Hand[1].value == sort_Hand[2].value and sort_Hand[3].value == sort_Hand[4].value) or (sort_Hand[0].value == sort_Hand[1].value and sort_Hand[3].value == sort_Hand[4].value):
            #2-2-1, 1-2-2, 2-1-2
            self.hand_type="Two Pairs"
            #return [6,max(sort_Hand)], highest of the two pairs
            #self.breaker =
        else:
            self.isOnePair(sort_Hand)
    def isOnePair(self,hand):
        sort_Hand = sorted(hand, reverse = False)
        flag = False
        current_val= sort_Hand[0].value
        for card in sort_Hand:
            if card.value == current_val:
                flag = True
                break
            else:
                current_val+=1
        if flag:
            self.hand_type="One Pair"
            self.breaker = [2,current_val]
        else:
            self.isHigh(sort_Hand)
            
    def isHigh(self,hand):
        sort_Hand = sorted(hand, reverse = False)
        self.hand_type="High"
        self.breaker = [1, max(sort_hand)]


    def findWinner(self):
        hand_types = []
        for hand in self.dealt:
            hand_types.append(self.breaker[0])
        count = 0
        cur_max = 0
        winners = [] 
        for rank in hand_types:
            #count += 1
            if rank >= cur_max:
                cur_max= rank
                #winners.append(count)
                #do i need to do this in another loop since if max is cur_max is 3 but theres 2,3,5,4 the 3 would be a winner, and as would the 5
        for rank in hand_types:
            count += 1
            if rank == cur_max:
                winners.append(count)
        if len(winners)==1:
            print("Player " + winners[0] + " wins")
        else:
           break_tie()
           
def break_tie(): #should take in something 
    print("there is a tie")
    count = 0
    for hand in self.dealt():
        cur_max = 0
        winners = []
        if self.breaker[1].__gt__(cur_max):
            cur_max = self.breaker[1]
    winner_hands= []
    for hand in self.dealt():
        new_hand = []
        count +=1
        if self.breaker[1] == cur_max:
            winners.append(count)
            for card in hand:
                new_hand.append(card.value)
        winner_hands.append(new_hand)
    if len(winners)==1:
            print("Player " + winners[0] + " wins")
    else:
        for hand in winner_hands:
            hand.remove(self.breaker[1])
        break_tie(winner_hands)
        
        

def getNumPlayers():
    try:
        players=int(input("Number of players: "))
    except: 
        print("Guess you don't want to play")
        quit()
    while players <=0 or players >10:
        print("invalid number of players")
        players=int(input("Please re-state the number of players: "))
    return players
    


#players=int(input("Number of players: "))
players = getNumPlayers()
print('\n')
game = Hand(players)
game.sortHand()

print('\n')
for i in range(players):
    curHand=game.dealt[i]
    game.isRoyalFlush(curHand)

game.findWinner()
        
    

    
        
