from Player import Player
from Poker import PokerGame, CARD


def main():
    player1 = Player("Jim", 500)
    player2 = Player("George")
    player3 = Player("Matt")
    poker = PokerGame(player1, player2, player3)

    # poker.test_play([CARD(14, 4), CARD(13, 4), CARD(12, 4), CARD(4, 4), CARD(2, 1), 
    #                  CARD(10, 4), CARD(11, 4),
    #                  CARD(5,  4), CARD(2,  4), 
    #                  CARD(14, 2), CARD(14, 3)])
    poker.test_play()
    poker.get_winner()
    # for _ in range(poker.test_range):
    #     poker.test_play()
    # for hand in poker.test_count.items():
    #     print(f"{hand[0]} -> {hand[1]/poker.test_range*100}% ")

if __name__ == "__main__":
    main()