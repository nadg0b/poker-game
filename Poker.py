import random, json
from Player import Player
from collections import namedtuple

CARD = namedtuple("Card", ["rank", "suit"])

class PokerGame(object):
    MIN_PLAYERS = 2
    MAX_PLAYERS = 9
    RANKS = (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14)    # 11 - Jack, 12 - Queen, 13 - King, 14(1) - Ace
    SUITS = (1, 2, 3, 4)                                    # 1 - ♠(Spades), 2 - ♥(Hearts), 3 - ♣(Clubs), 4 - ♦(Diamonds)
    HANDS_RATE = {
        "high card"       : 1,
        "pair"            : 2,
        "two pair"        : 3,
        "three of a kind" : 4,
        "straight"        : 5,
        "flush"           : 6,
        "full house"      : 7,      
        "four of a kind"  : 8,       
        "straight flush"  : 9,
        "royal flush"     : 10
    }

    def __init__(self, *players: Player):
        '''init function creates deck, list of players, table (common cards + hole cards)
        '''
        if not all(isinstance(p, Player) for p in players):
            raise ValueError(f"Passing non-players object to {type(self).__name__}")
        elif len(players) > self.MAX_PLAYERS:
            raise ValueError(f"Number of players exceeds the maximum player limit of {self.MAX_PLAYERS}")

        self.players = list(players)
        self.deck = [CARD(rank, suit) for rank in self.RANKS for suit in self.SUITS]
        self.table = []
        self.comm_cards = []

        self.test_range = 1_000_000
        self.test_count = {
            "high card"       : 0,
            "pair"            : 0,
            "two pair"        : 0,
            "three of a kind" : 0,
            "full house"      : 0,
            "four of a kind"  : 0,
            "straight"        : 0,      
            "flush"           : 0,       
            "straight flush"  : 0,
            "royal flush"     : 0
        }


    def add_player(self, player: Player):
        '''function to add player
        '''
        if player in self.players:
            raise ValueError(f"Trying to add existing player object '{player.name}'")
        elif not (isinstance(player, Player)):
            raise ValueError(f"Trying to add non-player object {type(player)}")
        elif len(self.players) + 1 > self.MAX_PLAYERS:
            raise ValueError(f"Number of players exceeds the maximum player limit of {self.MAX_PLAYERS}")
        
        self.players.append(player)


    def remove_player(self, player: Player):
        '''function to remove existing player
        '''
        if player not in self.players:
            raise ValueError(f"There is no such player '{player.name}'")
        
        self.players.remove(player)
    

    def print_players(self):
        '''function to print all players
        '''
        for player in self.players:
            print(f"Player {player.name} has ${player.balance}")


    def shuffle(self):
        '''function to shuffle deck
        '''
        random.shuffle(self.deck)


    def deal(self, num: int):
        '''function to deal n cards from deck
        '''
        if num > len(self.table):
            raise ValueError(f"Can't deal {num}, there is {len(self.table)} cards left in the table")
        return [self.table.pop() for _ in range(num)]


    def get_hands(self):
        '''function to determine player's hand
        '''
        for player in self.players:
            print(f"{player.name} has {self.comm_cards + player.hole_cards}")
            cards = sorted(self.comm_cards + player.hole_cards, reverse=True)

            # dict to store all player's combinations
            hands = {}

            ranks = [card.rank for card in cards]
            # print("ranks", ranks)

            suits = [card.suit for card in cards]
            # print("suits", suits)

            r_count = dict((rank, ranks.count(rank)) for rank in set(ranks))
            # print("ranks count", r_count)

            s_count = dict((suit, suits.count(suit)) for suit in self.SUITS)
            # print("suits count", s_count)

            kinds = {
                     2: [],
                     3: [],
                     4: []
            }

            for r in set(ranks):
                kind = cards[ranks.index(r):ranks.index(r)+r_count[r]]
                for k in kinds.keys():
                    for p in range(len(kind)//k):
                        kinds[k] += [kind[p*k:p*k+k]]

            # print("kinds", kinds)

            high_card = cards[0]
            # print("high card", high_card)
            
            pairs = kinds[2]
            # print("pairs", pairs)

            t_pairs = pairs if len(pairs) >= 2 else []
            # print("two pairs", t_pairs)

            triples = kinds[3]
            # print("triples", triples)

            full_house = []
            if pairs and triples:
                m_pair = sorted([p if all(map(lambda c: c not in triples[-1], p)) else [] for p in pairs])
                if m_pair[-1]: full_house = [triples[-1] + m_pair[-1]]
            # print("full house", full_house)

            quads = kinds[4]
            # print("quads", quads)

            straight = [cards[0]]
            for i in range(1, len(cards)):
                # card_diff    description
                #         0  - cards have the same rank 
                #        -1  - straight pair
                card_diff = cards[i].rank - cards[i-1].rank
                if (card_diff == 0) or (card_diff == -1):  # problem with card diff 0
                    straight.append(cards[i])              # try to gather straight without duplicates then extend for
                else:                                      # straight flush check
                    if len(set(c.rank for c in straight)) < 5:
                        if not (straight[-1] == 2):
                            straight.clear()
                            straight.append(cards[i])             

            if (straight[-1].rank == 2) and (14 in ranks):
                straight += cards[:r_count[14]]

            if len(set(c.rank for c in straight)) < 5:
                straight.clear()
            # print("straight", straight)

            flush = list(filter(lambda c: s_count[c.suit]>=5, cards))
            # print("flush", flush)

            s_flush = []
            if straight:
                if any([len(list(filter(lambda c: c.suit == s, straight))) >= 5 for s in self.SUITS]):
                    s_flush = straight
            # print("straight flush", s_flush)

            r_flush = []
            if s_flush:
                if s_flush[0].rank == 14:
                    r_flush = s_flush
            # print("royal flush", r_flush)

            hands["high card"] = high_card
            hands["pair"] = pairs
            hands["two pair"] = t_pairs
            hands["three of a kind"] = triples
            hands["full house"] = full_house
            hands["four of a kind"] = quads
            hands["straight"] = straight      
            hands["flush"] = flush       
            hands["straight flush"] = s_flush
            hands["royal flush"] = r_flush

            if high_card: self.test_count["high card"] += 1
            if pairs: self.test_count["pair"] += 1
            if t_pairs: self.test_count["two pair"] += 1
            if triples: self.test_count["three of a kind"] += 1
            if full_house: self.test_count["full house"] += 1
            if quads: self.test_count["four of a kind"] += 1
            if straight: self.test_count["straight"] += 1    
            if flush: self.test_count["flush"] += 1      
            if s_flush: self.test_count["straight flush"] += 1
            if r_flush: self.test_count["royal flush"] += 1

            player.hands = hands
            print(f"{player.name}\n{json.dumps(player.hands, indent=4)}")


    def get_winner(self):
        winners = []
        for player in self.players:
            p_hands = [hand for hand in player.hands.items() if hand[1]]
            winners.append((player.name, max(p_hands, key=lambda h: self.HANDS_RATE[h[0]])))
        for w in winners:
            print(w)
                    

    def test_play(self, table=None):
        '''function to test behaviour of main class
        '''
        self.shuffle()
        self.table = table if table else self.deck[:5+2*len(self.players)]

        for player in self.players:
            player.hole_cards = self.deal(2)

        self.comm_cards = self.deal(5)

        self.get_hands()


# streets (poker stages) to implement with state machine
    def pre_flop(self):
        ...


    def flop(self):
        ...
    

    def turn(self):
        ...


    def river(self):
        ...