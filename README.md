# Minimal Hanabi Emulator

![Hanabi](https://images-na.ssl-images-amazon.com/images/I/51tQM1c%2BTHL.jpg)

[Hanabi](https://en.wikipedia.org/wiki/Hanabi_%28card_game%29) is a cooperative card game created by Antoine Bauza. Playing the game successfully demands players effectively cultivate a *theory of mind* for each of their team mates. For this reason, Hanabi was recently identified as a challenging ["new frontier for AI research"](https://deepmind.com/research/publications/hanabi-challenge-new-frontier-ai-research).

This ultra-minimal (194 lines of Python 3) Hanabi emulator provides a simple test bed for the Hanabi problem. It should be easy for anybody to run and understand, and has no dependencies aside from the `random` module (for shuffling the deck!)

---

`example.py` walks you through the basic interactions needed to play the game. Broadly speaking:

- Initialise the game with a set of players.
- For each turn, the active player *p*:
  - Receives an observation of the game state from their perspective, and surveys what pieces of information it may give to the other players.
  - Decides which action to take: play, discard or give information.
  - Submits the action to the game emulator.
- The game ends when either the maximum score is reached, the players run out of 'fuses', or the deck is empty.

Enjoy!