from constants import GEISHA_POINTS

# A second attempt at getting chatgpt to write a functional version of hanamikoji
# ChatGPT wrote most of the getters and setters

class Player:
    def __init__(self, name: str) -> None:
        self.name = name
        self.hand = []
        self.actions_remaining = [1, 2, 3, 4]
        self.favors_won = {1: False, 2: False, 3: False, 4: False, 5: False, 6: False, 7: False}

        # player specific hidden zones
        self.secret = []
        self.traded = []


    def reset_player(self, reset_favors: bool = False) -> None:
        self.hand = []
        self.actions_remaining = [1, 2, 3, 4]
        self.secret = []
        self.traded = []

        if reset_favors:
            self.favors_won = {i: False for i in range(1, 8)}

    def add_card_to_hand(self, card: int) -> None:
        self.hand.append(card)

    def remove_card_from_hand(self, card: int) -> None:
        self.hand.remove(card)

    def use_action(self, action: int) -> None:
        self.actions_remaining.remove(action)

    def reset_actions(self) -> None:
        self.actions_remaining = [1, 2, 3, 4]

    def gain_favor(self, geisha: int) -> None:
        self.favors_won[geisha] = True

    def lose_favor(self, geisha: int) -> None:
        self.favors_won[geisha] = False

    def has_favor(self, geisha: int) -> bool:
        return self.favors_won[geisha]
    
    def add_cards_to_hand(self, cards: list[int]) -> None:
        self.hand.extend(cards)

    def charm_score(self) -> int:
        return sum([GEISHA_POINTS[i] for i in range(1, 8) if self.favors_won[i]])
    
    def total_favors_won(self) -> int:
        won_favors = [i for i in self.favors_won.values() if i]
        return len(won_favors)
    
    def add_secret(self, card: int) -> None:
        self.secret.append(card)

    def add_traded(self, cards: list[int]) -> None:
        self.traded.extend(cards)

    def choose(self, options: list, message: str, n_choices: int = 1):
        
        if n_choices < 1: raise ValueError("Cannot make 0 or fewer choices")
        
        print(message)
        print("Options are:")
        for i, option in enumerate(options):
            print(f"{i}: {option}")

        choice_message = "Choose option: " if n_choices == 1 else "Choose options (comma separated, spaces fine): "

        while True:

            try:
                user_input = input(choice_message)
                user_input = [int(i) for i in user_input.replace(" ", "").split(",")] if n_choices > 1 else int(user_input)
                
                valid_number = lambda x: x in range(len(options))

                if n_choices > 1:
                    # check for correct # of choices 
                    if len(set(user_input)) != n_choices or len(user_input) != n_choices: raise ValueError
                    if not all(map(valid_number, user_input)): raise ValueError
                else: 
                    if not valid_number(user_input): raise ValueError
                
                return user_input

            except:
                print("Invalid Response: Please try again")

    def to_string(self):
        base = f"{self.name}'s "
        result = []
        result.append(base + f"hand: {self.hand}")
        result.append(base + f"actions: {self.actions_remaining}")
        result.append(base + "secret: " + (f"{self.secret}" if self.secret else "None") )
        result.append(base + "traded: " + (f"{self.traded}" if self.traded else "None") )
        geishas = [i for i, won in self.favors_won.items() if won]
        result.append(base + "geishas: " + (f"{geishas}" if geishas else "None") )
        result.append(base + f"charm score: {self.charm_score()}")

        return "\n".join(result)


if __name__ == "__main__":
    tp = Player("Isaac")
    
    actions = ["a", "b", "c", "d"]
    out = tp.choose(options=actions, message="Pick one ya doofus")
    print(f"Choice Index: {out}")

    # actions = ["a", "b", "c", "d", "e"]
    # out = tp.choose(options=actions, message="Pick two ya doofus", n_choices=2)
    # print(out)

    # tp.gain_favor(1)
    # tp.gain_favor(5)
    # tp.gain_favor(6)

    # print(tp.to_string())
