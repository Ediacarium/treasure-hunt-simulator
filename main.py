from enum import Enum, auto
import random
import csv
from tqdm import tqdm
import matplotlib.pyplot as plot

TREASURE_HUNT_AMOUNT = 4
LIGHTNING_STORM_AMOUNT = 2
csv_file = "./results.csv"
gnuplotfile = "./results.dat"


class Mana(Enum):
    COLORLESS = auto()
    RED = auto()
    BLUE = auto()

class CardType(Enum):
    LAND = auto()
    SPELL = auto()

class LandState():
    
    def new_pair(card, lands = []):
        ls = LandState(card)
        return (card, ls)
        
    
    def __init__(self, card, lands = []):
        
        self.tapped = False
        if card == Card.TOLARIA_WEST:
            self.tapped = True
        elif card == Card.SPIREBLUFF_CANAL and len(lands) > 2:
            self.tapped = True    
                
        self.counter = 0
        if card == Card.GEMSTONE_CAVERNS_LUCKY:
            self.counter = 1
        elif card == Card.GEMSTONE_MINE:
            self.counter = 3
        
    def __repr__(self):
        return ("tapped" if self.tapped else "untapped") \
            + " with " + str(self.counter) + " counters"

class Card(Enum):
    BOSEIJU = (CardType.LAND, auto())
    CASCADE_BLUFFS = (CardType.LAND, auto())
    DESOLATE_LIGHTHOUSE = (CardType.LAND, auto())
    GEMSTONE_CAVERNS = (CardType.LAND, auto())
    GEMSTONE_CAVERNS_LUCKY = (CardType.LAND, auto())
    GEMSTONE_MINE = (CardType.LAND, auto())
    ISLAND = (CardType.LAND, auto())
    MOUNTAIN = (CardType.LAND, auto())
    NEPHALIA_ACADEMY = (CardType.LAND, auto())
    OBORO = (CardType.LAND, auto())
    RELIQUARY_TOWER = (CardType.LAND, auto())
    SPIREBLUFF_CANAL = (CardType.LAND, auto())
    TOLARIA_WEST = (CardType.LAND, auto())
    LIGHTNING_STORM = (CardType.SPELL,auto()) 
    TREASURE_HUNT = (CardType.SPELL, auto())
    
    def __str__(self):
        if self == Card.BOSEIJU:
            return "Boseiju"
        elif self == Card.CASCADE_BLUFFS:
            return "Cascade Bluffs"
        elif self == Card.DESOLATE_LIGHTHOUSE:
            return "Desolate Lighthouse"
        elif self == Card.GEMSTONE_CAVERNS:
            return "Gemstone Caverns"
        elif self == Card.GEMSTONE_CAVERNS_LUCKY:
            return "Gemstone Caverns"
        elif self == Card.GEMSTONE_MINE:
            return "Gemstone Mine"
        elif self == Card.ISLAND:
            return "Island"
        elif self == Card.MOUNTAIN:
            return "Mountain"
        elif self == Card.NEPHALIA_ACADEMY:
            return "Nephalia Academy"
        elif self == Card.OBORO:
            return "Oboro"
        elif self == Card.RELIQUARY_TOWER:
            return "Reliquary Tower"
        elif self == Card.SPIREBLUFF_CANAL:
            return "Spirebluff Canal"
        elif self == Card.TOLARIA_WEST:
            return "Tolaria West"
        elif self == Card.LIGHTNING_STORM:
            return "Lightning Storm"
        elif self == Card.TREASURE_HUNT:
            return "Treasure Hunt"
    
    def __repr__(self):
        return self.__str__()


class Battlefield:
    def __init__(self):
        self.lands = []

def contains_lands(cards):
    for card in cards:
        if card.value[0] == CardType.LAND:
            return True
    return False
            
red_sources = [Card.MOUNTAIN,
               Card.GEMSTONE_MINE,
               Card.GEMSTONE_CAVERNS_LUCKY,
               Card.SPIREBLUFF_CANAL]
            
def can_produce_red(cards):
    for source in red_sources:
        if source in cards:
            return True
            
    return Card.CASCADE_BLUFFS in cards and \
            Card.ISLAND in cards or \
            Card.TOLARIA_WEST in cards or \
            Card.OBORO in cards           
            
