## Potential Next Steps:

### Research
- How do you do Reinforcement Learning?
- How do you vectorize the board state?
- What do you evaluate? what is your target?
- RL has a reward function w/ rewards and penalties
    - how do we break down the game into buckets of desirable and non-desirable behavior
    - ex: Desirable -- win, increase the number of points represented on board state
    - ex: Undesirable -- play for a ton of rounds
- Neural Net design considerations:
    - First step, something simple like a FFN or CNN for a DQN 
    - Game data is sequential, maybe transformers?!? -> tokenization
    - If we go down the transformer hole, look into huggingface
- Use models that predict likelihood to win, other player's cards, desirable next action/card choice

### Code Refactoring + Debugging
- bug in how board state is being updated
    - Fixed I think
- Unit testing game and player classes

### Supporting AI w/ Code
- board state vectorization
- Develop out AI Player class extension
- update choose to be amenable to a NN playing the game
    - may require passing in a parameter to specify if we're choosing an action or whatever so we can use separate models for choosing cards and actions

### Long Term project vision
- Flask app w/ javascript GUI that lets you play the game
- treesearch formulation

### Actionable Steps:
- find resources that may be useful, skim and share if they seem useful.
- meeting cadence: Monday, Thursday around 5PM