import random
from player import Player
from constants import GEISHA_COLORS, GEISHA_POINTS, ACTION_NAMES, ACTION_DESCRIPTIONS

### An attempt to get ChatGPT to write a game class for Hanamikoji ###
# Addendum: ChatGPT rapidly forgets what it wrote between prompts sometimes
# It will also radically change the implementation (often for the worse!)
# I have diagrammed out most of the necessary functionality with ChatGPT
# However most of the Game class was written by me

def actions_to_string(actions: list[int]):
    names = [ACTION_NAMES[i] for i in actions]
    descriptions = [ACTION_DESCRIPTIONS[i] for i in actions]
    lines = [f"{n}: {d}" for n, d in zip(names, descriptions)]
    return "\n".join(lines)


class Game:
    def __init__(self, player1: Player, player2: Player) -> None:
        self.players: list[Player] = [player1, player2]
        self.current_player: int = 0
        self.first_player: int = random.choice([0, 1])
        self.have_winner = False
        self.deck = []

        self.board = {i: [0, 0] for i in range(1, 8)}

        # Initialize the game
        self.initialize_game()
    
    def initialize_game(self):
        
        pass

    def reset_game(self) -> None:
        pass

    def initialize_round(self):
        
        # initialize deck
        self.deck = []
        for geisha, value in GEISHA_POINTS.items():
            self.deck += [geisha] * value
        random.shuffle(self.deck)

        # remove top card from the game
        self.deck.pop()

        for player in self.players:
            player.reset_player()
            # deal cards
            player.add_cards_to_hand(self.deck[:6])
            self.deck = self.deck[6:]

        # swap first player
        self.first_player = 1 - self.first_player
        self.current_player = self.first_player

    def play(self):
        print("Starting Game!!!")
        winner = False
        while not winner:
            winner = self.round()


    def turn(self):
        turn_player = self.players[self.current_player]

        # player draws a card
        print(f"{turn_player.name} draws a card")
        turn_player.add_card_to_hand(self.deck.pop())
        
        # print board state
        print(turn_player.to_string())
        print("Current Board State:")
        print(self.board_to_string())
        
        # player picks a remaining action
        actions = turn_player.actions_remaining
        print("Remaining Actions:")
        print(actions_to_string(actions))

        action_idx = turn_player.choose(options=[ACTION_NAMES[i] for i in actions], 
                           message="Choose an action")
        action = actions[action_idx]

        # resolve the action
        match action:
            case 1:
                self.secret_action()
            case 2:
                self.trade_off_action()
            case 3:
                self.gift_action()
            case 4:
                self.competition_action()
        # update remaining actions
        turn_player.use_action(action)

    def secret_action(self):
        # Pick a card to put in the secret pile
        player, hand = self.current_player_and_hand()
        card_idx = player.choose(hand, f"{player.name}: pick a card to keep secret: ")
        card = hand[card_idx]
        player.add_secret(card)
        player.remove_card_from_hand(card)

    def trade_off_action(self):
        player, hand = self.current_player_and_hand()
        card_idxs = player.choose(hand, f"{player.name}: pick two cards to trade away", n_choices=2)
        cards = [hand[i] for i in card_idxs]
        player.add_traded(cards)
        for card in cards: player.remove_card_from_hand(card)


    def gift_action(self):
        # pick three cards
        player, hand = self.current_player_and_hand()
        card_idxs = player.choose(hand, f"{player.name}: pick three cards as gifts", n_choices=3)
        cards = [hand[i] for i in card_idxs]

        # remove them from hand
        for card in cards: player.remove_card_from_hand(card)
        # have opponent choose one
        opp_idx = 1 - self.current_player
        card_idx = self.players[opp_idx].choose(cards, f"{self.players[opp_idx].name}: choose a card to keep")
        card = cards[card_idx]
        cards.remove(card)
        # give opponent their picked card, keep your picked cards
        self.add_cards_to_board([card], opp_idx)
        self.add_cards_to_board(cards, self.current_player)

    def competition_action(self):
        player, hand = self.current_player_and_hand()
        # pick piles
        piles = []
        for num in ["first", "second"]:
            idxs = player.choose(hand, f"{player.name}: pick two cards for {num} pile", n_choices=2)
            pile = [hand[i] for i in idxs]
            for card in pile: player.remove_card_from_hand(card)
            piles.append(pile)

        # opponent picks one to keep
        opp_idx = 1 - self.current_player
        pile_idx = self.players[opp_idx].choose(piles, f"{self.players[opp_idx].name}: choose a pile to keep")
        self.add_cards_to_board(piles[pile_idx], opp_idx)
        self.add_cards_to_board(piles[1 - pile_idx], self.current_player)


    def current_player_and_hand(self) -> tuple[Player, list[int]]:
        return self.players[self.current_player], self.players[self.current_player].hand

    def add_cards_to_board(self, cards: list, player: int) -> None:
        for card in cards: self.board[card][player] += 1


    
    def round(self) -> bool:
        # intialize board state
        self.initialize_round()
        
        for turn in range(1, 9):
            print("*" * 10, f"Turn {turn}: {self.players[self.current_player].name}'s turn", "*" * 10)
            self.turn()
            
            # swap players
            self.swap_current_player()
        # update geisha favors

        #check wincons
        found_winner = False
        return found_winner
    
    def board_to_string(self) -> str:
        names = [player.name for player in self.players]
        result = [f"{key}: {names[0]}: {vals[0]} {names[1]}: {vals[1]}\tTotal: {GEISHA_POINTS[key]}" 
                  for key, vals in self.board.items()]
        return '\n'.join(result)
    
    def swap_current_player(self):
        self.current_player = 1 - self.current_player


if __name__ == "__main__":
    p1 = Player("Alice")
    p2 = Player("Bob")

    game = Game(p1, p2)
    
    game.play()