blue_sources = [Card.ISLAND,
                Card.TOLARIA_WEST,
                Card.GEMSTONE_MINE,
                Card.GEMSTONE_CAVERNS_LUCKY,
                Card.SPIREBLUFF_CANAL]
            
def can_produce_blue(cards):
    for source in blue_sources:
        if source in cards:
            return True
            
    return Card.CASCADE_BLUFFS in cards and Card.MOUNTAIN in cards

def shuffled_deck():
    deck = []

    for _ in range(4):
        deck.append(Card.BOSEIJU)
        
    for _ in range(4):
        deck.append(Card.CASCADE_BLUFFS)
        
    for _ in range(1):
        deck.append(Card.DESOLATE_LIGHTHOUSE)
        
    for _ in range(4):
        deck.append(Card.GEMSTONE_CAVERNS)
        
    for _ in range(4):
        deck.append(Card.GEMSTONE_MINE)
        
    for _ in range(10):
        deck.append(Card.ISLAND)
        
    for _ in range(10):
        deck.append(Card.MOUNTAIN)
        
    for _ in range(4):
        deck.append(Card.NEPHALIA_ACADEMY)
        
    for _ in range(1):
        deck.append(Card.OBORO)
        
    for _ in range(4):
        deck.append(Card.RELIQUARY_TOWER)
        
    for _ in range(4):
        deck.append(Card.SPIREBLUFF_CANAL)

    for _ in range(4):
        deck.append(Card.TOLARIA_WEST)
        
    for _ in range(LIGHTNING_STORM_AMOUNT):
        deck.append(Card.LIGHTNING_STORM)
        
    for _ in range(TREASURE_HUNT_AMOUNT):
        deck.append(Card.TREASURE_HUNT)
        

    random.shuffle(deck)
    return deck

def first_hand():
    for i in range(7,0,-1):
        deck = shuffled_deck()
        hand = deck[:i]
        deck = deck[i:]
        if Card.TREASURE_HUNT in hand:
            return hand, deck
    deck = shuffled_deck()
    return [deck[0]], deck[1:]
        
exile_order = [ Card.TOLARIA_WEST, 
                Card.NEPHALIA_ACADEMY, 
                Card.BOSEIJU, 
                Card.DESOLATE_LIGHTHOUSE, 
                Card.CASCADE_BLUFFS, 
                Card.MOUNTAIN, 
                Card.OBORO, 
                Card.ISLAND, 
                Card.GEMSTONE_MINE, 
                Card.SPIREBLUFF_CANAL, 
                Card.LIGHTNING_STORM, 
                Card.GEMSTONE_CAVERNS, 
                Card.TREASURE_HUNT]
def pregame_actions(hand, deck):
    battlefield = Battlefield()
    
    if len(hand) < 7:
        if deck[0] == Card.TREASURE_HUNT:
            if not contains_lands(hand):
                deck.append(deck.pop(0))
    
        elif deck[0] == Card.LIGHTNING_STORM:
            if not contains_lands(hand):
                deck.append(deck.pop(0))
        elif deck[0].value == CardType.LAND:
            if len(hand) == 1:
                deck.append(deck.pop(0))
        
    caverns = list(filter(lambda c: c == Card.GEMSTONE_CAVERNS, hand))
    for cavern in range(len(caverns)):
        if Card.GEMSTONE_CAVERNS in hand and len(hand) > 2:
            exiled = False
            hand.pop(hand.index(Card.GEMSTONE_CAVERNS))
            for card in exile_order:
                if card == Card.TREASURE_HUNT:
                    if hand.count(card) <= 1:
                        break
                if card in hand:
                    hand.pop(hand.index(card))
                    exiled = True
                    battlefield.lands.append(LandState.new_pair(Card.GEMSTONE_CAVERNS_LUCKY))
                    break
            if not exiled:
                hand.append(Card.GEMSTONE_CAVERNS)
                
    return hand, deck, battlefield
             
