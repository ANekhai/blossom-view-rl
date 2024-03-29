import random
from player import Player
from agents import RandomAgent
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
        self.first_player: int = random.choice([0, 1]) # TODO: Validate that players swap between rounds
        self.deck: list[int] = []

        # winner tracking
        self.has_winner: bool = False
        self.winner: int = None

        self.board: dict[int, list[int]] = {i: [0, 0] for i in range(1, 8)}

        # initialize the game
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

        # reset board
        self.board = {i: [0, 0] for i in range(1, 8)}

        # swap first player
        self.first_player = 1 - self.first_player
        self.current_player = self.first_player

    ### GAME FUNCTIONS ###

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

    def round(self) -> None:
        # intialize board state
        self.initialize_round()
        
        for turn in range(1, 9):
            print("*" * 10, f"Turn {turn}: {self.players[self.current_player].name}'s turn", "*" * 10)
            self.turn()
            
            # swap players
            self.swap_current_player()
        
        # update geisha favors
        self.update_favors()

        #check wincons
        self.determine_winner()

    def play(self):
        print("Starting Game!!!")
        round = 1
        while not self.has_winner:
            print("*" * 10, f"Round {round}", "*" * 10)
            self.round()
            round += 1

        print(f"Final board state at round {round}:")
        print(self.board_to_string())

        winning_player = self.players[self.winner]
        print(f"{winning_player.name} is the winner with {winning_player.charm_score()} charm points and {winning_player.total_favors_won()} favors won! Congratulations!")

    ### ACTION IMPLEMENTATIONS

    def secret_action(self) -> None:
        # Pick a card to put in the secret pile
        player, hand = self.current_player_and_hand()
        card_idx = player.choose(hand, f"{player.name}: pick a card to keep secret: ")
        card = hand[card_idx]
        player.add_secret(card)
        player.remove_card_from_hand(card)

    def trade_off_action(self) -> None:
        player, hand = self.current_player_and_hand()
        card_idxs = player.choose(hand, f"{player.name}: pick two cards to trade away", n_choices=2)
        cards = [hand[i] for i in card_idxs]
        player.add_traded(cards)
        for card in cards: player.remove_card_from_hand(card)

    def gift_action(self) -> None:
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

    def competition_action(self) -> None:
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

    ### Victory tracking

    def determine_round_favors(self) -> dict[int, str]:
        results = {}
        for i in self.board.keys():
            # go through each geisha and see which player has the most points
            if self.board[i][0] > self.board[i][1]:
                results[i] = 0
            elif self.board[i][0] < self.board[i][1]:
                results[i] = 1
            else:
                results[i] = None
        return results
    
    def get_favors_won(self):
        favors = {i: None for i in range(1, 8)}
        
        for i in range(1, 8):
            favor_vector = list(map(
                lambda p: p.has_favor(i), self.players))

            assert(not all(favor_vector))

            if any(favor_vector): 
                favors[i] = favor_vector.index(True)

        return favors

    def update_favors(self):
        # add secret cards to board
        for i in range(2):
            secret_card = self.players[i].secret[0]
            self.board[secret_card][i] += 1

        print("Final Board State:")
        print(self.board_to_string())

        # get current favor winners
        favors = self.determine_round_favors()
        for geisha, player in favors.items():
            # avoid any updates for ties
            if player is None:
                continue

            # add favor
            self.players[player].gain_favor(geisha)
            # other player loses favor of this geisha
            other_player = 1 - player
            self.players[other_player].lose_favor(geisha)

    def determine_winner(self) -> None:
        charm_won = [player.charm_score() > 10 for player in self.players]
        favors_won = [player.total_favors_won() > 3 for player in self.players]
        
        # check for winner
        if any(charm_won) or any(favors_won): 
            self.has_winner = True
        
        # determine who won
        # TODO: check victory edge case
        if any(charm_won):
            self.winner = charm_won.index(True)
        elif any(favors_won):
            self.winner = favors_won.index(True)       

    def board_to_string(self) -> str:
        names = [player.name for player in self.players]
        print(self.get_favors_won())
        curr_favors = self.determine_round_favors()
        favor_names = {i: self.players[k].name if k is not None else "None" for i, k in curr_favors.items()}
        result = [f"{key}: {names[0]}: {vals[0]} {names[1]}: {vals[1]}\t Leader: {favor_names[key]}\tTotal: {GEISHA_POINTS[key]}" 
                  for key, vals in self.board.items()]
        return '\n'.join(result)
    
    def swap_current_player(self):
        self.current_player = 1 - self.current_player


if __name__ == "__main__":
    p1 = Player("Alice")
    p2 = Player("Bob")

    p1 = RandomAgent("Alice-Bot")
    p2 = RandomAgent("Bob-Bot")

    game = Game(p1, p2)
    
    game.play()
