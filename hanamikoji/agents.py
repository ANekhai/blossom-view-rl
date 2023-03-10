from player import Player
import random

class RandomAgent(Player):

    def __init__(self, name:str="Random-Bot"):
        super().__init__(name)

    
    # Override choose to make random choices!
    def choose(self, options: list, message: str, n_choices: int = 1):
        print(message)
        choices = list(range(len(options)))
        choice = random.sample(choices, n_choices)
        print(f"{self.name} makes choice: {[options[i] for i in choice]}")

        return choice if n_choices > 1 else choice[0]