def play_lands(hand, deck, battlefield):

    if not contains_lands(hand):
        return hand, deck, battlefield

    land_types = list(map(lambda l: l[0], battlefield.lands))

    if len(battlefield.lands) == 0:
        pass
        if hand.count(Card.SPIREBLUFF_CANAL) + hand.count(Card.GEMSTONE_MINE) >= 2:
            if Card.SPIREBLUFF_CANAL in hand:
                battlefield.lands.append(LandState.new_pair(hand.pop(hand.index(Card.SPIREBLUFF_CANAL))))
                return hand, deck, battlefield
                
            if Card.GEMSTONE_MINE in hand:
                battlefield.lands.append(LandState.new_pair(hand.pop(hand.index(Card.GEMSTONE_MINE))))
                return hand, deck, battlefield
                
        if hand.count(Card.SPIREBLUFF_CANAL) + hand.count(Card.GEMSTONE_MINE) >= 1 \
           and hand.count(Card.CASCADE_BLUFFS) >= 1:
            if Card.SPIREBLUFF_CANAL in hand:
                battlefield.lands.append(LandState.new_pair(hand.pop(hand.index(Card.SPIREBLUFF_CANAL))))
                return hand, deck, battlefield
                
            if Card.GEMSTONE_MINE in hand:
                battlefield.lands.append(LandState.new_pair(hand.pop(hand.index(Card.GEMSTONE_MINE))))
                return hand, deck, battlefield
                
        if Card.TOLARIA_WEST in hand:
                battlefield.lands.append(LandState.new_pair(hand.pop(hand.index(Card.TOLARIA_WEST))))
                return hand, deck, battlefield
        
        play_order = [Card.ISLAND,
                      Card.OBORO,
                      Card.MOUNTAIN, 
                      Card.RELIQUARY_TOWER,
                      Card.CASCADE_BLUFFS,
                      Card.NEPHALIA_ACADEMY,
                      Card.BOSEIJU,
                      Card.DESOLATE_LIGHTHOUSE,
                      Card.GEMSTONE_CAVERNS]
        for card in play_order:
            if card in hand:
                battlefield.lands.append(LandState.new_pair(hand.pop(hand.index(card))))
                return hand, deck, battlefield

    if len(battlefield.lands) == 1:
        if hand.count(Card.RELIQUARY_TOWER) > 0 and can_produce_blue(land_types):
            battlefield.lands.append(LandState.new_pair(hand.pop(hand.index(Card.RELIQUARY_TOWER))))
            return hand, deck, battlefield
            
        elif battlefield.lands[0][0] == Card.RELIQUARY_TOWER and can_produce_blue(filter(lambda l: l == Card.TOLARIA_WEST, hand)):
            for (i, card) in enumerate(hand):
                if (not card == Card.TOLARIA_WEST) and can_produce_blue([card]):
                    hand.pop(i)
                    battlefield.lands.append(LandState.new_pair(card))
            return hand, deck, battlefield
        
    if Card.RELIQUARY_TOWER in hand and not Card.RELIQUARY_TOWER in land_types and can_produce_blue(land_types):
            battlefield.lands.append(LandState.new_pair(hand.pop(hand.index(Card.RELIQUARY_TOWER))))
            return hand, deck, battlefield        
        
    if Card.CASCADE_BLUFFS in hand and (can_produce_blue(land_types) or can_produce_red(land_types)):
            battlefield.lands.append(LandState.new_pair(hand.pop(hand.index(Card.CASCADE_BLUFFS))))
            return hand, deck, battlefield

    if Card.GEMSTONE_MINE in hand:
            battlefield.lands.append(LandState.new_pair(hand.pop(hand.index(Card.GEMSTONE_MINE))))
            return hand, deck, battlefield

    if Card.SPIREBLUFF_CANAL in hand and len(battlefield.lands) < 2:
            battlefield.lands.append(LandState.new_pair(hand.pop(hand.index(Card.SPIREBLUFF_CANAL))))
            return hand, deck, battlefield

    if can_produce_blue(land_types):
        if Card.MOUNTAIN in hand:
                battlefield.lands.append(LandState.new_pair(hand.pop(hand.index(Card.MOUNTAIN))))
                return hand, deck, battlefield
    
    play_order = [Card.GEMSTONE_MINE,
                  Card.SPIREBLUFF_CANAL,
                  Card.TOLARIA_WEST,
                  Card.ISLAND,
                  Card.MOUNTAIN,
                  Card.OBORO,
                  Card.RELIQUARY_TOWER,
                  Card.CASCADE_BLUFFS,
                  Card.DESOLATE_LIGHTHOUSE,
                  Card.NEPHALIA_ACADEMY,
                  Card.BOSEIJU,
                  Card.GEMSTONE_CAVERNS]
    for card in play_order:
        if card in hand:
            battlefield.lands.append(LandState.new_pair(hand.pop(hand.index(card))))
            return hand, deck, battlefield
    
    return hand, deck, battlefield

