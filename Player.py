class Player(object): 
    def __init__(self, name:str, balance: int=1000):
        self.name = name
        self.balance = balance
        self.hole_cards = []
        self.hands = {}