def try_tap_mana(u, r, c, sources):
    cb_tpd = 0
    u_tpd = 0
    r_tpd = 0
    c_tpd = 0
    tbt = []

    land_types = list(map(lambda l: l[0], sources))

    if Card.CASCADE_BLUFFS in land_types and (can_produce_blue(land_types) or can_produce_red(land_types)):
        bluffs = filter(lambda l: l == Card.CASCADE_BLUFFS, land_types)
        for bluff in bluffs:
            if u >= 1 or r >= 1:
                tapped = False
                cbs_idx = land_types.index(Card.CASCADE_BLUFFS)
                sub_sources = list(sources)
                sub_sources.pop(cbs_idx)
                urec, rrec, crec, tbt = try_tap_mana(1, 0, 0, sub_sources)
                if urec > 1:
                    tapped = True
                else:
                    urec, rrec, crec, tbt = try_tap_mana(0, 1, 0, sub_sources)
                    if rrec > 1:
                        tapped = True
                sources[cbs_idx][1].tapped = True
                if u - u_tpd >= 2:
                    u_tpd += 2
                elif r - r_tpd >= 2:
                    r_tpd += 2
                elif u - u_tpd >= 1 and r - r_tpd >= 1:
                    r_tpd += 1
                    u_tpd += 1
                elif u - u_tpd >= 1 and c - c_tpd >= 1:
                    u_tpd += 1
                    c_tpd += 1
                elif r - r_tpd>= 1 and c - c_tpd >= 1:
                    r_tpd += 1
                    c_tpd += 1
                else:
                    c_tpd += 2

    for (l, ls) in sources:
        if l in red_sources and r_tpd < r:
            tbt.append(ls)
            r_tpd += 1
        elif l in blue_sources and u_tpd < u:
            tbt.append(ls)
            u_tpd += 1
        elif c_tpd < c:
            tbt.append(ls)
            c_tpd += 1
    return u_tpd, r_tpd, c_tpd, tbt

def try_cast(card, battlefield):
    mana_sources = list(filter(lambda l: not l[1].tapped, battlefield.lands))
    land_types = list(map(lambda l: l[0], mana_sources))
    """if Card.CASCADE_BLUFFS in mana_sources and (can_produce_blue(land_types) or can_produce_red(land_types)):
        if card == Card.LIGHTNING_STORM and mana_sources >= 3:
            u, r, c, _ = try_tap_mana(0, 2, 1, mana_sources)
            return u >= 0 and r >= 2 and c >= 1
        if card == Card.TREASURE_HUNT:
            u, r, c, _ = try_tap_mana(1, 0, 1, mana_sources)
            return u >= 1 and r >= 0 and c >= 1
    """
    if card == Card.LIGHTNING_STORM:
        u, r, c, to_tap = try_tap_mana(0, 2, 1, mana_sources)
        if u >= 0 and r >= 2 and c >= 1:
            for tap in to_tap:
                tap.tapped = True
            return True
        return False
    
    if card == Card.TREASURE_HUNT:
        u, r, c, to_tap = try_tap_mana(1, 0, 1, mana_sources)
        if u >= 1 and r >= 0 and c >= 1:
            for tap in to_tap:
                tap.tapped = True
            return True
        return False        
    
discard_order = [
    Card.GEMSTONE_CAVERNS,
    Card.NEPHALIA_ACADEMY,
    Card.BOSEIJU,
    Card.OBORO,
    Card.DESOLATE_LIGHTHOUSE,
    Card.TOLARIA_WEST,
    Card.RELIQUARY_TOWER,
    Card.ISLAND,
    Card.MOUNTAIN,
    Card.CASCADE_BLUFFS,
    Card.SPIREBLUFF_CANAL,
    Card.GEMSTONE_MINE,
    Card.LIGHTNING_STORM,
    Card.TREASURE_HUNT
]
    
def turn(hand, deck, battlefield):

    land_played = False
    
    for (land_type, land_state) in battlefield.lands:
        land_state.tapped = False

    hand.append(deck.pop(0))

    if len(battlefield.lands) < 2:
        hand, deck, battlefield = play_lands(hand, deck, battlefield);
        land_played = True
        
    land_types = list(map(lambda l: l[0], battlefield.lands))
    land_amount = len(list(filter(lambda c: c.value[0] == CardType.LAND, hand)))
    
    #print(Card.LIGHTNING_STORM in hand , land_amount >= 7 , try_cast(Card.LIGHTNING_STORM, battlefield))
    #print(land)
    if Card.LIGHTNING_STORM in hand and land_amount >= 7 and try_cast(Card.LIGHTNING_STORM, battlefield):
        return hand, deck, battlefield, True
        
    if Card.TREASURE_HUNT in hand and len(battlefield.lands) >= 2 and not land_played and try_cast(Card.TREASURE_HUNT, battlefield):
        hand.pop(hand.index(Card.TREASURE_HUNT))
        while (len(deck) > 2) and (deck[0].value[0] == CardType.LAND):
            hand.append(deck.pop(0))
        hand.append(deck.pop(0))
    
    if not land_played:
        mana_sources = list(filter(lambda l: not l[1].tapped, battlefield.lands))
        ul, rl, cl, tbtl = try_tap_mana(0, 2, 1, mana_sources)
        uh, rh, ch, tbtl = try_tap_mana(1, 0, 1, mana_sources)
        if (not Card.RELIQUARY_TOWER in land_types) or not (rl >= 2 and cl >= 1 and uh >= 1 and ch >= 1):
            hand, deck, battlefield = play_lands(hand, deck, battlefield);
    
    if Card.TREASURE_HUNT in hand and Card.RELIQUARY_TOWER in list(map(lambda l: l[0], battlefield.lands)):
        if try_cast(Card.TREASURE_HUNT, battlefield):
            hand.pop(hand.index(Card.TREASURE_HUNT))
            while (len(deck) > 2) and (deck[0].value[0] == CardType.LAND):
                hand.append(deck.pop(0))
            hand.append(deck.pop(0))
        
        return hand, deck, battlefield, False
    
    if not Card.RELIQUARY_TOWER in list(map(lambda l: l[0], battlefield.lands)):
        while len(hand) > 7:
            for card in discard_order:
                if card in hand:
                    hand.pop(hand.index(card))
                    break
            
    return hand, deck, battlefield, False        
        
        
#with open(csv_file, 'w') as csvfile:
#    fieldnames = ["turnnumber", "lands", "hand", "win"]
#    writer = csv.writer(csvfile)
#    writer.writeheader(fieldnames)
maxturns = 0
turncounts = []
turnamounts = 1000000
for i in tqdm(range(turnamounts)):
    hand, deck = first_hand()
    hand, deck, battlefield = pregame_actions(hand, deck)
    won = False
    turncount = 0
    while (not won) and len(deck) > 1:
        #print(battlefield.lands, len(deck), hand)
        hand, deck, battlefield, won = turn(hand, deck, battlefield)
        turncount += 1
    if turncount > maxturns:
        maxturns = turncount
    turncounts.append(turncount)
 
print("Average game length: ", sum(turncounts)/turnamounts)
plot.hist(turncounts, bins=maxturns, align='mid') 
plot.xlim([0, maxturns]) 
#axis([xmin,xmax,ymin,ymax])
plot.xlabel('Turns')
plot.ylabel('Amount')
plot.show()

    
#with open(gnuplotfile, 'w') as plotfile:
#    print("Turn", "Amount", file=plotfile)
#    for i in range(60):
#        print(i, turncounts[i], file=plotfile)
    
    

    

    
    

